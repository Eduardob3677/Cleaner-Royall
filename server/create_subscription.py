#!/usr/bin/env python3
"""
Utility script to generate server response files for a user's premium activation.

It creates/updates two files using the provided token:
 - server/users/<token>
 - server/premium/users/<token>

Example:
    python create_subscription.py <token> <id> --key MyKey
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate server + premium responses and activate a subscription."
    )
    parser.add_argument(
        "token",
        help="Identifier used as filename for the user in both response folders.",
    )
    parser.add_argument(
        "subscription_id",
        help="Identifier stored in the premium response payload.",
    )
    parser.add_argument(
        "--key",
        default="TextView",
        help="Activation key label to embed in the premium response.",
    )
    parser.add_argument(
        "--mode",
        default="Permanent Acess",
        help="Access mode text saved with the premium response.",
    )
    parser.add_argument(
        "--comment",
        default="Thanks For Trying Premium Version\nKeep Supporting the Project 👍",
        help="Comment stored in the premium response payload.",
    )
    parser.add_argument(
        "--message",
        default="Premium activated for this device.",
        help="Message returned to the user in the general response payload.",
    )
    parser.add_argument(
        "--server-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Path to the 'server' directory. Defaults to the script location.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    server_dir = args.server_dir.resolve()
    users_dir = server_dir / "users"
    premium_users_dir = server_dir / "premium" / "users"

    users_dir.mkdir(parents=True, exist_ok=True)
    premium_users_dir.mkdir(parents=True, exist_ok=True)

    today = _dt.date.today().strftime("%d/%m/%Y")

    general_payload = {
        "RemovePremium": "0",
        "TransferredPremium": "0",
        "informdev": "0",
        "expired": "0",
        "cmd": "none",
        "Msg": args.message,
    }

    premium_payload = {
        "id": str(args.subscription_id),
        "date": today,
        "status": "1",
        "key": args.key,
        "comment": args.comment,
        "mode": args.mode,
    }

    general_file = users_dir / args.token
    premium_file = premium_users_dir / args.token

    general_file.write_text(json.dumps(general_payload, indent=4) + "\n", encoding="utf-8")
    premium_file.write_text(json.dumps(premium_payload, indent=4) + "\n", encoding="utf-8")

    print(f"Updated server response: {general_file}")
    print(f"Updated premium response: {premium_file}")


if __name__ == "__main__":
    main()
