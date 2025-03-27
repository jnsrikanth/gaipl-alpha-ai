cat README.md 
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
                         │                       │
                   ┌─────▼─────┐           ┌─────▼─────┐
                   │           │           │           │
                   │  Ollama   │◄──────────┤ LangChain │
                   │           │           │           │
                   └───────────┘           └───────────┘
```

- **Frontend**: React-based SPA for user interaction
- **Backend**: FastAPI providing REST APIs and WebSocket support
- **Database**: MariaDB for data persistence
- **Message Broker**: RabbitMQ for asynchronous processing and real-time messaging
- **Core**: GLPI as the foundation for IT asset management
- **Ollama**: Local AI model hosting and inference service
- **LangChain**: Framework for developing applications powered by language models

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

## AI Integration

The system integrates advanced AI capabilities through Ollama and LangChain, enhancing the user experience and automation capabilities.

### Ollama

Ollama provides local AI model hosting and inference capabilities:
- Runs large language models locally for enhanced privacy and reduced latency
- Supports multiple open-source models (Llama 2, Mistral, Vicuna, etc.)
- Processes natural language queries and generates contextual responses
- Integrates with the FastAPI backend to provide AI-powered assistance

### LangChain

LangChain is a framework for developing applications powered by language models:
- Connects the system with Ollama's language models
- Enables context-aware conversations through memory components
- Provides tools for document retrieval and knowledge base integration
- Powers advanced features like:
  - Intelligent ticket categorization and routing
  - Automated response suggestions
  - Knowledge extraction from technical documentation
  - Conversational interfaces for system interaction

### Enhanced System Capabilities

The AI integration delivers significant enhancements:
- **Natural Language Processing**: Users can interact with the system using natural language
- **Automated Assistance**: AI-powered recommendations for ticket resolution
- **Knowledge Management**: Improved information retrieval and insight generation
- **User Experience**: Conversational interfaces that simplify complex tasks
- **Operational Efficiency**: Reduced manual effort through AI-assisted workflows

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

## Data Generation Scripts

The system includes powerful scripts for generating realistic test data to populate your GLPI instance with cloud infrastructure-related incidents and changes.

### generate_incidents.py

This script generates simulated cloud infrastructure incidents with realistic attributes:

- Creates randomized incident tickets related to cloud services
- Simulates issues with AWS, Azure, GCP, and other cloud providers
- Generates diverse incident categories (outages, performance issues, security alerts)
- Populates tickets with detailed descriptions, priorities, and impact levels
- Assigns realistic timestamps and statuses to incidents

### generate_changes.py

This script creates simulated change requests for cloud infrastructure:

- Produces change tickets for cloud resource modifications
- Generates various change types (planned maintenance, updates, scaling operations)
- Creates realistic change approval workflows and implementation plans
- Simulates different risk levels and change categories
- Adds appropriate planning and execution timeframes

### Usage

To generate test data, run the following commands:

```bash
# Generate sample incidents (default: 50 incidents)
python generate_incidents.py --count 100

# Generate sample changes (default: 30 changes)
python generate_changes.py --count 50
```

Additional options:
```bash
# Set date range for generated data
python generate_incidents.py --start-date 2023-01-01 --end-date 2023-12-31

# Specify urgency distribution
python generate_changes.py --high-urgency-percent 20 --medium-urgency-percent 50
```

These scripts are valuable for:
- Creating realistic test environments
- Demonstrating system capabilities
- Testing reporting and dashboard features
- Training users on ticket handling procedures

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

### AI Configuration
- `OLLAMA_BASE_URL`: URL for the Ollama service (default: http://ollama:11434)
- `OLLAMA_MODEL`: Default AI model to use (default: llama2)
- `LANGCHAIN_VERBOSE`: Enable verbose logging for LangChain (true/false)
- `LANGCHAIN_MEMORY_TYPE`: Type of memory to use (default: conversation_buffer)
- `EMBEDDING_MODEL`: Model to use for embeddings (default: sentence-transformers/all-mpnet-base-v2)
- `VECTOR_STORE_PATH`: Path to store vector embeddings (default: ./vector_store)

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
