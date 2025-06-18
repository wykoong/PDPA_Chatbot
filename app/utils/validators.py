from typing import List

ALLOWED_KEYWORDS: List[str] = [
    "personal data privacy", "data protection", "data privacy", "privacy law", "GDPR", "PDPA",
    "ai governance", "AI governance", "AI ethics", "AI law", "AI regulation", "artificial intelligence governance"
]

def is_in_scope(question: str) -> bool:
    """
    Check if the question is within the allowed scope.
    
    Args:
        question: The user's question
        
    Returns:
        bool: True if the question is in scope, False otherwise
    """
    q = question.lower()
    return any(keyword.lower() in q for keyword in ALLOWED_KEYWORDS)
