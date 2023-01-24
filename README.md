# Python Email Bot (WIP)

I'm new to this whole web development thing. I want to create an email bot to handle POST requests from a contact-me form submission on my personal website (another WIP).

This email bot is a work in progress. Once finished, the bot will be able to:

- [x] Run on the cloud in a Docker container.
- [x] Communicate with a web server.
- [x] Authorize API requests using API keys.
- [x] Send professional looking emails using HTML templates.
- [ ] Use SSL or TLS encryption service
- [ ] Support uploading HTML templates and images using the email-bot dashboard.

---

## Setup

### Postgres Database

This email bot uses a PostgreSQL database to store and manage API keys. *An instance of a Postgres database MUST be started before API keys can be registered for the email bot.*

### Email Bot

A couple of environment variables need to be set for the email bot to work  either with a .env file or with docker:

Variable | Use
--|--
`BOT_EMAIL_ADDRESS`   | Email address that the bot uses to send emails
`BOT_EMAIL_PASSWORD`  | Password for email that the bot uses to send emails
`EMAIL_BOT_LOG_FILE`* | Optional log file location
`SMTP_ADDRESS`        | Address to the SMTP server for your email provider (ex. `smtp.google.com`)
`SMTP_PORT`*          | SMTP port for your email provider's SMTP server (defaults to 465)
`POSTGRES_USERNAME`   | Username used to access PostgreSQL database
`POSTGRES_PASSWORD`   | Password used to access PostgreSQL database
`POSTGRES_HOSTNAME`   | Address in which the PostgresSQL database is hosted
`POSTGRES_PORT`*      | Port that the PostgresSQL database is hosted (defaults to 5432)

\* *optional environment variable*

---

## Initial API Design

The API endpoints to this bot are handled using Flask and include the URLs:

### `/` (root endpoint)
**Method(s)**: `GET`

This endpoint leads to a dashboard webpage where the registered Key Manager can create, delete, and manage API keys (works by sending HTTP requests to the `/api-keys` endpoint). In future versions, the Key Manager should be able to upload HTML templates and images to the API server.

If an unauthenticated user attempts to access this endpoint, they are redirected to the `/login` page.

### `/login`
**Methods(s)**: `GET`, `POST`

Allows the Key Manager to log in. Redirects to the home dashboard page upon successful authentication.

### `/logout`
**Methods(s)**: `GET`

Allows the Key Manager to log out and makes the server to clear the Key Manager's session. Redirects to login page after clearing the Key Manager's session.

### `/send-email`
**Method(s)**: `POST`

The `email-server` endpoint is where an authorized web client should send the email data as a simple `POST` request.

Additionally, a API client must provide a username as well as an API key in the `Authorization` header of a post in order to send an email using the API.

***Javascript `fetch` example:***

```js
// base 64 encoded authorization header:
const encoded = btoa("<username>:<api-key>");

fetch('https://api.websitesite.com/', {
    methods: 'POST',
    headers: {
        'Authorization': `Basic ${encoded}`,
        'Content-Type': 'application/json'
    },
    // email data gets passed in body as JSON
    body: JSON.stringify({
        "to": [
            "<email-recipients>",
        ],
        "cc": [
            "[carbon-copy-email-recipients]",
        ],
        "bcc": [
            "[blind-carbon-copy-email-recipients]",
        ],
        "subject": "[subject-text]",
        "template": "[template-file-name]",
        "context": {
            "[context-var1]": "[context-val1]",
        },
    })
});
```

### `/api-keys`
**Method(s):** `GET`, `POST`, `DELETE`

Basic CRUD endpoint for fetching, creating, and deleting api keys. In future versions, there will be an `PUT` method where the Key Manager can update the data for API key.

---

## Email HTML Templates

HTML email templates are rendered using [Flask's HTML template rendering](https://flask.palletsprojects.com/en/2.2.x/quickstart/#rendering-templates).

**Example Template:**
```html
<!DOCTYPE html>
<html>
    <head></head>
    <body style="margin:0">
        <img width="100%" src="cid:cat-picture"/>
        <table width="100%" style="padding: 2vmin; justify-content:center; display:table">
            <tr><td align="center"><h1>{{ heading }}</h1></td></tr>
            <tr><td align="center">{{ body }}</td></tr>
        </table>
        <footer style="padding: 2vmin; background-color:#dfdfdf">Please do not reply to this email. This email was sent by a bot and will not respond to any messages.</footer>
    </body>
</html>
```

This bot also supports embedded images in emails. Images are handled using a global `TemplateImageRegistry` object that is used to register images to templates:

```python
"""./register_images.py"""

from image_registry import image_registry, ImageEntry

# create ImageEntry
cat_entry = ImageEntry(
    cid="cat-picture", 
    img_path="./static/images/cat-typing.gif",
    img_type="gif"
)

# register ImageEntry cat_entry to "generic.html" template 
image_registry["generic.html"] = [cat_entry]
```

After the images are registered in the `TemplateImageRegistry` the bot can fetch all the `ImageEntry`s for a given template whenever the template is being rendered.

In future versions, this method of registering files will probably be deprecated in favor of a file uploading feature.

```python
from image_registry import image_registry, ImageEntry

def build_mime_multipart_message(email_address:str, to, subject:str, template:str, context: dict) -> MIMEMultipart:
    # ...
    for recipient in to:
        to_str += (f"{recipient},")

    msg = MIMEMultipart('related')
    # ...
    msgHTML = MIMEText(render_template(template, **context), 'html')
    msg.attach(msgHTML)

    # adds images stored in image registry for the current template to
    # the MIME message
    for entry in image_registry[template]:
        with open(entry.img_path, 'rb') as img_file:
            msgImage = MIMEImage(img_file.read())
            msgImage.add_header('Content-ID', f"<{entry.cid}>")
            msg.attach(msgImage)

    return msg
```
