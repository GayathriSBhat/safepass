from __future__ import annotations
import argparse
import os
import sys
from getpass import getpass

from .strength import check_strength
from .generator import generate_password
from .hibp import k_anonymity_query
from .slack_send import send_via_webhook, send_via_bot_token

def cmd_check(args):
    pw = args.password or getpass("Enter password to check (input hidden): ")
    res = check_strength(pw, min_length=args.min_length, require_sets=not args.no_sets)
    if res.feedback:
        print("Strength feedback:")
        for f in res.feedback:
            print(f"- {f}")
    else:
        print("Strength checks passed.")
    if args.hibp:
        try:
            found, count = k_anonymity_query(pw)
            if found:
                print(f"Found in breach database {count} times.")
                sys.exit(2)
            else:
                print("Not found in HIBP breach database.")
        except Exception as e:
            print(f"HIBP check failed: {e}")
            sys.exit(3)
    sys.exit(0 if not res.feedback else 1)

def cmd_generate(args):
    length = args.length
    if length is None:
        length = 20
    if length < 16 or length > 24:
        print("Warning: recommended length is 16–24 characters.", file=sys.stderr)
    pw = generate_password(
        length=length,
        require_symbol=not args.no_symbols,
        allow_symbols=not args.no_symbols,
        require_digit=not args.no_digits,
        require_upper=not args.no_upper,
        require_lower=not args.no_lower,
    )
    # Print safely: mask partially unless explicitly asked to show
    if args.show:
        print(pw)
    else:
        print("Generated a password (hidden). Use --show to display.")
    if args.slack:
        msg = f"""Here is your generated password:\n`{pw}`""" if args.show else "A new password has been generated. Use --show to display locally; sent securely to Slack."
        try:
            if args.channel:
                send_via_bot_token(f"""`{pw}`""", args.channel)
            else:
                send_via_webhook(f"""`{pw}`""")
            print("Sent to Slack successfully.")
        except Exception as e:
            print(f"Failed to send to Slack: {e}", file=sys.stderr)
            sys.exit(4)

def cmd_slack(args):
    message = args.message
    if not message:
        print("No message provided.", file=sys.stderr)
        sys.exit(1)
    try:
        if args.channel:
            send_via_bot_token(message, args.channel)
        else:
            send_via_webhook(message)
        print("Sent.")
    except Exception as e:
        print(f"Failed to send to Slack: {e}", file=sys.stderr)
        sys.exit(2)

def build_parser():
    p = argparse.ArgumentParser(prog="securepass", description="Secure Password Strength & Distribution System")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("check", help="Check password strength and breaches")
    c.add_argument("--password", help="Password to check (omit to prompt)", default=None)
    c.add_argument("--min-length", type=int, default=12, help="Minimum length (default 12)")
    c.add_argument("--no-sets", action="store_true", help="Do not require all character classes")
    c.add_argument("--hibp", action="store_true", help="Also check against HIBP using k-anonymity")
    c.set_defaults(func=cmd_check)

    g = sub.add_parser("generate", help="Generate a strong random password")
    g.add_argument("--length", type=int, help="Password length (default 20, recommended 16–24)")
    g.add_argument("--no-symbols", action="store_true", help="Disallow symbols")
    g.add_argument("--no-digits", action="store_true", help="Do not require digits")
    g.add_argument("--no-upper", action="store_true", help="Do not require uppercase")
    g.add_argument("--no-lower", action="store_true", help="Do not require lowercase")
    g.add_argument("--show", action="store_true", help="Print the generated password to stdout")
    g.add_argument("--slack", action="store_true", help="Send generated password to Slack (webhook if no channel is set)")
    g.add_argument("--channel", help="Slack channel ID for bot-token sending (uses SLACK_BOT_TOKEN)")
    g.set_defaults(func=cmd_generate)

    s = sub.add_parser("slack", help="Send an arbitrary secret message to Slack")
    s.add_argument("message", nargs="?", default=None, help="The message to send")
    s.add_argument("--channel", help="Slack channel ID for bot-token sending (uses SLACK_BOT_TOKEN)")
    s.set_defaults(func=cmd_slack)

    return p

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
