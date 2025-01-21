"""
HeadlessAgents Python Library

A Python library for interacting with headless agents through various AI providers.
"""

import requests
from typing import Dict, List, Any, Optional

class HeadlessAgent:
    """A class for interacting with headless agents."""
    
    BASE_URL = "https://agents-api-434678060995.us-central1.run.app"
    VALID_PROVIDERS = ["openai", "anthropic", "o1", "xai"]

    def __init__(self, agent_id: str, user_id: str, client_provider: str, base_url: Optional[str] = None):
        """
        Initialize a HeadlessAgent instance.

        Args:
            agent_id (str): The ID of the agent to interact with
            user_id (str): The user ID for authentication
            client_provider (str): The AI provider to use (openai, anthropic, o1, xai)
            base_url (str, optional): Custom base URL for API endpoints
        """
        self.agent_id = agent_id
        self.user_id = user_id
        
        if client_provider not in self.VALID_PROVIDERS:
            raise ValueError(f"Invalid client provider: {client_provider}. Must be one of {self.VALID_PROVIDERS}")
        self.client_provider = client_provider
        
        self.base_url = base_url or self.BASE_URL

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Get the tools available for the agent.

        Returns:
            List[Dict[str, Any]]: List of tool configurations
        """
        payload = {
            "agent_id": self.agent_id,
            "user_id": self.user_id,
            "client_provider": self.client_provider
        }
        
        response = requests.post(
            f"{self.base_url}/agents/v1/get_agent_with_formatted_tools",
            json=payload
        )
        response.raise_for_status()
        return response.json()["tools"]

    def query(self, query: str) -> Dict[str, Any]:
        """
        Send a query to the agent.

        Args:
            query (str): The query to send to the agent

        Returns:
            Dict[str, Any]: The agent's response
        """
        payload = {
            "agent_id": self.agent_id,
            "query": query,
            "user_id": self.user_id
        }
        
        response = requests.post(
            f"{self.base_url}/agents/v1/query/{self.client_provider}",
            json=payload
        )
        response.raise_for_status()
        return response.json()

# Version of the package
__version__ = "0.1.0" 