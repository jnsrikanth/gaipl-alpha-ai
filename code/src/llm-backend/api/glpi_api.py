import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

class GLPI:
    def __init__(self, url: str, apptoken: str, usertoken: str):
        self.url = url
        self.app_token = apptoken
        self.user_token = usertoken
        self.session_token = None
        self.headers = {
            'App-Token': self.app_token,
            'Authorization': f'user_token {self.user_token}'
        }

    def init_session(self) -> bool:
        """Initialize a session with GLPI"""
        try:
            response = requests.get(
                f"{self.url}/initSession",
                headers=self.headers
            )
            response.raise_for_status()
            self.session_token = response.json().get('session_token')
            if self.session_token:
                self.headers['Session-Token'] = self.session_token
                logging.info("Session initialized successfully")
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to initialize GLPI session: {e}")
            return False

    def kill_session(self) -> bool:
        """Kill the current session"""
        if not self.session_token:
            return True
        try:
            response = requests.get(
                f"{self.url}/killSession",
                headers=self.headers
            )
            response.raise_for_status()
            self.session_token = None
            return True
        except Exception as e:
            logging.error(f"Failed to kill GLPI session: {e}")
            return False

    def create_ticket(self, data: Dict) -> Dict:
        """Create a new ticket"""
        if not self.session_token:
            return {"error": "No active session"}

        try:
            # Make sure data is formatted correctly
            ticket_data = data
            if 'input' not in ticket_data:
                ticket_data = {'input': data}

            logging.info(f"Creating ticket with data: {ticket_data}")
            response = requests.post(
                f"{self.url}/Ticket",
                headers=self.headers,
                json=ticket_data
            )
            response.raise_for_status()
            
            if not response.content:
                return {"error": "Empty response from server"}
                
            result = response.json()
            logging.info(f"Create ticket result: {result}")
            return result
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error creating ticket: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response content: {e.response.content}")
            return {"error": str(e)}
        except Exception as e:
            logging.error(f"Error creating ticket: {e}")
            return {"error": str(e)}

    def create_ticket_from_message(self, message: str, priority: int = 3) -> Dict:
        """Create a ticket from a user message"""
        try:
            # Extract location if mentioned
            location = None
            if "room" in message.lower():
                room_match = re.search(r'room\s+(\d+)', message.lower())
                if room_match:
                    location = int(room_match.group(1))

            # Extract category based on keywords
            category = 0  # Default category
            if any(word in message.lower() for word in ["printer", "printing", "scanner"]):
                category = 1  # Printers & Scanners
            elif any(word in message.lower() for word in ["monitor", "screen", "display"]):
                category = 2  # Monitors & Displays
            elif any(word in message.lower() for word in ["network", "internet", "wifi", "connection"]):
                category = 3  # Network

            # Create ticket data
            title = message[:50] + ('...' if len(message) > 50 else '')
            ticket_data = {
                'name': title,
                'content': message,
                'priority': priority,
                'type': 1,  # Incident
                'status': 1,  # New
                'itilcategories_id': category
            }

            # Add location if found
            if location:
                ticket_data['locations_id'] = location

            logging.info(f"Creating ticket with data: {ticket_data}")
            result = self.create_ticket(ticket_data)
            logging.info(f"Create ticket result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error creating ticket from message: {e}")
            return {"error": str(e)}

    def get_tickets(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get tickets based on filters"""
        if not self.session_token:
            return []
        try:
            params = {'expand_dropdowns': True}
            if filters:
                params.update(filters)
            
            response = requests.get(
                f"{self.url}/Ticket",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching tickets: {e}")
            return []

    def get_ticket_by_id(self, ticket_id: int) -> Dict:
        """Get a specific ticket by ID"""
        if not self.session_token:
            return {}
        try:
            response = requests.get(
                f"{self.url}/Ticket/{ticket_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching ticket {ticket_id}: {e}")
            return {}

    def update_ticket(self, ticket_id: int, data: Dict) -> Dict:
        """Update an existing ticket"""
        if not self.session_token:
            return {"error": "No active session"}
        try:
            response = requests.put(
                f"{self.url}/Ticket/{ticket_id}",
                headers=self.headers,
                json={'input': data}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error updating ticket {ticket_id}: {e}")
            return {"error": str(e)}
