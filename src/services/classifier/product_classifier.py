import logging
from typing import Optional

from services.classifier.categories import ProductCategory, get_category_keywords
from llm.config import get_llm, is_llm_available
from llm.prompts import create_classification_prompt

logger = logging.getLogger(__name__)


class ClassificationResult:
    """Classification result model."""
    
    def __init__(self, category: str, confidence: float, method: str):
        """
        Initialize classification result.
        
        Args:
            category: Classified category name
            confidence: Confidence score (0-1)
            method: Classification method used
        """
        self.category = category
        self.confidence = confidence
        self.method = method


class RuleBasedClassifier:
    """Rule-based product classifier using keyword matching."""
    
    def __init__(self):
        """Initialize rule-based classifier."""
        self.category_keywords = get_category_keywords()
    
    def classify_product(self, product_name: str) -> ClassificationResult:
        """
        Classify product using keyword matching rules.
        """
        product_lower = product_name.lower().strip()
        
        # Calculate scores for each category
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            
            for keyword in keywords:
                if keyword in product_lower:
                    # Weight by keyword length and position
                    weight = len(keyword) * 2
                    if f' {keyword} ' in f' {product_lower} ':
                        weight *= 2  # Exact word match bonus
                    if product_lower.startswith(keyword + ' '):
                        weight *= 1.5  # Beginning position bonus
                    score += weight
            
            # Store raw score
            category_scores[category] = score
        
        # Find best category
        if not category_scores or max(category_scores.values()) == 0:
            return ClassificationResult(
                category="Other",
                confidence=0.0,
                method="rule_based"
            )
        
        best_category = max(category_scores, key=category_scores.get)
        best_score = category_scores[best_category]
        
        # Calculate confidence based on match quality
        if best_score >= 30:  # Strong match
            confidence = 0.95
        elif best_score >= 20:  # Good match
            confidence = 0.85
        elif best_score >= 10:  # Decent match
            confidence = 0.70
        elif best_score >= 5:   # Weak match
            confidence = 0.50
        else:
            confidence = 0.30
        
        return ClassificationResult(
            category=best_category.value,
            confidence=confidence,
            method="rule_based"
        )


class HybridProductClassifier:
    """Hybrid classifier: rules first, LLM fallback for low confidence."""
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """
        Initialize the hybrid classifier.
        """
        self.llm_available = is_llm_available(groq_api_key)
        self.groq_api_key = groq_api_key
        
        if self.llm_available:
            try:
                self.llm = get_llm(groq_api_key, temperature=0.1)
                self._setup_llm_prompt()
                logger.info("LLM classification enabled")
            except Exception as e:
                logger.warning(f"Failed to initialize LLM: {e}")
                self.llm_available = False
        
        # Build rule-based classifier
        self.rule_classifier = RuleBasedClassifier()
        logger.info("Hybrid classifier initialized")
    
    def _setup_llm_prompt(self):
        """Setup LLM prompt for classification."""
        self.llm_prompt = create_classification_prompt()
    
    def classify_product(self, product_name: str) -> ClassificationResult:
        """
        Classify product using hybrid approach.
        """
        # Try rule-based classification first
        rule_result = self.rule_classifier.classify_product(product_name)
        
        # If rule-based has high confidence, use it
        if rule_result.confidence > 0.85:
            return ClassificationResult(
                category=rule_result.category,
                confidence=rule_result.confidence,
                method="rule_based"
            )
        
        # If LLM is available and rule-based confidence is low, use LLM
        if self.llm_available and rule_result.confidence <= 0.85:
            try:
                llm_result = self._classify_with_llm(product_name)
                return ClassificationResult(
                    category=llm_result.category,
                    confidence=llm_result.confidence,
                    method="llm"
                )
            except Exception as e:
                logger.warning(f"LLM classification failed: {e}, using rule-based result")
        
        # Fallback to rule-based result
        return ClassificationResult(
            category=rule_result.category,
            confidence=rule_result.confidence,
            method="rule_based"
        )
    
    def _classify_with_llm(self, product_name: str) -> ClassificationResult:
        """
        Classify using LLM.
        """
        try:
            response = self.llm.invoke(self.llm_prompt.format_messages(product_name=product_name))
            category_name = response.content.strip()
            
            # Map to enum
            try:
                category = ProductCategory(category_name)
                return ClassificationResult(
                    category=category.value,
                    confidence=0.9,  # High confidence for LLM
                    method="llm"
                )
            except ValueError:
                # If category not found, return Other
                return ClassificationResult(
                    category="Other",
                    confidence=0.5,
                    method="llm"
                )
                
        except Exception as e:
            raise Exception(f"LLM classification failed: {str(e)}")


def get_classifier(groq_api_key: Optional[str] = None) -> HybridProductClassifier:
    """
    Get classifier instance.
    """
    return HybridProductClassifier(groq_api_key)

