# Simple sample Flask App with Google Login

This is a Flask application that implements Google OAuth2 for user authentication. The application provides protected routes that require users to be authenticated via Google.


## Getting Started

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine:

- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)


### Configuration

Place the `client_secret.json` file in the root directory of your project. Ensure that the file contains your Google OAuth2 credentials.

### Build and run the Docker containers
To run the application, use the following command:
- docker-compose up --build


## Usage

### 1. **Home - /**
Homepage with a login button.


### 2. **Login - /login**
Redirects the user to Google OAuth2 login.


### 3. **Protected area - /protected_area**
A protected route that displays the user's Google profile information.


### 4. **List users -/users**
Lists all users stored in the database. Requires authentication


### 5. **Logout**
Logs out the user and clears the session.


## Contact
- For any inquiries, please contact Nicolas Hurtado at nicolashurtado0712@gmail.com

***Nicolas Hurtado C***