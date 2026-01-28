"""
Webhook Handlers - Phase II: Automatización
Handles incoming messages from WAHA webhooks
"""

from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
from loguru import logger
import asyncio

from sentinel.config import settings
from sentinel.utils.waha_client import WAHAClient
from sentinel.classifiers import IntentClassifier
from sentinel.response import ResponseEngine, ResponseContext

router = APIRouter()

# Initialize components
waha_client = WAHAClient()
intent_classifier = IntentClassifier()
response_engine = ResponseEngine()


@router.post("/waha")
async def handle_waha_webhook(
    request: Request,
    x_webhook_secret: Optional[str] = Header(None),
):
    """
    Handle incoming messages from WAHA webhook

    This endpoint receives real-time messages from WAHA and processes them:
    1. Validates webhook secret
    2. Classifies message intent
    3. Generates and sends automated response if appropriate
    """

    # Validate webhook secret
    if settings.WEBHOOK_SECRET and x_webhook_secret != settings.WEBHOOK_SECRET:
        logger.warning("Invalid webhook secret received")
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    try:
        # Parse webhook payload
        payload = await request.json()
        logger.info(f"Received webhook: {payload.get('event', 'unknown')}")

        # Only process incoming messages
        event = payload.get("event")
        if event != "message":
            return {"status": "ignored", "reason": "Not a message event"}

        # Extract message data
        message_data = payload.get("payload", {})
        message_text = message_data.get("body", "")
        chat_id = message_data.get("from")
        message_id = message_data.get("id")
        is_from_me = message_data.get("fromMe", False)

        # Ignore messages from ourselves
        if is_from_me:
            return {"status": "ignored", "reason": "Message from self"}

        # Ignore empty messages
        if not message_text:
            return {"status": "ignored", "reason": "Empty message"}

        logger.info(f"Processing message from {chat_id}: {message_text[:50]}...")

        # Classify intent
        intent = intent_classifier.classify(message_text)
        logger.info(
            f"Intent: {intent.level} (confidence: {intent.confidence:.2f}) - {intent.suggested_action}"
        )

        # Check if should auto-respond
        if not intent_classifier.should_auto_respond(intent):
            logger.info("Auto-response disabled for this intent level")
            return {
                "status": "processed",
                "action": "manual_review_required",
                "intent": intent.level,
            }

        # Generate response
        context = ResponseContext(
            customer_message=message_text,
            intent=intent,
            conversation_history=[],  # TODO: Load from DB
        )

        response = response_engine.generate_response(
            context=context,
            humanize=True,
        )

        # Send response asynchronously (don't block webhook)
        asyncio.create_task(
            response_engine.send_humanized_response(
                waha_client=waha_client,
                chat_id=chat_id,
                response=response,
            )
        )

        return {
            "status": "success",
            "intent": intent.level,
            "confidence": intent.confidence,
            "action": intent.suggested_action,
            "response_queued": True,
        }

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test_webhook():
    """Test endpoint for webhook configuration"""
    return {
        "status": "ok",
        "message": "Webhook is configured correctly",
        "timestamp": "2026-01-28T00:00:00Z",
    }


@router.get("/status")
async def webhook_status():
    """Get webhook status and configuration"""
    return {
        "enabled": settings.ENABLE_WEBHOOKS,
        "url": settings.WEBHOOK_URL,
        "auto_response": settings.ENABLE_AUTO_RESPONSE,
        "intent_classification": settings.ENABLE_INTENT_CLASSIFICATION,
    }
