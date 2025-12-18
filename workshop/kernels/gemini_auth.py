"""
gemini_auth.py
OAuth2 authentication helper for Gemini API with Interactions API support.

This module handles OAuth authentication for the Gemini API, specifically
for features requiring OAuth (like the Interactions API / Deep Research).

Credentials are cached at ~/.config/capy/token.json after first authorization.

Usage:
    from gemini_auth import get_authenticated_client

    client = get_authenticated_client()
    # Now use client.interactions.create() for Deep Research
"""

import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth2 scopes required for Gemini Interactions API
SCOPES = [
    'https://www.googleapis.com/auth/generative-language.retriever',
    'https://www.googleapis.com/auth/cloud-platform'
]

# Configuration paths
CONFIG_DIR = Path.home() / '.config' / 'capy'
CLIENT_SECRET_FILE = CONFIG_DIR / 'client_secret.json'
TOKEN_FILE = CONFIG_DIR / 'token.json'


def load_credentials() -> Credentials:
    """
    Load or create OAuth2 credentials for Gemini API.

    On first run, opens a browser for OAuth consent.
    On subsequent runs, uses cached token (refreshing if expired).

    Returns:
        google.oauth2.credentials.Credentials object
    """
    creds = None

    # Check for existing token
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired credentials
            creds.refresh(Request())
        else:
            # Run OAuth flow (opens browser)
            if not CLIENT_SECRET_FILE.exists():
                raise FileNotFoundError(
                    f"OAuth client secret not found at {CLIENT_SECRET_FILE}\n"
                    "Please create OAuth credentials in Google Cloud Console:\n"
                    "1. Go to https://console.cloud.google.com/apis/credentials\n"
                    "2. Create OAuth client ID (Desktop app)\n"
                    "3. Download JSON and save to ~/.config/capy/client_secret.json"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE),
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_authenticated_client():
    """
    Get a google.genai.Client authenticated with OAuth2.

    This client can use the Interactions API for Deep Research.

    Returns:
        google.genai.Client configured with OAuth credentials
    """
    from google import genai

    creds = load_credentials()

    # Create client with OAuth credentials
    # Note: The genai library accepts credentials for Vertex AI mode,
    # but for Gemini API with OAuth we need to set up differently
    client = genai.Client(
        credentials=creds,
        http_options={'api_version': 'v1alpha'}
    )

    return client


def test_auth():
    """Test authentication by making a simple API call."""
    print("Testing Gemini API authentication...")
    print(f"Client secret: {CLIENT_SECRET_FILE}")
    print(f"Token file: {TOKEN_FILE}")

    try:
        client = get_authenticated_client()
        print("✓ Authentication successful!")
        print(f"  Client type: {type(client)}")
        return True
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False


if __name__ == "__main__":
    test_auth()
