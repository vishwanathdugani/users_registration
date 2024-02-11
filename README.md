# README for User Authentication Service

## Overview

This repository contains a simple user authentication service built with FastAPI, designed to allow user registration, verification, and login. It uses SQLite for data persistence and Docker for easy deployment. The service is designed with simplicity in mind, following RESTful principles for easy integration with frontend services or as part of a microservice architecture.

## Getting Started

### Prerequisites

To run this project, you will need Docker installed on your machine.

### Running the Service

1. **Build the Docker Container**

   Navigate to the root directory of this project and run the following command to build the Docker container:

   ```sh
   docker-compose build
   ```

2. **Start the Service**

   Once the build is complete, start the service by running:

   ```sh
   docker-compose up
   ```

   This command starts the FastAPI server inside a Docker container, making the API accessible on `http://localhost:8000`.

## API Endpoints

The service exposes several endpoints for user management:

### Registration

- **POST** `/api/v1/users`

  Allows new users to register with an email and password.

  **Example Request:**

  ```json
  {
    "username": "user@example.com",
    "password": "yourpassword"
  }
  ```

  **Example Response:**

  ```json
  {
    "id": 1,
    "username": "user@example.com",
    "verified": false
  }
  ```

### Verification

- **POST** `/api/v1/verify-user`

  Simulates email verification by directly marking the user as verified.

  **Example Request:**

  ```json
  {
    "email": "user@example.com"
  }
  ```

  **Example Response:**

  ```json
  {
    "message": "User user@example.com has been verified"
  }
  ```

### Login

- **POST** `/api/v1/token`

  Authenticates a user and returns an access token.

  **Example Request:**

  ```http
  username=user@example.com&password=yourpassword
  ```

  **Example Response:**

  ```json
  {
    "access_token": "someaccesstoken",
    "token_type": "bearer"
  }
  ```

## Running Tests

To run the automated tests for this service, execute the following command:

```sh
docker-compose run web pytest
```

This will run all the tests defined in `tests.py` and generate a report in `report.html`.

## Future Improvements

- **Unit Tests**: Enhance the coverage of unit tests to include more scenarios and edge cases.
- **Asynchronous Tasks**: Implement asynchronous tasks for sending verification emails to provide a more realistic user registration flow.