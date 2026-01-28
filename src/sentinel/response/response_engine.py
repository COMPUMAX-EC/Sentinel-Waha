"""
Response Engine - Phase II: Automatización
Generates humanized automatic responses
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import random
import asyncio
from datetime import datetime
from loguru import logger

from sentinel.config import settings
from sentinel.classifiers import IntentLevel, IntentResult


@dataclass
class ResponseContext:
    """Context for generating responses"""

    customer_message: str
    intent: IntentResult
    conversation_history: List[Dict[str, Any]]
    customer_name: Optional[str] = None
    product_context: Optional[str] = None


@dataclass
class GeneratedResponse:
    """Generated response with timing"""

    text: str
    delay_seconds: int
    should_show_typing: bool
    typing_duration: int
    use_emoji: bool
    suggested_reactions: List[str]


class ResponseEngine:
    """Generates humanized automatic responses"""

    def __init__(self):
        self.min_delay = settings.RESPONSE_DELAY_MIN
        self.max_delay = settings.RESPONSE_DELAY_MAX
        self.typing_enabled = settings.ENABLE_TYPING_INDICATOR
        self.typing_speed = settings.TYPING_SPEED_CHARS_PER_SECOND

        # Response templates by intent level
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, List[str]]:
        """Load response templates"""
        return {
            "high_intent_price": [
                "¡Claro! El precio es de ${price}. ¿Te gustaría conocer las opciones de envío? 📦",
                "Perfecto, el costo es ${price}. Tenemos disponibilidad inmediata 🎯",
                "El precio es ${price}. Si lo necesitas hoy, podemos enviarlo en las próximas horas 🚀",
            ],
            "high_intent_payment": [
                "Aceptamos transferencia, tarjeta y efectivo. ¿Cuál prefieres? 💳",
                "Puedes pagar con tarjeta, transferencia o en efectivo al recibir. ¿Te parece bien? ✅",
                "Tenemos varias opciones: tarjeta, transferencia SPEI o efectivo. ¿Cuál te viene mejor? 💰",
            ],
            "high_intent_shipping": [
                "El envío tarda 24-48 horas. ¿A qué zona lo necesitas? 📍",
                "Hacemos envíos a toda la república. ¿A dónde te lo mandamos? 🚚",
                "Podemos enviártelo mañana mismo. Solo necesito tu código postal 📮",
            ],
            "high_intent_stock": [
                "¡Sí tenemos en stock! ¿Cuántas piezas necesitas? ✨",
                "Tenemos disponibilidad inmediata. ¿Te lo apartamos? 🎁",
                "Hay disponibles. ¿Quieres que te lo reservemos? ⭐",
            ],
            "medium_intent_info": [
                "Con gusto te explico. ¿Qué te gustaría saber específicamente? 🤔",
                "Te puedo ayudar con eso. ¿Es sobre las características técnicas? 📋",
                "Déjame darte más información. ¿Qué aspecto te interesa más? 💡",
            ],
            "medium_intent_warranty": [
                "Incluye garantía de {warranty_period}. Cubre cualquier defecto de fábrica 🛡️",
                "Tiene {warranty_period} de garantía. ¿Necesitas más detalles? ✅",
                "La garantía es de {warranty_period}. Te damos factura con todo en regla 📄",
            ],
            "low_intent_greeting": [
                "¡Hola! 👋 ¿En qué te puedo ayudar hoy?",
                "¡Buen día! 😊 ¿Buscas algo en particular?",
                "¡Hola! ¿Cómo estás? Cuéntame, ¿qué necesitas? 👍",
            ],
            "low_intent_thanks": [
                "¡Para eso estamos! 😊 Cualquier cosa me avisas",
                "¡Un placer ayudarte! 👍 Estamos para servirte",
                "¡De nada! 🙌 Aquí estamos cuando nos necesites",
            ],
        }

    def generate_response(
        self,
        context: ResponseContext,
        humanize: bool = True,
    ) -> GeneratedResponse:
        """
        Generate appropriate response based on context

        Args:
            context: ResponseContext with message and intent
            humanize: Whether to add human-like delays and behaviors

        Returns:
            GeneratedResponse with text and timing information
        """
        # Select appropriate template based on intent
        template = self._select_template(context)

        # Generate response text
        response_text = self._fill_template(template, context)

        # Calculate humanized timing
        delay_seconds = 0
        typing_duration = 0
        should_show_typing = False

        if humanize:
            delay_seconds = self._calculate_delay(response_text)
            typing_duration = self._calculate_typing_duration(response_text)
            should_show_typing = self.typing_enabled

        # Determine if should use emoji (80% of the time)
        use_emoji = random.random() < 0.8

        # Suggest reactions for the customer's message
        suggested_reactions = self._get_suggested_reactions(context.intent)

        return GeneratedResponse(
            text=response_text,
            delay_seconds=delay_seconds,
            should_show_typing=should_show_typing,
            typing_duration=typing_duration,
            use_emoji=use_emoji,
            suggested_reactions=suggested_reactions,
        )

    def _select_template(self, context: ResponseContext) -> str:
        """Select appropriate template based on context"""
        message_lower = context.customer_message.lower()

        # High intent - specific templates
        if context.intent.level == IntentLevel.HIGH:
            if any(word in message_lower for word in ["precio", "costo", "cuánto"]):
                templates = self.templates["high_intent_price"]
            elif any(word in message_lower for word in ["pago", "pagar", "tarjeta"]):
                templates = self.templates["high_intent_payment"]
            elif any(word in message_lower for word in ["envío", "enviar", "entrega"]):
                templates = self.templates["high_intent_shipping"]
            elif any(word in message_lower for word in ["disponible", "stock", "hay"]):
                templates = self.templates["high_intent_stock"]
            else:
                # Default high intent
                templates = self.templates["high_intent_price"]

        # Medium intent
        elif context.intent.level == IntentLevel.MEDIUM:
            if any(word in message_lower for word in ["garantía", "garantia"]):
                templates = self.templates["medium_intent_warranty"]
            else:
                templates = self.templates["medium_intent_info"]

        # Low intent
        else:
            if any(word in message_lower for word in ["gracias", "thanks"]):
                templates = self.templates["low_intent_thanks"]
            else:
                templates = self.templates["low_intent_greeting"]

        # Select random template from list
        return random.choice(templates)

    def _fill_template(self, template: str, context: ResponseContext) -> str:
        """Fill template with actual data"""
        # This would be replaced with actual product data from database
        # For now, using placeholders

        replacements = {
            "{price}": "1,299",  # TODO: Get from product DB
            "{warranty_period}": "1 año",  # TODO: Get from product DB
            "{name}": context.customer_name or "amigo/a",
        }

        response = template
        for placeholder, value in replacements.items():
            response = response.replace(placeholder, value)

        return response

    def _calculate_delay(self, text: str) -> int:
        """Calculate realistic delay before responding"""
        # Base delay
        base_delay = random.uniform(self.min_delay, self.max_delay)

        # Add slight delay for longer messages
        length_factor = min(len(text) / 100, 2)  # Max 2 seconds extra

        total_delay = int(base_delay + length_factor)

        return total_delay

    def _calculate_typing_duration(self, text: str) -> int:
        """Calculate typing indicator duration based on message length"""
        if not self.typing_enabled:
            return 0

        # Simulate typing at configured speed
        chars = len(text)
        duration = chars / self.typing_speed

        # Add random variation (±20%)
        variation = random.uniform(0.8, 1.2)
        duration = duration * variation

        # Clamp between 2 and 10 seconds
        return int(max(2, min(10, duration)))

    def _get_suggested_reactions(self, intent: IntentResult) -> List[str]:
        """Get suggested emoji reactions based on intent"""
        reactions = {
            IntentLevel.HIGH: ["👍", "❤️", "🔥"],
            IntentLevel.MEDIUM: ["👍", "😊"],
            IntentLevel.LOW: ["👋", "😊"],
        }

        return reactions.get(intent.level, ["👍"])

    async def send_humanized_response(
        self,
        waha_client: Any,
        chat_id: str,
        response: GeneratedResponse,
    ) -> None:
        """
        Send response with human-like behavior

        Args:
            waha_client: WAHAClient instance
            chat_id: Chat ID to send message to
            response: GeneratedResponse to send
        """
        try:
            # Wait before responding (realistic delay)
            if response.delay_seconds > 0:
                logger.debug(f"Waiting {response.delay_seconds}s before responding...")
                await asyncio.sleep(response.delay_seconds)

            # Show typing indicator
            if response.should_show_typing:
                logger.debug(f"Showing typing for {response.typing_duration}s...")
                await waha_client.send_typing(
                    chat_id=chat_id,
                    duration=response.typing_duration,
                )
                await asyncio.sleep(response.typing_duration)

            # Send actual message
            logger.info(f"Sending response: {response.text[:50]}...")
            await waha_client.send_message(
                chat_id=chat_id,
                text=response.text,
            )

            logger.success("Response sent successfully!")

        except Exception as e:
            logger.error(f"Error sending humanized response: {e}")
            raise
