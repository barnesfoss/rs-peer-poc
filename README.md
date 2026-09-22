# Runestone Peer Instruction PoCs

This repository contains code that exploits vulnerabilities within the [publish_message](https://github.com/RunestoneInteractive/rs/blob/eca3eba5162d4461dd5966fffbfd58d3022f332f/bases/rsptx/assignment_server_api/routers/peer.py#L1312) api endpoint. This code is for research and debugging purposes only.

## Vulnerabilities
### POC 1 - Access to instructor commands
#### CWE-306: Missing Authentication for Critical Function

The `CWE-306.py` shows that non-instructor users can access commands designed for instructors. Enabling them to use the following:
- Broadcast - Chat within every chat in the session
- countDownAndStop - Starts a timer that closes a question for all students
- enableVote - Start voting questions for all students
- enableNext - Moves all students to the next question within the session
- enableChat - Enables the chat for all students
- enableFaceChat - Enables the group "face-to-face" discussion menu for all students

### POC 2 - XSS via `enableChat`
#### CWE-79: Cross-Site Scripting

`CWE-79.py` shows an example of utilizing the vulnerability within PoC 1 to inject persistent arbitrary code; by leveraging the [answers](https://github.com/RunestoneInteractive/rs/blob/eca3eba5162d4461dd5966fffbfd58d3022f332f/bases/rsptx/assignment_server_api/routers/peer.py#L960) argument attacker-controlled input can be inserted into the answers field of the chat GUI without any kind of validation, allowing an attacker to inject a persistent Javascript payload.


## Conclusion

These two vulnerabilities are related, CWE-306 allows an ordinary user to gain access to instructor functionality which further allows the function of CWE-79. Though it's important to note that there is still an underlying XSS vulnerability within `enableChat` that could be accessed by anyone with instructor privileges.
