#!/usr/bin/env python3
"""Test script for the restaurant message classifier"""

import os
from dotenv import load_dotenv
from classifier import classify_message

load_dotenv()

def test_classification():
    test_messages = [
        "Lampu di toilet mati dan pelayan tidak menanggapi",
        "Makanannya enak banget, tolong sampaikan ke chef ya!",
        "Ada tumpahan minyak di lantai, takutnya orang terpeleset!",
        "Tagihan saya salah dan pelayan tidak bisa bantu"
    ]
    
    print("🧪 Testing Restaurant Message Classifier\n")
    
    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}: {message}")
        try:
            result = classify_message(message)
            print(f"  Urgency: {result['urgency']}")
            print(f"  Groups: {', '.join(result['groups'])}")
            if 'error' in result:
                print(f"  Error: {result['error']}")
        except Exception as e:
            print(f"  Error: {e}")
        print()

if __name__ == "__main__":
    test_classification()
