import pytest
from challenge import prepare_input_text

def test_prepare_input_text_happy_path():
    """Test normal text processing with HTML removal and whitespace normalization."""
    raw_text = "<p>Hello    world!\n\nThis is a test.</p>"
    result = prepare_input_text(raw_text, max_length=100)
    
    assert result["processed_text"] == "Hello world! This is a test."
    assert result["truncated"] == False
    assert isinstance(result, dict)
    assert len(result) == 2

def test_prepare_input_text_truncation_edge_case():
    """Test truncation at word boundary when text exceeds max_length."""
    long_text = "The quick brown fox jumps over the lazy dog again and again"
    result = prepare_input_text(long_text, max_length=30)
    
    # Should truncate at word boundary, not mid-word
    assert result["processed_text"] == "The quick brown fox jumps over"
    assert result["truncated"] == True
    assert len(result["processed_text"]) <= 30
    assert not result["processed_text"].endswith(" ")

def test_prepare_input_text_empty_string_failure():
    """Test that empty string raises ValueError."""
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        prepare_input_text("")

def test_prepare_input_text_wrong_type_failure():
    """Test that non-string input raises TypeError."""
    with pytest.raises(TypeError, match="Expected string, got"):
        prepare_input_text(123)

def test_prepare_input_text_html_removal():
    """Test comprehensive HTML tag removal."""
    html_text = "<div><span>Hello</span> <b>world</b>!</div>"
    result = prepare_input_text(html_text)
    
    assert result["processed_text"] == "Hello world!"
    assert "<" not in result["processed_text"]
    assert ">" not in result["processed_text"]

def test_prepare_input_text_whitespace_normalization():
    """Test that various whitespace patterns are normalized to single spaces."""
    messy_text = "Hello\t\t\tworld\n\n\n   test"
    result = prepare_input_text(messy_text)
    
    assert result["processed_text"] == "Hello world test"
    assert "\n" not in result["processed_text"]
    assert "\t" not in result["processed_text"]
    assert "  " not in result["processed_text"]