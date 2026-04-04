#!/usr/bin/env bash

# Test script for git_commit_report.py

echo "Test 1: Running with default settings (50 commits)"
python3 scripts/git_commit_report.py
echo ""
echo "---"
echo ""

echo "Test 2: Running with limited commits (5)"
python3 scripts/git_commit_report.py -n 5
echo ""
echo "---"
echo ""

echo "Test 3: Running with output to file"
python3 scripts/git_commit_report.py -n 3 -o test_report.txt
echo "Content of test_report.txt:"
cat test_report.txt
echo ""
echo "---"
echo ""

echo "Test 4: Running with help flag"
python3 scripts/git_commit_report.py --help
echo ""
echo "---"
echo ""

echo "Test 5: Check if script is executable"
ls -lh scripts/git_commit_report.py
echo ""

# Cleanup
rm -f test_report.txt

echo "All tests completed!"
