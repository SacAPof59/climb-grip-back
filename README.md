# climb-grip-back

## Project Description
This project is a FastAPI application for measuring climbing-specific finger strength measures, such as Critical Force.

## Prerequisites
- Python 3.13 or higher
- pip (Python package installer)

## Installation

### Linux & Mac
1. **Clone the repository:**
    ```sh
    git clone https://github.com/SacAPof59/climb-grip-back.git
    cd climb-grip-back
    ```

2. **Create a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Windows
1. **Clone the repository:**
    ```sh
    git clone https://github.com/SacAPof59/climb-grip-back.git
    cd climb-grip-back
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application
1. **Start the FastAPI server:**
    ```sh
    uvicorn main:app --reload
    ```

2. **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000`.

## Endpoints
- **GET /**: Returns a welcome message.
- **GET /climber/create-test**: Creates a test climber in the database.

## License
This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for more details.