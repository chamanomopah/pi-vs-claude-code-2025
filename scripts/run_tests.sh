#!/usr/bin/env bash
cd /c/Users/JOSE/.claude/.IMPLEMENTATION/projects/B-software/H-minimum-orquestration/pi-vs-claude-code

echo "Test 1: Running with default settings (50 commits)"
python scripts/git_commit_report.py
echo ""
echo "---"
echo ""

echo "Test 2: Running with limited commits (5)"
python scripts/git_commit_report.py -n 5
echo ""
echo "---"
echo ""

echo "Test 3: Running with output to file"
python scripts/git_commit_report.py -n 3 -o test_report.txt
echo "Content of test_report.txt:"
cat test_report.txt
echo ""
echo "---"
echo ""

echo "Test 4: Running with help flag"
python scripts/git_commit_report.py --help
echo ""
echo "---"
echo ""

echo "Test 5: Check if script is executable"
ls -lh scripts/git_commit_report.py
echo ""

# Cleanup
rm -f test_report.txt

echo "All tests completed!"
