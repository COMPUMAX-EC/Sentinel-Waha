"""
Message Extractor - Phase I: Diagnóstico
Extracts historical messages from WAHA for analysis
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger
import asyncio

from sentinel.utils.waha_client import WAHAClient
from sentinel.config import settings


class MessageExtractor:
    """Extracts and processes WhatsApp messages for historical analysis"""

    def __init__(self):
        self.client = WAHAClient()
        self.batch_size = settings.EXTRACTION_BATCH_SIZE
        self.max_retries = settings.EXTRACTION_MAX_RETRIES

    async def extract_all_messages(
        self,
        phone_number: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Extract all messages from WAHA

        Args:
            phone_number: Optional filter by phone number
            start_date: Optional start date (YYYY-MM-DD)
            end_date: Optional end date (YYYY-MM-DD)

        Returns:
            List of message dictionaries
        """
        logger.info("Starting message extraction...")
        logger.info(f"Date range: {start_date} to {end_date}")

        try:
            # Get all messages from WAHA
            messages = await self.client.get_all_messages(
                start_date=start_date,
                end_date=end_date,
            )

            # Filter by phone number if provided
            if phone_number:
                messages = [
                    msg
                    for msg in messages
                    if phone_number in msg.get("from", "")
                    or phone_number in msg.get("to", "")
                ]

            logger.info(f"Extracted {len(messages)} messages")
            return messages

        except Exception as e:
            logger.error(f"Error extracting messages: {e}")
            raise

    def process_messages(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process extracted messages to generate insights

        Returns:
            Dictionary with processed data and insights
        """
        if not messages:
            return {
                "total_messages": 0,
                "insights": {},
            }

        # Basic statistics
        total_messages = len(messages)
        incoming_messages = [msg for msg in messages if not msg.get("fromMe", False)]
        outgoing_messages = [msg for msg in messages if msg.get("fromMe", False)]

        # Calculate response times
        response_times = self._calculate_response_times(messages)

        # Identify common questions
        common_questions = self._identify_common_questions(incoming_messages)

        # Analyze message types
        message_types = self._analyze_message_types(messages)

        return {
            "total_messages": total_messages,
            "incoming_count": len(incoming_messages),
            "outgoing_count": len(outgoing_messages),
            "avg_response_time_minutes": response_times.get("average", 0),
            "median_response_time_minutes": response_times.get("median", 0),
            "common_questions": common_questions,
            "message_types": message_types,
            "conversation_stats": self._analyze_conversations(messages),
        }

    def _calculate_response_times(
        self, messages: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate response time statistics"""
        response_times = []

        # Sort messages by timestamp
        sorted_messages = sorted(
            messages, key=lambda x: x.get("timestamp", 0)
        )

        # Calculate time between customer message and our response
        for i in range(len(sorted_messages) - 1):
            current = sorted_messages[i]
            next_msg = sorted_messages[i + 1]

            # If customer sent message and we responded
            if not current.get("fromMe") and next_msg.get("fromMe"):
                time_diff = next_msg.get("timestamp", 0) - current.get("timestamp", 0)
                response_times.append(time_diff / 60)  # Convert to minutes

        if not response_times:
            return {"average": 0, "median": 0, "min": 0, "max": 0}

        sorted_times = sorted(response_times)
        return {
            "average": sum(response_times) / len(response_times),
            "median": sorted_times[len(sorted_times) // 2],
            "min": min(response_times),
            "max": max(response_times),
            "percentile_90": sorted_times[int(len(sorted_times) * 0.9)],
        }

    def _identify_common_questions(
        self, messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify most common customer questions"""
        questions = {}

        for msg in messages:
            text = msg.get("body", "").lower().strip()

            # Simple question detection
            if "?" in text or any(
                word in text
                for word in [
                    "cuánto",
                    "cómo",
                    "dónde",
                    "cuándo",
                    "qué",
                    "precio",
                    "costo",
                ]
            ):
                # Normalize the question
                normalized = text[:100]  # First 100 chars
                questions[normalized] = questions.get(normalized, 0) + 1

        # Sort by frequency
        sorted_questions = sorted(
            questions.items(), key=lambda x: x[1], reverse=True
        )

        return [
            {"question": q, "count": count}
            for q, count in sorted_questions[:10]  # Top 10
        ]

    def _analyze_message_types(
        self, messages: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """Analyze distribution of message types"""
        types = {
            "text": 0,
            "image": 0,
            "video": 0,
            "audio": 0,
            "document": 0,
            "location": 0,
            "other": 0,
        }

        for msg in messages:
            msg_type = msg.get("type", "text").lower()
            if msg_type in types:
                types[msg_type] += 1
            else:
                types["other"] += 1

        return types

    def _analyze_conversations(
        self, messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze conversation patterns"""
        # Group messages by chat
        conversations = {}

        for msg in messages:
            chat_id = msg.get("from") or msg.get("chatId")
            if not chat_id:
                continue

            if chat_id not in conversations:
                conversations[chat_id] = []

            conversations[chat_id].append(msg)

        # Calculate statistics
        conversation_lengths = [len(conv) for conv in conversations.values()]

        # Identify abandoned conversations (customer sent last message)
        abandoned_count = 0
        for conv in conversations.values():
            if conv:
                last_message = sorted(conv, key=lambda x: x.get("timestamp", 0))[-1]
                if not last_message.get("fromMe", False):
                    abandoned_count += 1

        return {
            "total_conversations": len(conversations),
            "avg_messages_per_conversation": (
                sum(conversation_lengths) / len(conversation_lengths)
                if conversation_lengths
                else 0
            ),
            "abandoned_conversations": abandoned_count,
            "abandonment_rate": (
                abandoned_count / len(conversations) if conversations else 0
            ),
        }
