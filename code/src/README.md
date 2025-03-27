# GLPI-based System with FastAPI and React

## Project Overview
This project is a comprehensive IT asset and service management system built on GLPI (Gestionnaire Libre de Parc Informatique), integrating a modern FastAPI backend and React frontend with integrated chat functionality. The system provides a robust platform for managing IT assets, tickets, and service requests while offering real-time communication capabilities.

## System Architecture
The system follows a microservices architecture pattern, with distinct services containerized using Docker:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  React Frontend ├────►│  FastAPI Backend├────►│  GLPI Core      │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────┬───────┴───────────────┬──────┘
                         │                       │
                   ┌─────▼─────┐           ┌─────▼─────┐
                   │           │           │           │
                   │  MariaDB  │           │  RabbitMQ │
                   │           │           │           │
                   └───────────┘           └───────────┘
```

- **Frontend**: React-based SPA for user interaction
- **Backend**: FastAPI providing REST APIs and WebSocket support
- **Database**: MariaDB for data persistence
- **Message Broker**: RabbitMQ for asynchronous processing and real-time messaging
- **Core**: GLPI as the foundation for IT asset management

## Components Description

### GLPI Core
The GLPI (Gestionnaire Libre de Parc Informatique) serves as the core engine, providing inventory management, ticketing, and service catalog capabilities. It offers a comprehensive ITIL-compliant service management framework.

### FastAPI Backend
A modern Python-based API service that extends GLPI functionality with custom business logic and serves as an integration layer between the frontend and GLPI core. It provides:
- RESTful API endpoints
- WebSocket support for real-time chat functionality
- Authentication and authorization
- Custom business logic implementation

### React Frontend
A responsive and intuitive user interface built with React, providing:
- Modern and accessible UI for GLPI functionality
- Real-time chat and notifications
- Dashboard and reporting views
- Mobile-friendly design

### MariaDB
Database server that stores both GLPI data and application-specific data.

### RabbitMQ
Message broker used for:
- Asynchronous task processing
- Real-time messaging for the chat system
- Event-driven architecture support

### Redis
In-memory data store used for:
- Caching
- Session management
- Temporary data storage

### Traefik
Reverse proxy and load balancer handling:
- Routing
- SSL/TLS termination
- Service discovery

## Prerequisites
- Docker (version 20.10.x or later)
- Docker Compose (version 2.x or later)
- Git
- Minimum 4GB RAM
- 20GB available disk space

## Installation Instructions

### Clone the Repository
```bash
git clone https://github.com/your-organization/glpi-system.git
cd glpi-system
```

### Configure Environment Variables
1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file to configure your environment variables (see Environment Variables section below).

### Start the Services
```bash
docker-compose up -d
```

### Initialize the Database
```bash
docker-compose exec glpi php bin/console db:install
```

### Create Admin User
```bash
docker-compose exec glpi php bin/console user:create --admin username password "Admin User" admin@example.com
```

### Access the Application
- GLPI UI: http://localhost:8080
- Modern UI: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## Environment Variables

### Core Configuration
- `GLPI_DOMAIN`: Domain name for GLPI (default: localhost)
- `DB_HOST`: Database host (default: db)
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name (default: glpi)

### API Configuration
- `API_SECRET_KEY`: Secret key for JWT token generation
- `API_DEBUG`: Enable debug mode (true/false)
- `API_CORS_ORIGINS`: Allowed CORS origins

### Frontend Configuration
- `REACT_APP_API_URL`: URL for backend API
- `REACT_APP_WEBSOCKET_URL`: URL for WebSocket connection
- `REACT_APP_TITLE`: Application title

### Email Configuration
- `SMTP_HOST`: SMTP server host
- `SMTP_PORT`: SMTP server port
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `MAIL_FROM`: Default sender email address

## Usage

### Admin Dashboard
Access the admin dashboard at `/admin` to:
- Manage users and permissions
- Configure system settings
- View system logs and status

### Asset Management
Navigate to `/assets` to:
- Add, update, and track hardware and software assets
- Manage asset lifecycles
- Generate inventory reports

### Ticketing System
Access the ticketing system at `/tickets` to:
- Create and manage support tickets
- Track issue resolution
- Set up SLAs and escalation paths

### Chat Functionality
The integrated chat system allows:
- Real-time communication between users
- Ticket-related discussions
- File sharing and notifications

## Development Setup

### Local Development Environment
1. Install development dependencies:
```bash
npm install # Frontend dependencies
pip install -r requirements-dev.txt # Backend dependencies
```

2. Start development servers:
```bash
# Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Linting and Formatting
```bash
# Backend
cd backend
flake8 .
black .

# Frontend
cd frontend
npm run lint
npm run format
```

### Building for Production
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Troubleshooting
Common issues and their solutions:

1. **Database connection errors**:
   - Check if database service is running
   - Verify database credentials in `.env` file

2. **Permission issues**:
   - Ensure proper volume permissions
   - Run `docker-compose exec glpi chmod -R 775 /var/www/html/files`

3. **Service unavailable**:
   - Check service logs: `docker-compose logs [service_name]`
   - Verify network connectivity between containers

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

