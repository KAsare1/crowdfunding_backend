# Crowdfunding Backend
Backend service for Crowdfunding

## Setup

### Prerequisites

- Python 3.11.0
- Virtual Environment (optional but recommended)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/KAsare1/crowdfunding_backend.git
    cd crowdfunding_backend
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```
    OR...

    ```sh
    cd .venv/bin
    activate
    cd ../..
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```env
        DB_URL=
        SECRET_KEY=
        REFRESH_KEY=
        REFRESH_EXPIRES=9000
        ACCESS_EXPIRES=7200
        ALGORITHM=HS256
    ```

### Running the Application

1. **Run the FastAPI application:**

    ```sh
    uvicorn src.main:app --host 127.0.0.1 --port 8080
    ```

2. **Access the API documentation:**

    Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.
