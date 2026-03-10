import base64
import os
import requests
from typing import List, Dict

from app.core.config import ATTACHMENTS_DIR, settings
from app.core.security import EmailAuth


class EmailReader:
    def __init__(self):
        self.auth = EmailAuth()
        self.graph_base = "https://graph.microsoft.com/v1.0"
        self.mailbox = settings.OUTLOOK_USER  # application permission mailbox

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.auth.get_token()}",
            "Accept": "application/json",
            "ConsistencyLevel": "eventual",  # 🔥 REQUIRED
        }


    # --------------------------------------------------
    # 1️⃣ Fetch Inbox Messages (latest → older)
    # --------------------------------------------------
    def fetch_messages(self, max_messages: int = 5):
        url = f"{self.graph_base}/users/{self.mailbox}/mailFolders/inbox/messages"

        params = {
            "$top": max_messages,
            "$filter": "hasAttachments eq true and isDraft eq false",
            "$orderby": "receivedDateTime desc",
            "$select": "id,subject,receivedDateTime",
            "$count": "true",
        }

        response = requests.get(
            url,
            headers=self._headers(),
            params=params
        )
        response.raise_for_status()

        messages = response.json().get("value", [])
        print(f"📩 Total inbox messages fetched: {len(messages)}")
        return messages


    # --------------------------------------------------
    # 2️⃣ Fetch Attachments for a Single Message
    # --------------------------------------------------
    def fetch_attachments_for_message(self, message_id: str) -> List[str]:
        url = (
            f"{self.graph_base}/users/{self.mailbox}"
            f"/messages/{message_id}/attachments"
        )

        response = requests.get(url, headers=self._headers())
        response.raise_for_status()

        attachments = response.json().get("value", [])
        saved_files = []

        for att in attachments:
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

                print(f"📎 Saved attachment: {file_path}")
                saved_files.append(file_path)

        return saved_files

    # --------------------------------------------------
    # 3️⃣ Orchestrator (Messages → Attachments)
    # --------------------------------------------------
    def fetch_latest_invoice_attachments(self, max_messages: int = 5) -> List[str]:
        files = []

        messages = self.fetch_messages(max_messages)

        if not messages:
            print("⚠ No inbox messages with attachments found")
            return files

        for msg in messages:
            print(
                f"\n➡ Processing message:"
                f"\n   Subject : {msg.get('subject')}"
                f"\n   Received: {msg.get('receivedDateTime')}"
            )

            message_files = self.fetch_attachments_for_message(msg["id"])
            files.extend(message_files)

        return files
