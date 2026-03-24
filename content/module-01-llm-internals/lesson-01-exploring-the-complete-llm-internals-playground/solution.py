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
    # Step 1: Validate input type and check for empty text
    if not isinstance(raw_text, str):
        raise TypeError(f"Expected string, got {type(raw_text)}")
    
    if len(raw_text) == 0:
        raise ValueError("Input text cannot be empty")
    
    # Step 2: Remove HTML tags using regex
    processed = re.sub(r'<[^>]+>', '', raw_text)
    
    # Step 3: Normalize whitespace (multiple spaces/newlines to single space)
    processed = re.sub(r'\s+', ' ', processed).strip()
    
    # Step 4: Handle truncation at word boundaries if text exceeds max_length
    truncated = len(processed) > max_length
    if truncated:
        processed = processed[:max_length].rsplit(' ', 1)[0]
    
    # Step 5: Return dictionary with processed_text and truncated flag
    return {
        "processed_text": processed,
        "truncated": truncated
    }