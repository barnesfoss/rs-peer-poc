# Runestone Peer Instruction PoCs

This repository contains code that exploits vulnerabilities within the [publish_message](https://github.com/RunestoneInteractive/rs/blob/eca3eba5162d4461dd5966fffbfd58d3022f332f/bases/rsptx/assignment_server_api/routers/peer.py#L1312) api endpoint. This code is for research and debugging purposes only.

## Vulnerabilities
### POC 1 - Access to instructor commands
#### CWE-306: Missing Authentication for Critical Function

The `CWE-306.py` shows that attackers can access commands designed for instructors. Enabling them to use the following:
- Broadcast - Chat within every chat in the session
- countDownAndStop - Starts a timer that closes a question for all students
- enableVote - Start voting questions for all students
- enableNext - Moves all students to the next question within the session
- enableChat - Enables the chat for all students
- enableFaceChat - Enables the group "face-to-face" discussion menu for all students

### POC 2 - XSS via `enableChat`
#### CWE-79: Cross-Site Scripting

`CWE-79.py` shows an example of utilizing the vulnerability within PoC 1 to inject persistent arbitrary code; by leveraging the [answers](https://github.com/RunestoneInteractive/rs/blob/eca3eba5162d4461dd5966fffbfd58d3022f332f/bases/rsptx/assignment_server_api/routers/peer.py#L960) argument, attacker-controlled input can be inserted into the answers field of the chat GUI without any kind of validation. This allows an attacker to inject a persistent Javascript payload.

## Usage

Both files take 3 basic command line arguments:
- `access_token` for user authentication, instructor or editor role is not required
- `course_name` the name of the targeted course
- `div_id` the name of the target peer instruction assignment

`CWE-79.py` automatically injects `payload.html` when given these arguments.<br/>
`CWE-306.py` is slightly more complicated in that it creates a simple repl.
You can send a control by prefixing a message with `c` e.g. `>> c enableChat`.<br/>
All other messages are sent as a broadcast.

## Summary

CWE-306 allows an attacker to gain access to instructor functionality which in turn allows the function of CWE-79. It's important to note that there is still an underlying XSS vulnerability within `enableChat`, which is accessable by anyone with appropriate privileges.
