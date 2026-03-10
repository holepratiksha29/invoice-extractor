import base64
import os
import requests
from app.core.config import ATTACHMENTS_DIR, settings
from app.core.security import EmailAuth


class EmailReader:
    def __init__(self):
        self.auth = EmailAuth()
        self.graph_base = "https://graph.microsoft.com/v1.0"

        # REQUIRED for application permission
        # Example: invoices@company.com
        self.mailbox = settings.OUTLOOK_USER

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.auth.get_token()}",
            "Accept": "application/json",
        }
    
    def fetch_messages(self, max_messages: int = 10):
        url = f"{self.graph_base}/users/{self.mailbox}/mailFolders/inbox/messages"

        params = {
            "$top": max_messages,
            "$filter": "hasAttachments eq true and isDraft eq false",
            #"$orderby": "receivedDateTime desc",
            "$expand": "attachments"
        }

        response = requests.get(url, headers=self._headers(),params=params)
        response.raise_for_status()

        messages = response.json().get("value", [])
        print(f"Total messages fetched: {len(messages)}")
        return messages

    def fetch_attachments(self, max_messages: int = 2):
        url = f"{self.graph_base}/users/{self.mailbox}/mailFolders/inbox/messages"

        params = {
            "$top": max_messages,
            "$filter": "hasAttachments eq true and isDraft eq false",
            #"$orderby": "receivedDateTime desc",
            "$expand": "attachments"
        }

        response = requests.get(url, headers=self._headers(),params=params)
        response.raise_for_status()

        messages = response.json().get("value", [])
        print(f"Total messages fetched: {len(messages)}")

        files = []

        for msg in messages:
            print(f"Processing message: {msg.get('subject')} (ID: {msg.get('receivedDateTime')})")
            for att in msg.get("attachments", []):
                print(f"Processing attachment: {att.get('name')} ({att.get('@odata.mediaContentType')})")
                if not att.get("contentBytes"):
                    continue

                if att.get("@odata.mediaContentType") in (
                    "application/pdf",
                    "image/png",
                    "image/jpeg",
                ):
                    os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
                    file_path = os.path.join(ATTACHMENTS_DIR, att["name"])

                    with open(file_path, "wb") as f:
                        f.write(base64.b64decode(att["contentBytes"]))
                        print(f"Saved attachment: {file_path}")
                    files.append(file_path)

        return files
