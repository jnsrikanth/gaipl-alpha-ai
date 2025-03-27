cat main.py 
import os
import sys
import json
import re
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional, Union
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from glpi_api import GLPI
from glpi_config import GLPIConfig

# LangChain imports
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model definitions
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    metadata: Optional[Dict[str, Any]] = None
    source: str = "langchain"

# Initialize GLPI config
try:
    glpi_config = GLPIConfig()
    logger.info("GLPI configuration loaded successfully")
except ValueError as e:
    logger.error(f"Failed to load GLPI configuration: {e}")
    sys.exit(1)

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_llm():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    return Ollama(
        model="mistral",
        callback_manager=callback_manager,
        temperature=0.7
    )

async def handle_ticket_action(message: str, glpi_client: GLPI) -> str:
    """Handle ticket-related actions"""
    # Check for ticket creation intent
    if any(word in message.lower() for word in ["create", "new", "open"]):
        # Get priority from message
        priority = 3  # Default to normal priority
        if "high priority" in message.lower() or "urgent" in message.lower():
            priority = 4
        elif "low priority" in message.lower():
            priority = 2

        # Create ticket
        result = glpi_client.create_ticket_from_message(message, priority)
        if "error" not in result:
            return f"Created new ticket #{result.get('id')} successfully."
        else:
            return "Failed to create ticket: " + result["error"]

    # Check for ticket query intent
    elif any(word in message.lower() for word in ["show", "get", "find", "search"]):
        if "ticket #" in message.lower() or "#" in message:
            # Extract ticket number
            ticket_match = re.search(r'#(\d+)', message)
            if ticket_match:
                ticket_id = int(ticket_match.group(1))
                ticket = glpi_client.get_ticket_by_id(ticket_id)
                if ticket and not isinstance(ticket, dict):
                    return f"Ticket #{ticket_id}:\n" + \
                        f"Title: {ticket.get('name')}\n" + \
                        f"Status: {ticket.get('status')}\n" + \
                        f"Priority: {ticket.get('priority')}\n" + \
                        f"Description: {ticket.get('content')}"
                return f"Could not find ticket #{ticket_id}"

        # General ticket listing
        tickets = glpi_client.get_tickets()
        if tickets and isinstance(tickets, list):
            return "Recent tickets:\n" + "\n".join([
                f"#{t.get('id')}: {t.get('name')} ({t.get('status')})"
                for t in tickets[:5]
            ])

    return None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, llm: Any = Depends(get_llm)):
    try:
        history = "\n".join([
            f"{msg.role}: {msg.content}"
            for msg in request.history
        ]) if request.history else ""

        conversation_id = request.conversation_id or f"conv_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Handle ticket-related queries
        glpi_context = ""
        if any(word in request.message.lower() for word in ["ticket", "issue", "problem"]):
            config = glpi_config.get_config()
            client = GLPI(**config)
            if client.init_session():
                # Try to handle specific ticket action
                action_result = await handle_ticket_action(request.message, client)
                if action_result:
                    glpi_context = action_result
                else:
                    # Fall back to general ticket listing
                    tickets = client.get_tickets()
                    if tickets and isinstance(tickets, list):
                        glpi_context = "Recent tickets:\n" + "\n".join([
                            f"#{t.get('id')}: {t.get('name')} ({t.get('status')})"
                            for t in tickets[:5]
                        ])
                client.kill_session()

        # Create prompt with GLPI context
        template = """Assistant: I'm an IT support assistant with access to GLPI ticket system.
        
        GLPI Context: {glpi_context}
        Chat History: {history}
        User Message: {message}
        
        Keep responses brief and direct. If ticket information is available, reference it specifically."""

        prompt = PromptTemplate(
            template=template,
            input_variables=["glpi_context", "history", "message"]
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.invoke({
            "message": request.message,
            "history": history,
            "glpi_context": glpi_context or "No relevant ticket information found."
        })

        return ChatResponse(
            response=response["text"],
            conversation_id=conversation_id,
            metadata={
                "timestamp": datetime.now().isoformat(),
                "glpi_data": bool(glpi_context)
            }
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "glpi_config": "loaded" if glpi_config else "not loaded"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
