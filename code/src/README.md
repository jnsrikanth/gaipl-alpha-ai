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
A modern Python-based API service located in `IPE-AI/llm-backend/api/` that extends GLPI functionality with custom business logic and serves as an integration layer between the frontend and GLPI core. It provides:
- RESTful API endpoints with automatic OpenAPI documentation
- WebSocket support for real-time chat functionality
- Authentication and authorization with JWT token handling
- Custom business logic implementation
- Integration with Ollama for AI-powered assistance
- Asynchronous processing capabilities
- Database abstraction with SQLAlchemy and Pydantic models
- Middleware for request processing, CORS handling, and error management
- Environment-based configuration system
- Comprehensive logging and monitoring

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
- Containerized deployment for consistent environment across installations
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

## Project Structure

The project repository is organized into modular components with a clear separation of concerns:

```
glpi-system/
├── docker-compose.yml              # Main Docker Compose configuration
├── docker-compose.prod.yml         # Production-specific configurations
├── .env.example                    # Example environment variables
├── README.md                       # Project documentation
├── generate_incidents.py           # Script to generate test incidents
├── generate_changes.py             # Script to generate test changes
├── glpi/                           # GLPI core files
│   ├── Dockerfile                  # GLPI container configuration
│   ├── config/                     # GLPI configuration files
│   └── plugins/                    # GLPI plugin directory
├── IPE-AI/
│   ├── llm-backend/                # LLM backend directory
│   │   ├── api/                    # FastAPI backend service
│   │   │   ├── main.py             # FastAPI entry point
│   │   │   ├── endpoints/          # API endpoints definition
│   │   │   ├── models/             # Data models and schemas
│   │   │   ├── controllers/        # Business logic controllers
│   │   │   ├── services/           # Service implementations
│   │   │   ├── utils/              # Utility functions
│   │   │   ├── middleware/         # API middleware components
│   │   │   └── tests/              # Backend unit tests
│   │   ├── venv/                   # Python virtual environment
│   │   └── requirements.txt        # Python dependencies
├── frontend/                       # React frontend application
│   ├── Dockerfile                  # Frontend container configuration
│   ├── src/                        # React source code
│   ├── public/                     # Static assets
│   └── package.json                # Node.js dependencies
├── chatbot-react-app/              # Chat UI component
│   ├── Dockerfile                  # Chat UI container configuration
│   ├── src/                        # Chat application source code
│   └── package.json                # Chat UI dependencies
├── IPE-AI/                         # AI core functionality
│   ├── Dockerfile                  # AI service container configuration
│   ├── app/                        # AI service code
│   │   ├── main.py                 # AI service entry point
│   │   ├── models/                 # AI model definitions
│   │   ├── services/               # AI services
│   │   └── utils/                  # Utility functions
│   └── requirements.txt            # AI Python dependencies
├── integrated-experience/          # Integration layer for UX/AI
│   ├── Dockerfile                  # Integration service configuration
│   ├── app/                        # Integration service code
│   │   ├── connectors/             # Service connectors
│   │   └── orchestrators/          # Service orchestration 
│   └── requirements.txt            # Integration dependencies
├── ollama/                         # Ollama service for AI model hosting
│   ├── Dockerfile                  # Ollama container configuration
│   ├── models/                     # Pre-downloaded models
│   └── config/                     # Ollama configuration
└── langchain/                      # LangChain integration service
    ├── Dockerfile                  # LangChain container configuration
    ├── app/                        # LangChain application code
    │   ├── main.py                 # LangChain service entry point
    │   ├── chains/                 # LangChain chain definitions
    │   ├── memory/                 # Conversation memory components
    │   ├── tools/                  # Custom LangChain tools
    │   └── embeddings/             # Vector embedding utilities
    └── requirements.txt            # LangChain Python dependencies
```

### Docker Service Configuration

All services are containerized with Docker and orchestrated using Docker Compose:

1. **GLPI (`glpi`)**
   - Base Image: `php:8.1-apache`
   - Ports: `8080:80`
   - Volumes: GLPI files, configurations
   - Dependencies: MariaDB

2. **FastAPI Backend (`fastapi`)**
   - Base Image: `python:3.10-slim`
   - Ports: `8000:8000` 
   - Volumes: Application code from `IPE-AI/llm-backend/api/`
   - Dependencies: MariaDB, RabbitMQ, Ollama
   - Features:
     - Automatic API documentation (Swagger UI and ReDoc)
     - Type-validated request/response models
     - Dependency injection system
     - Background task processing

3. **React Frontend (`frontend`)**
   - Base Image: `node:18-alpine`
   - Ports: `3000:3000`
   - Volumes: Source code
   - Dependencies: Backend API

4. **Chat UI (`chatbot-react-app`)**
   - Base Image: `node:18-alpine`
   - Ports: `5173:5173`
   - Volumes: Source code
   - Dependencies: Backend API, WebSocket connections

5. **MariaDB (`db`)**
   - Image: `mariadb:10.6`
   - Ports: `3306:3306`
   - Volumes: Database data
   - Environment: Database credentials

6. **RabbitMQ (`rabbitmq`)**
   - Image: `rabbitmq:3-management`
   - Ports: `5672:5672` (AMQP), `15672:15672` (Management)
   - Volumes: Message queue data

7. **Ollama (`ollama`)**
   - Custom Dockerfile based on `ollama/ollama:latest`
   - Ports: `11434:11434`
   - Volumes:
     - `./ollama/models:/root/.ollama/models` (persisted models)
     - `./ollama/config:/etc/ollama` (configuration)
   - GPU Support: Optional NVIDIA GPU passthrough with runtime configuration
   - Environment variables for model configuration and resource allocation
