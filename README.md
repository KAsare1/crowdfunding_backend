# Akan Recorder
Backend service for recording Akan speech to gather data

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL
- Virtual Environment (optional but recommended)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Akan-ASR-for-Health/akan-recorder-backend
    cd akan-recorder-backend
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```env
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_SERVER=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=your_database_name
    SECRET=your_secret_key
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    EMAIL_USERNAME=your_email@example.com
    EMAIL_PASSWORD=your_email_password
    ```

### Setting up PostgreSQL Database

1. **Start PostgreSQL server:**

    Ensure that your PostgreSQL server is running.

2. **Create a new database:**

    ```sh
    psql -U postgres
    CREATE DATABASE your_database_name;
    ```

3. **Update the database URL in the `.env` file:**

    ```env
    DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@localhost:5432/your_database_name
    ```

### Running the Application

1. **Run the FastAPI application:**

    ```sh
    fastapi dev src/main.py
    ```

2. **Access the API documentation:**

    Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.
