import re
from typing import List, Dict, Any

def tokenize_text_with_positions(text: str, vocab: Dict[str, int]) -> List[Dict[str, Any]]:
    """
    Tokenize input text using a simple word-based vocabulary and track positions.
    
    This function serves as the tokenization step in our LLM pipeline visualization.
    It breaks text into tokens, maps them to vocabulary IDs, and tracks their
    positions for highlighting in the UI.
    
    Args:
        text: Input text to tokenize
        vocab: Dictionary mapping tokens to integer IDs
        
    Returns:
        List of token dictionaries, each containing:
        - 'token': the actual token string
        - 'id': vocabulary ID (or vocab['<UNK>'] for unknown tokens)
        - 'start': character start position in original text
        - 'end': character end position in original text
    """
    if not text.strip():
        return []
    
    tokens = []
    token_matches = _find_token_matches(text)
    
    for token, start, end in token_matches:
        normalized = _normalize_token(token)
        token_id = vocab.get(normalized, vocab['<UNK>'])
        
        tokens.append({
            'token': token,
            'id': token_id,
            'start': start,
            'end': end
        })
    
    return tokens

def _normalize_token(token: str) -> str:
    """Helper: Convert token to lowercase and strip punctuation."""
    return re.sub(r'[^\w]', '', token.lower())

def _find_token_matches(text: str) -> List[tuple]:
    """Helper: Find all word tokens with their positions."""
    return [(match.group(), match.start(), match.end()) 
            for match in re.finditer(r'\b\w+\b', text)]