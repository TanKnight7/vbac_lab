import asyncio
from mcp.server.fastmcp import FastMCP
import requests
from database import get_db, RoleRepository, AccountRepository, CookieRepository, APIEndpointRepository, ScenarioRepository, FindingRepository
from typing import Any, Dict, Optional, Union
import os
mcp = FastMCP("Vertical Broken Access Control (VBAC) Tools")

@mcp.tool()
async def fetch_api(url: str, method: str, headers: dict, body: dict = {}, timeout: int = 60, allow_redirects: bool = False) -> str:
    """Makes a request to the given URL with the given method, headers and body.
    Args:
        url: The URL to make the request to.
        method: The method to use for the request.
        headers: The headers to send with the request.
        body: The body to send with the request.
        timeout: The timeout for the request.
        allow_redirects: Whether to allow redirects.
    Returns:
        Response from the request.
        - Status Code: The status code of the response.
        - Headers: The headers of the response.
        - Cookies: The cookies of the response.
        - Response: The response body.
    """
    

    content_types = {
        'application/json': {'json': body},
        'application/x-www-form-urlencoded': {'data': body},
        'multipart/form-data': {'files': body},
    }
    
    content_type = content_types.get(headers.get('Content-Type'), {'data': body})
    
    if method == "GET": # GET requests
        response = requests.get(url, headers=headers, timeout=timeout, verify=False, allow_redirects=allow_redirects)
    elif not headers.get('Content-Type'): # No content type, Assuming no body.
        response = requests.request(method, url, headers=headers, timeout=timeout, verify=False, allow_redirects=allow_redirects)
    else: # Has content type, send body accordingly.
        response = requests.request(method, url, headers=headers, **content_type, timeout=timeout, verify=False, allow_redirects=allow_redirects)
    
    
    return f"""Status Code: {response.status_code}
    Headers: {response.headers}
    Cookies: {response.cookies}
    Response: {response.text}
    """

@mcp.tool()
async def database_crud(model: str, action: str, data: dict = {}, filters: dict = {}):
    """
    Perform create/read/update/delete/list on any registered model.

    Registered models: role, account, cookie, api_endpoint, scenario, finding
    Registered actions: create, read, update, delete, list
    
    Args:
        model: model name (role, account, apiendpoint)
        action: one of create/read/update/delete/list
        data: dict for creating or updating
        filters: dict for selecting objects
        
    Returns:
        Result of the action.
    """
    MODEL_REPOSITORIES = {
        "role": RoleRepository,
        "account": AccountRepository,
        "cookie": CookieRepository,
        "api_endpoint": APIEndpointRepository,
        "scenario": ScenarioRepository,
        "finding": FindingRepository,
    }
    
    repository = MODEL_REPOSITORIES.get(model.lower())
    if not repository:
        return "Model not found, available models: " + ", ".join(MODEL_REPOSITORIES.keys())
    
    ACTIONS = ["create", "read", "update", "delete", "list"]
    action = action.lower()
    if action not in ACTIONS:
        return "Invalid action, available actions: " + ", ".join(ACTIONS)
    
    with get_db() as db:
        repo = repository(db)
        
        if action == "create":
            return repo.create(data)
        elif action == "read":
            if 'id' not in filters:
                return "ID is required for read action"
            return repo.get(filters['id'])
        elif action == "update":
            if 'id' not in filters:
                return "ID is required for update action"
            return repo.update(filters['id'], data)
        elif action == "delete":
            if 'id' not in filters:
                return "ID is required for delete action"
            return repo.delete(filters['id'])
        elif action == "list":
            return repo.list()


if __name__ == "__main__":
    mcp.run(transport="stdio")
    # mcp.run(transport="http", host="0.0.0.0", port=8000)