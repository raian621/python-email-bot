# Python Email Bot (WIP)

I'm new to this whole web development thing. I want to create an email bot to handle POST requests from a contact-me form submission on my personal website (another WIP).

This email bot is a work in progress. Once finished, the bot will be able to:

- [ ] Run on the cloud in a Docker container.
- [ ] Communicate with a web server
- [ ] Authorize the API requests via `jwt` or `Oauth2`
- [x] Send professional looking emails using HTML templates.
---

## Initial API Design

The API endpoints to this bot are handled using Flask and include the URIs:

### `/email-server`
**Method(s)**: `POST`

The `email-server` endpoint is where an authorized web client should send the email data as a simple JSON object in the request body.

**Example JSON:** 
```json
{
    "to": [
        "<email-recipient>",
        // ...
    ],
    "cc": [
        "[carbon-copy-email-recipient]",
        // ...
    ],
    "bcc": [
        "[blind-carbon-copy-email-recipient]",
        // ...
    ],
    "subject": "[subject-text]",
    "template": "[template-name]",
    "context": {
        "[context-var1]": "[context-val1]",
        // ...
    },
}
```

### `/email-auth`
**Method(s)**: `POST`?

I'm not entirely sure how I want to implement this yet. Probably will use jwt or Oauth2

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

