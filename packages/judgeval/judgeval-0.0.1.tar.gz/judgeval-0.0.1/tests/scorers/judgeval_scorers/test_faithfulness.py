import pytest
from judgeval.scorers.judgeval_scorers.faithfulness import FaithfulnessScorer
from judgeval.constants import APIScorer


class TestFaithfulnessScorer:
    def test_init(self):
        # Test initialization with valid threshold
        threshold = 0.7
        scorer = FaithfulnessScorer(threshold=threshold)
        
        assert scorer.threshold == threshold
        assert scorer.score_type == APIScorer.FAITHFULNESS

    def test_init_invalid_threshold(self):
        # Test initialization with invalid threshold values
        with pytest.raises(ValueError):
            FaithfulnessScorer(threshold=-0.1)
        
        with pytest.raises(ValueError):
            FaithfulnessScorer(threshold=1.1)

    def test_name_property(self):
        # Test the __name__ property
        scorer = FaithfulnessScorer(threshold=0.5)
        assert scorer.__name__ == "Faithfulness"
        