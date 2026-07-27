import unittest
from src.ai.intent_classifier import IntentClassifier

class TestIntentClassifier(unittest.TestCase):

    def test_stock_check(self):
        result = IntentClassifier.classify("Is there stock left for milk?")
        self.assertIn(result["intent"], ["product_search", "stock_check"])
        self.assertGreater(result["confidence"], 0)

    def test_create_order(self):
        result = IntentClassifier.classify("I want to buy 2 apples")
        self.assertEqual(result["intent"], "create_order")
        self.assertGreater(result["confidence"], 0)

    def test_store_info(self):
        result = IntentClassifier.classify("What are your store timing and address?")
        self.assertEqual(result["intent"], "store_info")

    def test_unknown_intent(self):
        result = IntentClassifier.classify("xyz123abc")
        self.assertEqual(result["intent"], "unknown")
        self.assertEqual(result["confidence"], 0)

if __name__ == "__main__":
    unittest.main()
