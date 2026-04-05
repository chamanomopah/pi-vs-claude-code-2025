#!/usr/bin/env python3
"""
Simple word counter script.
Counts words in a text file.
"""

import sys
import re


def count_words(text):
    """Count words in a text string."""
    # Split by whitespace and filter out empty strings
    words = re.findall(r'\b\w+\b', text.lower())
    return len(words)


def count_unique_words(text):
    """Count unique words in a text string."""
    words = re.findall(r'\b\w+\b', text.lower())
    return len(set(words))


def main():
    if len(sys.argv) < 2:
        print("Usage: python word_count.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        
        total_words = count_words(text)
        unique_words = count_unique_words(text)
        
        print(f"File: {filename}")
        print(f"Total words: {total_words}")
        print(f"Unique words: {unique_words}")
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
