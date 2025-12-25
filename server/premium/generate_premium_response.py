#!/usr/bin/env python3
"""Utility to generate premium server responses and activate subscriptions.

Creates a JSON response file under `server/premium/users/` so the server can
return an active subscription for the provided premium identifier.
"""

from __future__ import annotations

import argparse
import json
import re
import secrets
from datetime import datetime
from pathlib import Path


DEFAULT_COMMENT = "Thanks For Trying Premium Version\nKeep Supporting the Project 👍"


def _validate_pid(pid: str) -> str:
    if Path(pid).name != pid or "/" in pid or "\\" in pid:
        raise argparse.ArgumentTypeError("pid must not contain path separators.")
    if not re.fullmatch(r"[A-Za-z0-9._=+-]+", pid):
        raise argparse.ArgumentTypeError(
            "pid may only contain letters, numbers, dot, underscore, plus, minus or equals."
        )
    return pid


def _validate_user_id(user_id: str) -> str:
    if not user_id.isdigit():
        raise argparse.ArgumentTypeError("user-id must be numeric.")
    return user_id


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the server response used to activate a premium subscription "
            "for a user."
        )
    )
    parser.add_argument(
        "--pid",
        type=_validate_pid,
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
        type=_validate_user_id,
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
        "--date-format",
        default="%d/%m/%Y",
        help="Custom strftime format for the date field (default: %(default)s).",
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

    try:
        formatted_date = datetime.now().strftime(args.date_format)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive guard
        parser.error(f"Invalid date format: {exc}")

    payload = {
        "id": args.user_id or f"{secrets.randbelow(100000):05d}",
        "date": formatted_date,
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
