"""
Intent Classifier - Phase II: Automatización
Classifies customer messages by intent level
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger

from sentinel.config import settings


class IntentLevel(str, Enum):
    """Intent level classification"""

    HIGH = "high"  # Ready to buy: precio, pago, envío
    MEDIUM = "medium"  # Interested but needs info: garantía, specs
    LOW = "low"  # Just browsing or spam: hola, thanks


@dataclass
class IntentResult:
    """Result of intent classification"""

    level: IntentLevel
    confidence: float
    keywords_matched: List[str]
    suggested_action: str


class IntentClassifier:
    """Classifies customer messages to prioritize responses"""

    def __init__(self):
        self.high_intent_keywords = settings.high_intent_keywords_list
        self.low_intent_keywords = settings.low_intent_keywords_list
        self.high_threshold = settings.INTENT_HIGH_THRESHOLD
        self.medium_threshold = settings.INTENT_MEDIUM_THRESHOLD

    def classify(self, message: str, context: Optional[List[str]] = None) -> IntentResult:
        """
        Classify message intent

        Args:
            message: The customer message text
            context: Optional list of previous messages in conversation

        Returns:
            IntentResult with level, confidence, and suggested action
        """
        message_lower = message.lower()
        matched_keywords = []

        # Check for high intent keywords
        high_intent_score = 0
        for keyword in self.high_intent_keywords:
            if keyword in message_lower:
                high_intent_score += 1
                matched_keywords.append(keyword)

        # Check for low intent keywords
        low_intent_score = 0
        for keyword in self.low_intent_keywords:
            if keyword in message_lower:
                low_intent_score += 1

        # Calculate confidence and determine level
        total_keywords = len(self.high_intent_keywords) + len(self.low_intent_keywords)

        # High intent detection
        if high_intent_score > 0:
            confidence = min(high_intent_score / 3, 1.0)  # Max 3 keywords = 100%

            if confidence >= self.high_threshold:
                return IntentResult(
                    level=IntentLevel.HIGH,
                    confidence=confidence,
                    keywords_matched=matched_keywords,
                    suggested_action="immediate_response",
                )

        # Low intent detection (spam, greetings)
        if low_intent_score > 0 and high_intent_score == 0:
            if len(message.split()) <= 3:  # Short messages
                return IntentResult(
                    level=IntentLevel.LOW,
                    confidence=0.7,
                    keywords_matched=[],
                    suggested_action="automated_greeting",
                )

        # Check for question indicators
        question_indicators = ["?", "cuánto", "cómo", "dónde", "cuándo", "qué", "por qué"]
        has_question = any(indicator in message_lower for indicator in question_indicators)

        # Medium intent (questions, technical inquiries)
        if has_question or (high_intent_score > 0 and high_intent_score < 2):
            confidence = 0.6 if has_question else 0.5
            return IntentResult(
                level=IntentLevel.MEDIUM,
                confidence=confidence,
                keywords_matched=matched_keywords,
                suggested_action="assign_to_expert",
            )

        # Default to medium intent
        return IntentResult(
            level=IntentLevel.MEDIUM,
            confidence=0.5,
            keywords_matched=matched_keywords,
            suggested_action="standard_response",
        )

    def should_auto_respond(self, intent: IntentResult) -> bool:
        """Determine if message should trigger automatic response"""
        if not settings.ENABLE_AUTO_RESPONSE:
            return False

        # Always auto-respond to high intent
        if intent.level == IntentLevel.HIGH:
            return True

        # Auto-respond to medium intent if confidence is high enough
        if intent.level == IntentLevel.MEDIUM and intent.confidence >= 0.7:
            return True

        # Auto-respond to low intent with automated greeting
        if intent.level == IntentLevel.LOW:
            return True

        return False

    def get_priority_score(self, intent: IntentResult) -> int:
        """Get priority score for queue management (1-10, 10 is highest)"""
        base_scores = {
            IntentLevel.HIGH: 10,
            IntentLevel.MEDIUM: 5,
            IntentLevel.LOW: 1,
        }

        base_score = base_scores[intent.level]

        # Adjust by confidence
        adjusted_score = int(base_score * intent.confidence)

        return max(1, min(10, adjusted_score))
