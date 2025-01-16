import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.contribution import Contribution
from src.models.contribution import ContributionBase, ContributionResponse
from src.db import Project, User
from src.db.db import get_db
from src.models.project import ProjectCreate, ProjectResponse, ProjectListResponse
from src.utils.oauth2 import get_current_user
from typing import List




router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new project. The creator must be authenticated.
    """

    existing_project = db.query(Project).filter(Project.name == project.name).first()
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A project with the name '{project.name}' already exists."
        )
    

    new_project = Project(
        name=project.name,
        description=project.description,
        creator_id=current_user.id,
        goal_amount=project.goal_amount,
        deadline=project.deadline,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return ProjectResponse(
        id=new_project.id,
        name=new_project.name,
        description=new_project.description,
        goal_amount=new_project.goal_amount,
        deadline=new_project.deadline,
        created_at=new_project.created_at,
        number_of_contributions=new_project.number_of_contributions,
        total_contributions=0,  # No contributions yet
        contributors=[],  # No contributors yet
        creator_id=new_project.creator_id,
    )





@router.get("/", response_model=List[ProjectListResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    project_list = []
    for project in projects:
        total_contributions = sum(c.amount for c in project.contributions)
        contributor_count = len(set(c.contributor_id for c in project.contributions))

        project_list.append(ProjectListResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            goal_amount=project.goal_amount,
            deadline=project.deadline,
            creator_id=project.creator_id,
            created_at=project.created_at,
            number_of_contributions=len(project.contributions),
            total_contributions=total_contributions,
            contributor_count=contributor_count,
        ))

    return project_list



@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    """
    Get details of a single project by its ID, including total contributions and contributor usernames.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    

    total_contributions = sum(contribution.amount for contribution in project.contributions)
    
  
    contributors = [contribution.contributor.username for contribution in project.contributions]
    
   
    project_response = ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        goal_amount=project.goal_amount,
        deadline=project.deadline,
        creator_id=project.creator_id,
        created_at=project.created_at,
        number_of_contributions=len(project.contributions),
        total_contributions=total_contributions,
        contributors=contributors,
    )
    return project_response





@router.post("/{project_id}/contribute", response_model=ContributionResponse, status_code=status.HTTP_201_CREATED)
def contribute_to_project(
    project_id: str,
    contribution: ContributionBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Contribute to a project identified by its ID.
    - Only authenticated users can contribute.
    - Validates that the project exists.
    - Ensures the project deadline has not passed.
    """
    
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.deadline < datetime.datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot contribute to a project after its deadline."
        )

   
    new_contribution = Contribution(
        amount=contribution.amount,
        project_id=project_id,
        contributor_id=current_user.id,
        contributed_at=datetime.datetime.utcnow()
    )

    db.add(new_contribution)


    project.number_of_contributions += 1
    project.contributions.append(new_contribution)

    db.commit()
    db.refresh(new_contribution)


    contributor_data = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }

    return {
        "id": new_contribution.id,
        "amount": new_contribution.amount,
        "contributed_at": new_contribution.contributed_at,
        "project_id": new_contribution.project_id,
        "contributor": contributor_data,
    }
