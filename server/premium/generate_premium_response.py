#!/usr/bin/env python3
"""Utility to generate premium server responses and activate subscriptions.

Creates a JSON response file under `server/premium/users/` so the server can
return an active subscription for the provided premium identifier.
"""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime
from pathlib import Path


DEFAULT_COMMENT = "Thanks For Trying Premium Version\nKeep Supporting the Project 👍"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the server response used to activate a premium subscription "
            "for a user."
        )
    )
    parser.add_argument(
        "--pid",
        required=True,
        help="Premium identifier. This is also used as the response filename.",
    )
    parser.add_argument(
        "--key",
        required=True,
        help="Activation key or token to embed in the server response.",
    )
    parser.add_argument(
        "--user-id",
        dest="user_id",
        help="Optional numeric user identifier. Defaults to a random 5-digit value.",
    )
    parser.add_argument(
        "--uid",
        help="Optional device/user UID to embed alongside the premium response.",
    )
    parser.add_argument(
        "--status",
        default="1",
        choices=["0", "1"],
        help="Subscription status flag. Use 1 to activate, 0 to disable (default: 1).",
    )
    parser.add_argument(
        "--mode",
        default="Permanent Access",
        help="Subscription mode label to persist with the response.",
    )
    parser.add_argument(
        "--comment",
        default=DEFAULT_COMMENT,
        help="Optional note stored with the response.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Custom output directory for the response file (defaults to ./users).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing response file if it already exists.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    output_dir = (
        args.output_dir
        if args.output_dir is not None
        else Path(__file__).resolve().parent / "users"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / args.pid
    if target.exists() and not args.force:
        parser.error(
            f"Refusing to overwrite existing response file at {target}. "
            "Use --force to replace it."
        )

    payload = {
        "id": args.user_id or f"{random.randint(0, 99999):05d}",
        "date": datetime.now().strftime("%d/%m/%Y"),
        "status": args.status,
        "key": args.key,
        "comment": args.comment,
        "mode": args.mode,
        "pid": args.pid,
    }

    if args.uid:
        payload["uid"] = args.uid

    with target.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=4, ensure_ascii=False)
        fp.write("\n")

    print(f"✅ Premium response written to: {target}")


if __name__ == "__main__":
    main()
