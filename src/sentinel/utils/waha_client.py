"""
WAHA API Client
"""

from typing import Dict, List, Optional, Any
import httpx
from loguru import logger
from datetime import datetime

from sentinel.config import settings


class WAHAClient:
    """Client for interacting with WAHA API"""

    def __init__(self):
        self.base_url = settings.WAHA_API_URL
        self.api_key = settings.WAHA_API_KEY
        self.session_name = settings.WAHA_SESSION_NAME
        self.timeout = settings.WAHA_TIMEOUT

        self.headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            self.headers["X-Api-Key"] = self.api_key

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to WAHA API"""
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=self.headers,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"WAHA API error: {e}")
            raise

    async def get_session_status(self) -> Dict[str, Any]:
        """Get session status"""
        return await self._request("GET", f"/api/sessions/{self.session_name}")

    async def start_session(self) -> Dict[str, Any]:
        """Start WhatsApp session"""
        return await self._request(
            "POST",
            f"/api/sessions/{self.session_name}/start",
        )

    async def stop_session(self) -> Dict[str, Any]:
        """Stop WhatsApp session"""
        return await self._request(
            "POST",
            f"/api/sessions/{self.session_name}/stop",
        )

    async def send_message(
        self,
        chat_id: str,
        text: str,
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send text message"""
        data = {
            "chatId": chat_id,
            "text": text,
            "session": self.session_name,
        }
        if reply_to:
            data["reply_to"] = reply_to

        return await self._request(
            "POST",
            f"/api/sendText",
            data=data,
        )

    async def send_typing(self, chat_id: str, duration: int = 3) -> Dict[str, Any]:
        """Send typing indicator"""
        data = {
            "chatId": chat_id,
            "session": self.session_name,
            "duration": duration,
        }
        return await self._request(
            "POST",
            f"/api/startTyping",
            data=data,
        )

    async def get_chats(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all chats"""
        params = {
            "session": self.session_name,
            "limit": limit,
        }
        response = await self._request("GET", "/api/chats", params=params)
        return response.get("chats", [])

    async def get_messages(
        self,
        chat_id: str,
        limit: int = 100,
        download_media: bool = False,
    ) -> List[Dict[str, Any]]:
        """Get messages from a chat"""
        params = {
            "session": self.session_name,
            "chatId": chat_id,
            "limit": limit,
            "downloadMedia": download_media,
        }
        response = await self._request("GET", "/api/messages", params=params)
        return response.get("messages", [])

    async def get_all_messages(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get all messages from all chats (for historical extraction)"""
        all_messages = []

        # Get all chats first
        chats = await self.get_chats(limit=1000)
        logger.info(f"Found {len(chats)} chats")

        # Get messages from each chat
        for chat in chats:
            chat_id = chat.get("id")
            if not chat_id:
                continue

            try:
                messages = await self.get_messages(chat_id=chat_id, limit=1000)

                # Filter by date if provided
                if start_date or end_date:
                    filtered_messages = []
                    for msg in messages:
                        msg_timestamp = msg.get("timestamp")
                        if not msg_timestamp:
                            continue

                        msg_date = datetime.fromtimestamp(msg_timestamp)

                        if start_date and msg_date < datetime.fromisoformat(start_date):
                            continue
                        if end_date and msg_date > datetime.fromisoformat(end_date):
                            continue

                        filtered_messages.append(msg)

                    messages = filtered_messages

                all_messages.extend(messages)
                logger.debug(f"Chat {chat_id}: {len(messages)} messages")

            except Exception as e:
                logger.error(f"Error getting messages from chat {chat_id}: {e}")
                continue

        logger.info(f"Total messages extracted: {len(all_messages)}")
        return all_messages

    async def set_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Configure webhook for receiving messages"""
        data = {
            "session": self.session_name,
            "url": webhook_url,
        }
        return await self._request(
            "POST",
            "/api/webhooks",
            data=data,
        )

    async def react_to_message(
        self,
        chat_id: str,
        message_id: str,
        reaction: str,
    ) -> Dict[str, Any]:
        """React to a message with emoji"""
        data = {
            "chatId": chat_id,
            "messageId": message_id,
            "reaction": reaction,
            "session": self.session_name,
        }
        return await self._request(
            "POST",
            "/api/sendReaction",
            data=data,
        )
