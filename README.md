# Python Email Bot (WIP)

I'm new to this whole web development thing. I want to create an email bot to handle POST requests from a contact-me form submission on my personal website (another WIP).

This email bot is a work in progress. Once finished, the bot will be able to:

- [ ] Run on the cloud in a Docker container.
- [ ] Communicate with a web server (such as a personal website backend) to authorize API requests so that users cannot send unauthorized emails from the bot.
- [ ] Send professional looking emails using HTML templates.
---

## Initial API Design

The API endpoints are handled using Flask and include the URIs:

### `/email-server`
**Method(s)**: `POST`

The `email-server` endpoint is where an authorized web client should send the email data as a simple JSON object in the request body.

**Example JSON:** 
```json
{
    "to": [
        "<email-recipient>",
    ],
    "cc": [
        "[carbon-copy-email-recipient]",
    ],
    "bcc": [
        "[blind-carbon-copy-email-recipient]",
    ],
    "subject": "[subject-text]",
    "body": "<body-text>",
}
```

### `/email-auth`
**Method(s)**: `POST`?

I'm not entirely sure how I want to implement this yet. This should be the endpoint in which requests can be authorized through the use of a token given out be the website,
