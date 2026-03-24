# Forge Challenge — Exploring the Complete LLM Internals Playground
# Implement the function below.
# Run tests with: pytest test_suite.py -v

import re
from typing import Dict

def prepare_input_text(raw_text: str, max_length: int = 2048) -> Dict[str, any]:
    """
    Validates, cleans, and truncates raw text for the tokenizer panel.
    
    This is the entry point to our four-stage LLM processing pipeline:
    tokenize → embed → attend → sample
    
    Args:
        raw_text: The input text to prepare
        max_length: Maximum character length before truncation
        
    Returns:
        Dict with 'processed_text' (str) and 'truncated' (bool) keys
        
    Raises:
        TypeError: If raw_text is not a string
        ValueError: If raw_text is empty
    """
    # YOUR CODE HERE
    # Step 1: Validate input type and check for empty text
    
    # YOUR CODE HERE  
    # Step 2: Remove HTML tags using regex pattern r'<[^>]+>'
    
    # YOUR CODE HERE
    # Step 3: Normalize whitespace (multiple spaces/newlines to single space)
    
    # YOUR CODE HERE
    # Step 4: Handle truncation at word boundaries if text exceeds max_length
    
    # YOUR CODE HERE
    # Step 5: Return dictionary with processed_text and truncated flag
    pass