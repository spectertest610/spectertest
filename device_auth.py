#!/usr/bin/env python3

import os
import sys
import time
import json
import webbrowser
import urllib.request
import urllib.parse

def get_device_code(client_id, scope="repo"):
    """
    Request a device and user code from GitHub for the OAuth device flow.
    """
    url = "https://github.com/login/device/code"
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "scope": scope
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)

def poll_for_token(client_id, device_code, interval, expires_in):
    """
    Poll GitHub for an access token once the user has entered the user code
    on the verification page.
    """
    token_url = "https://github.com/login/oauth/access_token"
    start = time.time()
    while time.time() - start < expires_in:
        data = urllib.parse.urlencode({
            "client_id": client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }).encode("utf-8")
        req = urllib.request.Request(token_url, data=data, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req) as resp:
            result = json.load(resp)
        if "access_token" in result:
            return result
        error = result.get("error")
        if error == "authorization_pending":
            time.sleep(interval)
            continue
        if error == "slow_down":
            interval += 5
            time.sleep(interval)
            continue
        raise RuntimeError(f"Error while polling: {result.get('error_description', error)}")
    raise TimeoutError("Timed out waiting for the user to authorize the device.")

def main():
    """
    Initiate the device code flow. You must set the GITHUB_CLIENT_ID environment
    variable to your OAuth application's client ID before running this script.
    """
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    if not client_id:
        print("Please set the GITHUB_CLIENT_ID environment variable with your OAuth client ID.")
        sys.exit(1)
    device_data = get_device_code(client_id)
    user_code = device_data["user_code"]
    verification_uri = device_data["verification_uri"]
    expires_in = device_data["expires_in"]
    interval = device_data["interval"]
    device_code = device_data["device_code"]

    print("Please complete authorization by visiting the following URL in a browser and entering the code:")
    print(f"{verification_uri}\nCode: {user_code}")
    # optionally open browser automatically
    try:
        webbrowser.open(verification_uri)
    except Exception:
        pass

    print("Waiting for authorization...")
    token = poll_for_token(client_id, device_code, interval, expires_in)
    access_token = token["access_token"]
    print("Successfully received access token:")
    print(access_token)

if __name__ == "__main__":
    main()
