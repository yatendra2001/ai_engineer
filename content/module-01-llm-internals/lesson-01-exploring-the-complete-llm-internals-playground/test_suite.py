import pytest
from challenge import tokenize_text_with_positions

def test_basic_tokenization():
    """Test happy path with known vocabulary tokens."""
    vocab = {
        'hello': 1,
        'world': 2, 
        'the': 3,
        '<UNK>': 0
    }
    text = "Hello world"
    
    result = tokenize_text_with_positions(text, vocab)
    
    expected = [
        {'token': 'Hello', 'id': 1, 'start': 0, 'end': 5},
        {'token': 'world', 'id': 2, 'start': 6, 'end': 11}
    ]
    
    assert len(result) == 2
    assert result[0]['token'] == 'Hello'
    assert result[0]['id'] == 1
    assert result[0]['start'] == 0
    assert result[0]['end'] == 5
    assert result[1]['token'] == 'world'
    assert result[1]['id'] == 2
    assert result[1]['start'] == 6
    assert result[1]['end'] == 11

def test_unknown_tokens():
    """Test edge case with tokens not in vocabulary."""
    vocab = {
        'hello': 1,
        '<UNK>': 0
    }
    text = "hello xyz unknown"
    
    result = tokenize_text_with_positions(text, vocab)
    
    assert len(result) == 3
    assert result[0]['id'] == 1  # 'hello' is known
    assert result[1]['id'] == 0  # 'xyz' is unknown -> <UNK>
    assert result[2]['id'] == 0  # 'unknown' is unknown -> <UNK>
    assert result[1]['token'] == 'xyz'
    assert result[2]['token'] == 'unknown'

def test_empty_text_failure():
    """Test failure case with empty input."""
    vocab = {'hello': 1, '<UNK>': 0}
    text = ""
    
    result = tokenize_text_with_positions(text, vocab)
    
    assert result == []

def test_punctuation_and_spacing():
    """Test handling of punctuation and multiple spaces."""
    vocab = {
        'hello': 1,
        'world': 2,
        '<UNK>': 0
    }
    text = "Hello,  world!"
    
    result = tokenize_text_with_positions(text, vocab)
    
    assert len(result) == 2
    assert result[0]['token'] == 'Hello'
    assert result[0]['start'] == 0
    assert result[0]['end'] == 5
    assert result[1]['token'] == 'world'
    assert result[1]['start'] == 8
    assert result[1]['end'] == 13