8. **LangChain Service (`langchain`)**
   - Base Image: `python:3.10-slim`
   - Ports: `7000:7000`
   - Volumes: Application code
   - Dependencies: Ollama, Backend API

### Component Relationships

The system components interact in the following ways:
1. **Frontend → Backend**: React frontend communicates with FastAPI backend via REST APIs
2. **Backend → GLPI**: Backend interacts with GLPI through its API
3. **Chat UI → Backend**: Chat application connects to WebSocket endpoints on the backend
4. **Backend → RabbitMQ**: Backend publishes and consumes messages for async processing
5. **LangChain → Ollama**: LangChain queries Ollama for AI model inference
6. **LangChain → Backend**: LangChain provides AI capabilities to the backend
7. **Backend → Ollama**: FastAPI backend directly interfaces with Ollama for AI processing
6. **LangChain → Backend**: LangChain provides AI capabilities to the backend
7. **IPE-AI ↔ integrated-experience**: AI core services integrate with UX components

### AI Components

The AI functionality is provided by three interconnected components:

1. **IPE-AI Directory**
   - Core AI functionality and model interfaces
   - Processes natural language requests
   - Handles model inference and response generation
   - Manages AI session contexts

2. **integrated-experience Directory**
   - Integration layer between AI and user experience
   - Orchestrates the flow of information between components
   - Provides contextual awareness for AI responses
   - Manages user sessions and preferences

3. **chatbot-react-app Directory**
   - User interface for conversational AI interaction
   - Renders chat messages and responses
   - Handles user input and commands
   - Provides real-time communication through WebSockets

### AI Components Setup

To set up the AI components:

1. **Configure Ollama**:
   - Models are automatically downloaded on first use and persisted to the `ollama/models` volume
   - Configure model preferences in `ollama/config/ollama.json`
   - Customize the Ollama container via the `ollama/Dockerfile` for specific requirements
   - GPU acceleration can be enabled in `docker-compose.yml` by setting appropriate runtime configurations
   - Adjust memory and CPU allocations in the `docker-compose.yml` file according to your model requirements
   - For detailed Ollama configuration and usage, refer to the dedicated documentation in [`ollama/README.md`](ollama/README.md)

   #### Mistral Model Setup
   
   This project primarily uses the Mistral model for AI capabilities, which offers an excellent balance between performance and resource efficiency:
   
   - **Model Name**: Mistral (mistral:7b)
   - **Parameter Size**: 7 billion parameters
   - **Available Quantization Options**:
     - `mistral:7b` (full precision)
     - `mistral:7b-q4_0` (4-bit quantized, recommended for most deployments)
     - `mistral:7b-q4_K_M` (4-bit quantized with key/value cache in fp16)
   - **Context Length**: 8,192 tokens
   - **Resource Requirements**:
     - Full precision: ~16GB RAM
     - 4-bit quantized: ~5-8GB RAM
     - Disk Space: ~4-5GB (depending on quantization)
   - **License**: Apache 2.0

   #### Pulling the Mistral Model
   
   The Docker setup will attempt to pull the model automatically on startup, but you can also pull it manually:

   ```bash
   # From your host system
   docker-compose exec ollama ollama pull mistral:7b-q4_0
   ```

   #### Common Mistral Model Issues

   - **Out of Memory Errors**: If you encounter OOM errors, try using the quantized version (`mistral:7b-q4_0`) and increase container memory limits in `docker-compose.yml`
   - **Slow First Response**: The first request may be slow as the model loads into memory; subsequent requests will be faster
   - **Model Loading Failures**: Ensure sufficient disk space and verify model files aren't corrupted
2. **Configure LangChain**:
   - Set up environment variables for model selection and parameters
   - Configure memory components for conversation history
   - Set vector store path for embedded knowledge bases

3. **Integrate with Backend**:
   - Add API keys to the `.env` file
   - Connect backend services to LangChain endpoints
   - Set up WebSocket connections for real-time AI responses

4. **FastAPI Backend Configuration**:
   - Located in `IPE-AI/llm-backend/api/`
   - Handles the HTTP API and WebSocket interfaces
   - Implements the controller layer between frontend and AI components
   - Configurable through environment variables in the `.env` file
   - Key components:
     - **endpoints/** - API route definitions and handlers
     - **models/** - Pydantic data models for request/response validation
     - **services/** - Business logic and external service integrations
     - **controllers/** - Orchestration of service components
     - **middleware/** - Request/response processing middleware

4. **Configure Knowledge Base** (optional):
   - Place documentation in `langchain/app/knowledge`
   - Run embedding generation: `docker-compose exec langchain python -m app.embeddings.generate`
   - Configure retrieval parameters in the `.env` file

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
- `OLLAMA_CONCURRENCY`: Number of concurrent requests Ollama can handle (default: 2)
- `OLLAMA_GPU_ENABLED`: Enable GPU acceleration for Ollama (true/false)
- `OLLAMA_MODEL_PATH`: Custom path for model storage (default: /root/.ollama/models)
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
cd IPE-AI/llm-backend/api
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

### Running Tests
```bash
# Backend tests
cd IPE-AI/llm-backend/api
pytest

# Frontend tests
cd frontend
npm test
```

### Code Linting and Formatting
```bash
# Backend
cd IPE-AI/llm-backend/api
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
