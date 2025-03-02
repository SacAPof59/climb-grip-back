# climb-grip-back

## Project Description

This project is a FastAPI application designed for measuring climbing-specific finger strength metrics, such as Critical
Force. It includes an API (`webapi`) for data management and a basic user interface (`temp_ui`) for interacting with the application.  The project also includes a GitHub Actions workflow for automated deployment to a VPS.

## Architecture Overview

*   **`temp_ui`**: This module provides a simple, temporary user interface built using HTML, CSS, and JavaScript. It's designed for basic interaction with the API, allowing users to view and interact with data. This UI is intended for demonstration and initial development.
*   **GitHub Actions**: The `.github/workflows/deploy.yml` file contains a workflow that automates the deployment of the application to a VPS. This ensures that code changes are automatically pushed to the server.
* **Database**: The application uses a relational database (SQLite by default, but configurable to others) to store the data. The `models` define the structure of the database.
* **Data Loading**: The `export_tool.py` file allows to load data from json files located in the `data` directory into the database.
*  (OPTIONAL) **`webapi`**: It serves as the backend of the application. It is currently unused, waiting for a UI migration to a proper frontend Javascript framework.

## Prerequisites

- Python 3.12 or higher (tested with 3.12.8)
- pip (Python package installer)
- git
- gunicorn
- uvicorn
- nginx
- certbot

## Installation

### Linux & Mac

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/SacAPof59/climb-grip-back.git
    cd climb-grip-back
    ```

2.  **Create a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

### Windows

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/SacAPof59/climb-grip-back.git
    cd climb-grip-back
    ```

2.  **Create a virtual environment:**

    ```sh
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application (Locally for development)

1.  **Start the FastAPI server:**

    ```sh
    uvicorn main:app --reload
    ```

2.  **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000`. You can access the api documentation at `http://127.0.0.1:8000/docs`

## Running the Application (Production - VPS setup)

This section describes how to deploy the application on a VPS using Gunicorn, Uvicorn, and Nginx with HTTPS.

### 1. Install Additional Packages:

   ```sh
  uvicorn main:app --reload
   ```

### 2. Run the Application with Gunicorn:

To run the application in production, use Gunicorn with Uvicorn workers. This provides stability and performance.

1.  **Navigate to the project directory:**

    ```bash
    cd /path/to/your/project/climb-grip-back
    ```

    Replace `/path/to/your/project/` with the correct path

2.  **Start Gunicorn:**

    ```bash
    gunicorn main:app --workers 3 --bind unix:climb-grip-back.sock --timeout 120 --worker-class uvicorn.workers.UvicornWorker --umask 007
    ```

    *   `main:app`: Specifies the entry point (the `app` object in `main.py`).
    *   `--workers 3`: Uses 3 worker processes.
    *   `--bind unix:climb-grip-back.sock`: Binds to a Unix socket for local communication.
    *   `--timeout 120`: Sets a 120-second timeout for each worker.
    *   `--worker-class uvicorn.workers.UvicornWorker`: Enables ASGI support using Uvicorn workers.
    *   `--umask 007`: set the correct permission to the socket
    *   the socket `climb-grip-back.sock` will be created in the current directory, from which the command is executed.

### 3. Configure Nginx as a Reverse Proxy:

Nginx handles HTTPS termination and forwards requests to Gunicorn via the Unix socket.

1.  **Create or edit the Nginx configuration file:**

    ```bash
    sudo nano /etc/nginx/sites-available/climb-grip-back
    ```

2.  **Add the following content to the configuration file:**

    ```nginx
    server {
        server_name your_domain.com www.your_domain.com;

        location / {
            proxy_pass http://unix:/path/to/your/project/climb-grip-back/climb-grip-back.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location /static {
            root /path/to/your/project/climb-grip-back/temp_ui;
        }

        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
    }
    server {
        if ($host = www.your_domain.com) {
            return 301 https://$host$request_uri;
        } # managed by Certbot
        if ($host = your_domain.com) {
            return 301 https://$host$request_uri;
        } # managed by Certbot

        listen 80;
        server_name your_domain.com www.your_domain.com;
        return 404; # managed by Certbot
    }
    ```

    *   Replace `your_domain.com` with your actual domain.
    *   Replace `/path/to/your/project/` with the correct path to your project directory.

3.  **Enable the Nginx configuration:**

    ```bash
    sudo ln -s /etc/nginx/sites-available/climb-grip-back /etc/nginx/sites-enabled/
    ```

4.  **Test the Nginx configuration:**

    ```bash
    sudo nginx -t
    ```

5.  **Restart Nginx:**

    ```bash
    sudo systemctl restart nginx
    ```

### 4. Obtain an SSL/TLS Certificate (Let's Encrypt):

1.  Run this command, replace `your_domain.com` by your domain :

    ```bash
    sudo certbot --nginx -d your_domain.com -d www.your_domain.com
    ```

    *   the certificate will be automatically generated, and the configuration file updated.
    *   It will ask if you want to redirect all HTTP traffic to HTTPS. **I recommend choosing to redirect** (option 2).
    *   Certbot sets up a cron job to automatically renew them.

### 5. Configure the firewall :

   ```bash
   sudo certbot --nginx -d your_domain.com -d www.your_domain.com
   ```

   ### 6. Access the application :

Access your application via `https://your_domain.com/`

### 7. Restart Gunicorn :

restart gunicorn to take the new parameters in consideration.

## Automated Deployment with GitHub Actions

This project uses GitHub Actions to automate the deployment process. The workflow is defined in `.github/workflows/deploy.yml`.

**Key Features:**

*   **Trigger:** The workflow is manually triggered using `workflow_dispatch`.
*   **Steps:**
    *   **Checkout code:** Checks out the code from the repository.
    *   **Create archive of repository:** Creates a compressed archive of the repository, excluding unnecessary files (.venv, .database, .git, .github).
    *   **Copy files to VPS:** Uses SCP to securely copy the archive to the VPS.
    *   **Extract files and restart application on VPS:** Uses SSH to connect to the VPS, extract the archive, install requirements and restart the application, including gunicorn and nginx.
*   **Secrets:** The workflow uses GitHub secrets (`VPS_HOST`, `VPS_USER`, `VPS_PASSWORD`) to securely manage VPS credentials.

**To use the deployment:**
- configure the three VPS secrets in your repository (Settings/Security/Secrets and variables/Actions)
- run the action by clicking the "run workflow" button in the "Actions" tab.

## Endpoints

The `webapi` module provides the following main endpoints:

- **GET /**: Returns a welcome message.
- **GET /climber/{climber_id}**: Retrieves a climber by their ID.
- **GET /climber**: Retrieves all climbers.
- **GET /test/climber/create-test**: Creates a test climber in the database.
- **GET /test/load-exemple-data**: creates multiple climbers and workouts from the files present in `data` directory
- **other endpoints**: other endpoints related to the different models (workouts, workout type etc) are available.

## License

This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for more details.