# Forge Challenge — Exploring the Complete LLM Internals Playground
# Implement the function below.
# Run tests with: pytest test_suite.py -v

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
        
    Example:
        >>> vocab = {'hello': 1, 'world': 2, '<UNK>': 0}
        >>> tokenize_text_with_positions('hello world', vocab)
        [{'token': 'hello', 'id': 1, 'start': 0, 'end': 5},
         {'token': 'world', 'id': 2, 'start': 6, 'end': 11}]
    """
    # YOUR CODE HERE
    # Hint: Use regex to find word boundaries and track positions
    # Handle unknown tokens by mapping to vocab['<UNK>']
    pass

def _normalize_token(token: str) -> str:
    """Helper: Convert token to lowercase and strip punctuation."""
    return re.sub(r'[^\w]', '', token.lower())

def _find_token_matches(text: str) -> List[tuple]:
    """Helper: Find all word tokens with their positions."""
    return [(match.group(), match.start(), match.end()) 
            for match in re.finditer(r'\b\w+\b', text)]