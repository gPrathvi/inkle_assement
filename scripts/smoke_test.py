#!/usr/bin/env python3
import os, sys, json, time
from typing import Tuple

try:
    import requests
except ImportError:
    print("This script requires the 'requests' package. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
USERNAME = os.getenv("TEST_USERNAME", "alice")
EMAIL = os.getenv("TEST_EMAIL", "alice@example.com")
PASSWORD = os.getenv("TEST_PASSWORD", "secret123")

s = requests.Session()

def post(path: str, json_body: dict, token: str = None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = s.post(BASE_URL + path, json=json_body, headers=headers)
    return r

def get(path: str, token: str = None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = s.get(BASE_URL + path, headers=headers)
    return r

def patch(path: str, json_body: dict, token: str = None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = s.patch(BASE_URL + path, json=json_body, headers=headers)
    return r

def delete(path: str, token: str = None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = s.delete(BASE_URL + path, headers=headers)
    return r

if __name__ == "__main__":
    print(f"Using BASE_URL={BASE_URL}")

    # Signup (ignore if user exists)
    r = post("/api/auth/signup/", {"username": USERNAME, "email": EMAIL, "password": PASSWORD})
    print("Signup:", r.status_code, r.text[:200])

    # Login
    r = post("/api/auth/login/", {"username": USERNAME, "password": PASSWORD})
    if r.status_code != 200:
        print("Login failed:", r.status_code, r.text)
        sys.exit(1)
    tokens = r.json()
    access = tokens.get("access")
    print("Login OK, access token acquired")

    # Me (GET)
    r = get("/api/users/me/", token=access)
    print("Me GET:", r.status_code, r.text[:200])

    # Me (PATCH)
    r = patch("/api/users/me/", {"email": EMAIL}, token=access)
    print("Me PATCH:", r.status_code, r.text[:200])

    # Create Post
    r = post("/api/posts/", {"content": "Hello from smoke test"}, token=access)
    print("Create Post:", r.status_code, r.text[:200])
    if r.status_code not in (200, 201):
        sys.exit(1)
    post_id = r.json().get("id")

    # List Posts
    r = get("/api/posts/", token=access)
    print("List Posts:", r.status_code)

    # Like Post
    r = post(f"/api/posts/{post_id}/like/", {}, token=access)
    print("Like:", r.status_code, r.text[:200])

    # Unlike Post
    r = delete(f"/api/posts/{post_id}/like/", token=access)
    print("Unlike:", r.status_code)

    # Delete Post (soft)
    r = delete(f"/api/posts/{post_id}/", token=access)
    print("Delete Post:", r.status_code)

    print("Smoke test complete.")
