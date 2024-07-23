## Introduction

This project contains the source code for the HVAC-Millionaire Support Bot. The bot is designed to help users with common questions and issues related to the HVAC-Millionaire app. Additionally, the bot can also book appointments and create opportunities based on user request.

This repository contains both the backend and frontend code. The backend is developed using FastAPI while the frontend is developed using a standard HTML/CSS/JS stack.

## File Structure
The backend code can be located in the `app` directory. This also contains the `requirements.txt` file as well as the Dockerfile of the backend application.
The frontend code can be located in the `src` directory.

## Installation

This project also contains a `docker-compose.yml` file which can be used to run the entire application in a single command. First a `.env` file will have to be initialized in the root directory of the project. The `.env` file should contain the following environment variables:

```bash
# .env
CLIENT_ID
CLIENT_SECRET
LOCATION_ID
OPENAI_API_KEY
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
URL
PORT 
```

The backend makes use of a PostgreSQL database to store the refresh and access tokens for API usage. 

After the `.env` file has been setup, run the application and the database, simply run the following command:

```bash
docker-compose up --build -d
```

If VS-Code is being used, the frontend can be run using the pre-installed Live Server extension, which will run the frontend on `localhost:5500`. To do so, simply right-click on the `index.html` file and select `Open with Live Server`, or click on the `Go Live` button at the bottom right of the window.

Once the application is running, the frontend can be accessed at `localhost:5500` and the backend can be accessed at `localhost:3000`. To check whether the backend is running, navigate to `localhost:3000/` in a browser. If the backend is running, a JSON response should be displayed.

### Setting up Access Token in Database

After the docker container is running, the access token and refresh token can be set up using the backend itself. It is recommended to use Postman and send a POST request to the `/initialize_token` endpoint with the following JSON body:

```json
{
    "refresh_token": "value of refresh token",
}
```

This will store the refresh token in the database and generate an access token which can be used to make requests to the backend. Once 20 hours are up, the backend will automatically refresh the access token using the refresh token stored in the database.

This command can also be run using the following bash command:

```bash
$body = '{"refresh_token": "xxxx"}'  # Replace "xxxx" with your actual refresh token
$url = 'http://localhost:3000/initialize_tokens'

Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType 'application/json'
```

## Usage

Once the application has been setup and the access token has been initialized, the frontend can be used to interact with the backend. The frontend contains a chatbot which can be used to interact with the backend. The chatbot can be used to ask questions, book appointments, and create opportunities.