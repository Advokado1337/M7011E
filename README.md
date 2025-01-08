


# Movie Website Project

This project is a Django-based web application for managing movies and reviews. It uses Docker for containerization, MySQL for the database, and Pytest for running tests. Below, you'll find all the necessary instructions to set up and run the project.

---

## Prerequisites

Before you start, ensure you have the following installed on your system:

- Docker: Used to containerize the application and manage dependencies.
- Docker Compose: To orchestrate multiple containers.
- MySQL: The database used for the project (handled via Docker).
- Pytest: For running unit tests.
- Postman For testing APIs.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Create a `.env` File

Create a `.env` file in the root directory with the following content:

```env
# Django settings
SECRET_KEY=your-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# MySQL settings
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=db
MYSQL_PORT=3306

# Users
ADMIN="name@example.com"
ADMINPASS='choicenewpassword'

# Google SSO settings
GOOGLE_CLIENT_ID=yourclientid
GOOGLE_CLIENT_SECRET=yourclientsecret
```

> **Note:** Ensure you replace placeholder values with your actual configuration.

### 3. Build and Run the Project

To set up the containers and start the application:

```bash
docker-compose up --build
```

This command will:

1. Build the Docker images for the project.
2. Start the Django application container.
3. Start the MySQL database container.

The Django application and the MySQL database are run in separate Docker containers. This ensures that the application and database are isolated but can communicate with each other using Docker networking. The configuration for these containers is defined in the `docker-compose.yml` file.

> **Access the application**: Open [http://localhost:8000](http://localhost:8000) (or the port configured in your `docker-compose.yml` file).

---

## Database Configuration

The MySQL database is managed via Docker. Configuration details (e.g., username, password, and database name) are stored in the `docker-compose.yml` and `.env` files. Ensure you update these files if required.

---

## API Testing

The application exposes several APIs that you can test. To explore and test the APIs:

1. Use tools such as [Postman](https://www.postman.com/) or cURL to send requests to the endpoints.

2. While the application is running, visit the Swagger documentation at:

   ```
   http://localhost:8000/swagger/
   ```

   This page provides a detailed overview of all available endpoints, their parameters, and responses. You can also test the APIs directly from the Swagger interface.

---

## Running Tests

The project uses Pytest for testing. To run the tests:

1. Ensure the containers are built and running using the previous commands.

2. Inside other terminal, run:

   ```bash
   python -m pytest
   ```

This will execute all tests and display the results.

---

## Clearing Docker Images

To clear all unused Docker images and containers, use:

```bash
docker system prune -a
```

⚠️ **Warning:** This will delete all stopped containers, unused networks, dangling images, and build cache.

---
