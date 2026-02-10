from __future__ import annotations
import os
import json
import requests
from typing import Optional

def send_via_webhook(message: str, webhook_url: Optional[str] = None) -> None:
    webhook_url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError("Missing Slack webhook URL. Set SLACK_WEBHOOK_URL env var.")
    # Do not log message content here
    payload = {"text": message}
    resp = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type":"application/json"}, timeout=10)
    resp.raise_for_status()

def send_via_bot_token(message: str, channel: str) -> None:
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing Slack bot token. Set SLACK_BOT_TOKEN env var.")
    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"},
        json={"channel": channel, "text": message, "parse": "full"},
        timeout=10,
    )
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data}")
