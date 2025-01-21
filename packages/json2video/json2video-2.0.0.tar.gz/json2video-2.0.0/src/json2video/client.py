"""
JSON2Video SDK v2.0

Author: JSON2Video.com
Description: SDK for creating videos programmatically using JSON2Video API

GET YOUR FREE APIKey at https://json2video.com/get-api-key/
CHECK DOCUMENTATION at: https://json2video.com/docs/
"""

import json
import time
from typing import Any, Dict, List, Optional, Union
import requests


class Base:
    """Base class for Scene and Movie classes."""

    def __init__(self):
        """Initialize base object with empty properties."""
        self.object: Dict[str, Any] = {}
        self.properties: List[str] = []

    def set(self, property_name: str, value: Any) -> None:
        """Set a property for the Scene or Movie.

        Args:
            property_name: Name of the property to set
            value: Value to set for the property

        Raises:
            ValueError: If the property doesn't exist
        """
        property_name = property_name.lower().replace('_', '-')
        if property_name in self.properties:
            self.object[property_name] = value
        else:
            raise ValueError(f"Property {property_name} does not exist")

    def add_element(self, element: Optional[Dict[str, Any]] = None) -> bool:
        """Add a new element to the Scene or Movie.

        Args:
            element: Dictionary containing element properties

        Returns:
            bool: True if element was added successfully
        """
        if element and isinstance(element, dict):
            if "elements" not in self.object:
                self.object["elements"] = []
            self.object["elements"].append(element)
            return True
        return False

    def get_json(self) -> str:
        """Return the data object as a JSON string.

        Returns:
            str: JSON string representation of the object
        """
        return json.dumps(self.object, indent=2)

    def get_object(self) -> Dict[str, Any]:
        """Return the data object.

        Returns:
            Dict[str, Any]: The internal object
        """
        return self.object


class Scene(Base):
    """Scene class for creating video scenes."""

    def __init__(self):
        """Initialize Scene with its specific properties."""
        super().__init__()
        self.properties = ['comment', 'background-color', 'duration', 'cache']

    def set_transition(
        self,
        style: Optional[str] = None,
        duration: Optional[float] = None,
        transition_type: Optional[str] = None
    ) -> None:
        """Set the transition style for this scene.

        Args:
            style: Transition style
            duration: Transition duration
            transition_type: Type of transition
        """
        if any(param is not None for param in [style, duration, transition_type]):
            if "transition" not in self.object:
                self.object["transition"] = {}
            if style is not None:
                self.object["transition"]["style"] = style
            if duration is not None:
                self.object["transition"]["duration"] = duration
            if transition_type is not None:
                self.object["transition"]["type"] = transition_type


class Movie(Base):
    """Movie class for creating and managing video projects."""

    def __init__(self):
        """Initialize Movie with its specific properties."""
        super().__init__()
        self.properties = [
            'comment', 'draft', 'width', 'height', 'resolution',
            'exports', 'quality', 'fps', 'cache', 'template',
            'variables', 'id'
        ]
        self.api_url = 'https://api.json2video.com/v2/movies'
        self.apikey = None

    def set_api_key(self, apikey: str) -> None:
        """Set the API key for authentication.

        Args:
            apikey: Your JSON2Video API key
        """
        self.apikey = apikey

    def add_scene(self, scene: Optional[Scene] = None) -> bool:
        """Add a new scene to the Movie.

        Args:
            scene: Scene object to add

        Returns:
            bool: True if scene was added successfully

        Raises:
            ValueError: If scene is invalid
        """
        if scene:
            if "scenes" not in self.object:
                self.object["scenes"] = []
            self.object["scenes"].append(scene.get_object())
            return True
        raise ValueError("Invalid scene")

    def _make_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: API endpoint URL
            data: Request payload
            headers: Request headers

        Returns:
            Dict[str, Any]: API response

        Raises:
            requests.RequestException: If the request fails
        """
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data if data else None,
                headers=headers or {}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "status": 500,
                "success": False,
                "message": "Unknown SDK error",
                "error": str(e)
            }

    async def render(self) -> Dict[str, Any]:
        """Start a new rendering job.

        Returns:
            Dict[str, Any]: API response

        Raises:
            ValueError: If API key is invalid
        """
        if not self.apikey:
            raise ValueError("Invalid API Key")

        response = self._make_request(
            method="POST",
            url=self.api_url,
            data=self.object,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.apikey
            }
        )

        if response.get("success") and "project" in response:
            self.object["project"] = response["project"]

        return response

    def get_status(self, project: Optional[str] = None) -> Dict[str, Any]:
        """Get the current project rendering status.

        Args:
            project: Project ID (optional, uses stored project ID if not provided)

        Returns:
            Dict[str, Any]: API response

        Raises:
            ValueError: If API key or project ID is invalid
        """
        if not self.apikey:
            raise ValueError("Invalid API Key")

        project = project or self.object.get("project")
        if not project:
            raise ValueError("Project ID not set")

        url = f"{self.api_url}?project={project}"
        return self._make_request(
            method="GET",
            url=url,
            headers={"x-api-key": self.apikey}
        )

    def wait_to_finish(self, callback: Optional[callable] = None) -> Dict[str, Any]:
        """Wait for the current project to finish rendering.

        Args:
            callback: Optional callback function to receive status updates

        Returns:
            Dict[str, Any]: Final API response
        """
        while True:
            response = self.get_status()
            
            if callback:
                callback(response)

            if not response.get("success"):
                return response

            if "movie" in response and response["movie"]["status"] == "done":
                return response

            time.sleep(5)  # Check every 5 seconds 