#!/usr/bin/env python3
"""
Simple script to demonstrate GitHub device code authentication.

This script requests a device/user code using GitHub's device code flow,
prints instructions for the user to enter the code at the verification URL,
polls GitHub for the resulting access token and prints it.
"""

import time
import json
import urllib.request
import urllib.parse
import webbrowser

# Replace with your OAuth application's client ID or use GitHub CLI's ID.
CLIENT_ID = 'a945f87ad537bfddb109'
SCOPE = 'repo'  # adjust scopes as needed

def request_device_code(client_id: str, scope: str) -> dict:
    data = urllib.parse.urlencode({'client_id': client_id, 'scope': scope}).encode('utf-8')
    req = urllib.request.Request('https://github.com/login/device/code', data=data,
                                 headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)

def poll_for_access_token(client_id: str, device_code: str, interval: int, expires_in: int) -> dict:
    token_url = 'https://github.com/login/oauth/access_token'
    start_time = time.time()
    while time.time() - start_time < expires_in:
        data = urllib.parse.urlencode({
            'client_id': client_id,
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }).encode('utf-8')
        req = urllib.request.Request(token_url, data=data, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            result = json.load(resp)
        if 'access_token' in result:
            return result
        error = result.get('error')
        if error == 'authorization_pending':
            time.sleep(interval)
            continue
        if error == 'slow_down':
            interval += 5
            time.sleep(interval)
            continue
        raise RuntimeError(f'Error while polling: {result.get("error_description", error)}')
    raise TimeoutError('Timed out waiting for user authorization')

def main():
    device_data = request_device_code(CLIENT_ID, SCOPE)
    user_code = device_data['user_code']
    verification_uri = device_data['verification_uri']
    expires_in = device_data['expires_in']
    interval = device_data['interval']
    device_code = device_data['device_code']

    print('Please complete authorization by visiting the following URL and entering the code:')
    print(f'{verification_uri}\nCode: {user_code}')

    try:
        webbrowser.open(verification_uri)
    except Exception:
        pass

    print('Waiting for authorization...')
    token_data = poll_for_access_token(CLIENT_ID, device_code, interval, expires_in)
    print('Access token obtained:', token_data['access_token'])

if __name__ == '__main__':
    main()
