import aiohttp
import logging
import requests
import json
import zipfile
import io
import base64
import asyncio

from langgraph.utils.runnable import RunnableCallable, RunnableConfig
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ServerlessNode:
    """
    Represents a 'serverless' node on your backend. When called, it sends the
    current state to your backend (e.g., AWS Lambda) and returns the updated state.
    """

    def __init__(self, node_id: str, endpoint_url: str, api_key: str):
        """
        Args:
            node_id: Unique ID for the uploaded custom node on your platform.
            endpoint_url: The URL to invoke the serverless function (could be API Gateway).
            api_key: API key or token for authenticating with your backend.
        """
        self.node_id = node_id
        self.endpoint_url = endpoint_url
        self.api_key = api_key

    async def __call__(self, state: dict) -> dict:
        """
        Send the input `state` to the remote node code (AWS Lambda) and retrieve the updated state.
        Now properly async!
        """
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "node_id": self.node_id,
            "state": state
        }
        logger.debug(f"Invoking serverless node '{self.node_id}' with state keys: {list(state.keys())}")

        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint_url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Serverless node invocation failed: {error_text}")
                    raise Exception(f"Invocation failed with status code {response.status}")

                data = await response.json()
                updated_state = data.get("updated_state")
                if updated_state is None:
                    logger.error("Serverless node response did not contain 'updated_state'")
                    raise ValueError("Missing 'updated_state' in response.")

                logger.debug(f"Serverless node '{self.node_id}' returned updated state keys: {list(updated_state.keys())}")
                return updated_state


def create_serverless_node(node_id: str, endpoint_url: str, api_key: str) -> RunnableCallable:
    """
    Factory function that produces a langgraph RunnableCallable for your serverless node.
    """
    node = ServerlessNode(node_id, endpoint_url, api_key)

    def node_fn(state: Dict[str, Any], config: RunnableConfig | None = None) -> Dict[str, Any]:
        """Synchronous wrapper around async node execution"""
        async def _execute():
            try:
                response = await node(state)
                updated_state = response.get("updated_state", {})
                return {
                    "messages": updated_state.get("messages", [])
                }
            except Exception as e:
                logger.error(f"Node execution failed: {str(e)}")
                raise

        # Run the async function in the current event loop
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_execute())

    return RunnableCallable(
        func=node_fn,
        name=f"serverless_node_{node_id}"
    )


def upload_custom_node(
    node_code: str,
    metadata: dict,
    client_token: str,
    backend_url: str
) -> dict:
    """
    Upload a user's custom node code to your backend.

    The zip file should contain:
    - Your Python handler file
    - lambda_config.json specifying the handler details
    - Any additional dependencies
    """
    # Validate zip contains lambda_config.json
    try:
        zip_data = base64.b64decode(node_code)
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
            if "lambda_config.json" not in zip_file.namelist():
                raise ValueError("ZIP must contain lambda_config.json")

            # Read and validate config
            with zip_file.open("lambda_config.json") as config_file:
                config = json.load(config_file)

                required_fields = ["handler_file", "handler_function"]
                for field in required_fields:
                    if field not in config:
                        raise ValueError(f"lambda_config.json missing required field: {field}")

                # Verify handler file exists
                if config["handler_file"] not in zip_file.namelist():
                    raise ValueError(f"Handler file {config['handler_file']} not found in ZIP")

            # Validate directions if present
            if "directions" in metadata and not isinstance(metadata["directions"], str):
                raise ValueError("Directions must be a string")

    except (zipfile.BadZipFile, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid ZIP file or lambda_config.json: {str(e)}")

    # Add config to metadata for backend processing
    metadata["lambda_config"] = config

    # Continue with existing upload logic
    headers = {
        "Authorization": f"Bearer {client_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "node_code": node_code,
        "metadata": metadata,
    }

    logger.debug(f"Uploading custom node with metadata keys: {list(metadata.keys())}")

    response = requests.post(f"{backend_url}/api/nodes/upload", json=payload, headers=headers)

    if response.status_code != 200:
        logger.error(f"Node upload failed: {response.text}")
        raise Exception(f"Node upload failed with HTTP {response.status_code}: {response.text}")

    data = response.json()
    logger.debug(f"Upload successful. Response keys: {list(data.keys())}")

    # data should at least contain { "node_id", "endpoint_url", "api_key" }
    return data
