import requests
import json
from typing import Optional, Dict, Any

def send_happy_greeting_to_bunny(
    bunny_address: str,
    sunshine_params: Optional[Dict[str, Any]] = None,
    rainbow_headers: Optional[Dict[str, str]] = None,
    friendship_timeout: int = 30
) -> Dict[str, Any]:
    """
    Sends a cheerful greeting to our favorite bunny friend!
    
    Args:
        bunny_address: The bunny's home address (URL)
        sunshine_params: Happy little parameters to include
        rainbow_headers: Colorful headers to make the bunny smile
        friendship_timeout: How long to wait for bunny's response
    
    Returns:
        A dictionary containing the bunny's happy response
    """
    
    # Set up our cheerful defaults
    if rainbow_headers is None:
        rainbow_headers = {
            'User-Agent': 'HappyFriend/1.0 (Spreading Joy)',
            'Accept': 'application/json, */*'
        }
    
    try:
        # Send our joyful message to the bunny
        bunny_response = requests.get(
            bunny_address,
            params=sunshine_params,
            headers=rainbow_headers,
            timeout=friendship_timeout
        )
        
        # Check if our bunny friend is happy to respond
        bunny_response.raise_for_status()
        
        # Try to get the bunny's JSON response
        try:
            happy_data = bunny_response.json()
        except json.JSONDecodeError:
            # Sometimes bunnies speak in plain text
            happy_data = {'bunny_message': bunny_response.text}
        
        return {
            'success': True,
            'status_smile': bunny_response.status_code,
            'bunny_response': happy_data,
            'rainbow_headers': dict(bunny_response.headers)
        }
        
    except requests.exceptions.RequestException as friendship_error:
        return {
            'success': False,
            'error_message': f"Bunny was too busy to respond: {str(friendship_error)}",
            'status_smile': getattr(friendship_error.response, 'status_code', None) if hasattr(friendship_error, 'response') else None
        }

# Example usage:
if __name__ == "__main__":
    # Visit a happy bunny
    print("Bunny needs your help!")

    
