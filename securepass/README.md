# SecurePass — Secure Password Strength & Distribution System

A Python CLI for checking password strength, performing HIBP k-anonymity breach lookups, generating strong passwords, and sending secrets to Slack.

## Features
- **Strength checker** with actionable feedback
- **HIBP k-anonymity** breach check (SHA-1 range API with Add-Padding)
- **Password generator** (16–24 recommended; flags like `--length`, `--no-symbols`)
- **Slack integration** via Incoming Webhooks or Bot Token
- **No plaintext password logging**

## Quick Start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m securepass.cli --help
```

### Check strength + HIBP
```bash
python -m securepass.cli check --hibp
# You'll be prompted securely for the password
```

### Generate a password
```bash
python -m securepass.cli generate --length 20 --show
```

### Send to Slack
Set either:
- `SLACK_WEBHOOK_URL` for webhook delivery **or**
- `SLACK_BOT_TOKEN` and pass `--channel C12345678` for bot-token delivery

```bash
export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'
python -m securepass.cli generate --length 20 --show --slack
```

### Security Notes
- HIBP uses k-anonymity and never sends the full password.
- The tool avoids printing secrets by default; use `--show` to reveal intentionally.
- Configure secrets via environment variables.

## Docker
Build and run:
```bash
docker build -t securepass .
docker run --rm -it --env SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL securepass python -m securepass.cli generate --length 20 --slack
```

## Testing
```bash
pytest -q
```

