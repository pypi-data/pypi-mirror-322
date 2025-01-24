import pytest
from reasoning_gym.arithmetic import ChainSum, ChainSumConfig


def test_chain_sum_config_validation():
    """Test that invalid configs raise appropriate errors"""
    with pytest.raises(AssertionError):
        config = ChainSumConfig(min_terms=0)
        config.validate()
    
    with pytest.raises(AssertionError):
        config = ChainSumConfig(min_terms=3, max_terms=2)
        config.validate()


def test_chain_sum_deterministic():
    """Test that dataset generates same items with same seed"""
    config = ChainSumConfig(seed=42, size=10)
    dataset1 = ChainSum(config)
    dataset2 = ChainSum(config)
    
    for i in range(len(dataset1)):
        assert dataset1[i] == dataset2[i]


def test_chain_sum_items():
    """Test basic properties of generated items"""
    config = ChainSumConfig(
        min_terms=2,
        max_terms=4,
        min_digits=1,
        max_digits=2,
        size=100,
        seed=42
    )
    dataset = ChainSum(config)
    
    for i in range(len(dataset)):
        item = dataset[i]
        assert isinstance(item, dict)
        assert "question" in item
        assert "answer" in item
        assert "metadata" in item
        
        # Verify only + and - are used
        expression = item["metadata"]["expression"]
        assert all(op in ["+", "-", " "] or op.isdigit() for op in expression)
        
        # Verify the answer matches the expression
        answer = eval(expression)  # Safe here as we control the expression
        assert str(answer) == item["answer"]


def test_chain_sum_number_ranges():
    """Test that generated numbers respect digit constraints"""
    # Test 3-digit numbers
    config = ChainSumConfig(
        min_terms=2,
        max_terms=2,  # Fix to 2 terms for easier testing
        min_digits=3,  # Should generate numbers >= 100
        max_digits=3,  # Should generate numbers <= 999
        size=50,
        seed=42
    )
    dataset = ChainSum(config)
    
    for i in range(len(dataset)):
        item = dataset[i]
        expression = item["metadata"]["expression"]
        numbers = [int(n) for n in expression.split() if n.isdigit()]
        for num in numbers:
            if config.allow_negation:
                assert -999 <= num <= 999, f"Number {num} outside valid range for 3 digits"
            else:
                assert 100 <= num <= 999, f"Number {num} outside valid range for 3 digits"


    # Test 1-digit numbers
    config = ChainSumConfig(
        min_terms=2,
        max_terms=2,
        min_digits=1,
        max_digits=1,
        size=50,
        seed=42
    )
    dataset = ChainSum(config)
    for i in range(len(dataset)):
        item = dataset[i]
        expression = item["metadata"]["expression"]
        numbers = [int(n) for n in expression.split() if n.isdigit()]
        for num in numbers:
            if config.allow_negation:
                assert -9 <= num <= 9, f"Number {num} outside valid range for 1 digit"
            else:
                assert 0 <= num <= 9, f"Number {num} outside valid range for 1 digit"

def test_chain_sum_negation():
    """Test that allow_negation controls number ranges"""
    config = ChainSumConfig(
        min_terms=2,
        max_terms=2,
        min_digits=2,
        max_digits=2,
        size=100,
        seed=42,
        allow_negation=True
    )
    dataset = ChainSum(config)
    
    # Track if we see both positive and negative numbers
    has_positive = False
    has_negative = False
    
    for i in range(len(dataset)):
        item = dataset[i]
        expression = item["metadata"]["expression"]
        numbers = [int(n) for n in expression.split() if n.isdigit() or (n.startswith('-') and n[1:].isdigit())]
        
        for num in numbers:
            if num > 0:
                has_positive = True
            if num < 0:
                has_negative = True
                
    # With enough samples and allow_negation=True, we should see both positive and negative numbers
    assert has_positive and has_negative, "Expected both positive and negative numbers with allow_negation=True"


def test_chain_sum_iteration():
    """Test that iteration respects dataset size"""
    config = ChainSumConfig(
        min_terms=2,
        max_terms=2,
        size=5,  # Small size for testing
        seed=42
    )
    dataset = ChainSum(config)
    
    # Test manual iteration
    items = []
    for item in dataset:
        items.append(item)
    assert len(items) == config.size, "Iterator should yield exactly size items"
    
    # Test list conversion
    items = list(dataset)
    assert len(items) == config.size, "Iterator should yield exactly size items"
    
    # Test multiple iterations
    first_items = list(dataset)
    second_items = list(dataset)
    assert first_items == second_items, "Multiple iterations should yield same items"
