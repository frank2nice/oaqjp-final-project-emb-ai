"""
Unit tests for testing Emotion Detection application
"""

import unittest
from EmotionDetection import emotion_detector

class TestEmotionDetector(unittest.TestCase):
    """
    Test class for the emotion_detector function
    """
    
    def test_emotion_detector(self):
        """
        Test emotion_detector with different statements and expected dominant emotions
        """
        # Test case 1: Joy
        result1 = emotion_detector("I am glad this happened")
        self.assertEqual(result1['dominant_emotion'], 'joy')
        
        # Test case 2: Anger
        result2 = emotion_detector("I am really mad about this")
        self.assertEqual(result2['dominant_emotion'], 'anger')
        
        # Test case 3: Disgust
        result3 = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result3['dominant_emotion'], 'disgust')
        
        # Test case 4: Sadness
        result4 = emotion_detector("I am so sad about this")
        self.assertEqual(result4['dominant_emotion'], 'sadness')
        
        # Test case 5: Fear
        result5 = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result5['dominant_emotion'], 'fear')

if __name__ == '__main__':
    unittest.main()