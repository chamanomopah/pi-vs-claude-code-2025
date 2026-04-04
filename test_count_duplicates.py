#!/usr/bin/env python3
"""
Test script for count_duplicates.py
Runs 5 test cases as required by the 5-min-scripts skill.
"""

import os
import shutil
import subprocess
from pathlib import Path


def run_test(test_name: str, test_func):
    """Run a test case and display results."""
    print(f"\n{'#'*70}")
    print(f"TEST: {test_name}")
    print(f"{'#'*70}")
    test_func()


def test_1_empty_directory():
    """Test Case 1: Empty directory - should show 0 files."""
    test_dir = Path("test_data/empty_dir")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Created empty directory: {test_dir}")
    subprocess.run(["python", "count_duplicates.py", str(test_dir)])
    
    # Cleanup
    shutil.rmtree(test_dir)


def test_2_all_unique_files():
    """Test Case 2: Directory with all unique files - should show 0 duplicates."""
    test_dir = Path("test_data/unique_files")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Create unique files with different content
    (test_dir / "file1.txt").write_text("This is file 1 with unique content.")
    (test_dir / "file2.txt").write_text("This is file 2 with different content.")
    (test_dir / "file3.txt").write_text("Completely different content here.")
    (test_dir / "readme.md").write_text("# Readme\n\nSome documentation.")
    (test_dir / "data.json").write_text('{"key": "value"}')
    
    print(f"Created 5 unique files in: {test_dir}")
    subprocess.run(["python", "count_duplicates.py", str(test_dir)])
    
    # Cleanup
    shutil.rmtree(test_dir)


def test_3_some_duplicates():
    """Test Case 3: Directory with some exact duplicate files - should identify duplicates."""
    test_dir = Path("test_data/some_duplicates")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Create unique files
    (test_dir / "unique1.txt").write_text("This file is unique.")
    (test_dir / "unique2.txt").write_text("Another unique file.")
    
    # Create duplicate files with same content
    content1 = "This is duplicate content."
    (test_dir / "duplicate_a.txt").write_text(content1)
    (test_dir / "duplicate_b.txt").write_text(content1)
    (test_dir / "copy_of_duplicate.txt").write_text(content1)
    
    # Another duplicate set
    content2 = "Another duplicate set content."
    (test_dir / "photo_copy1.jpg.txt").write_text(content2)
    (test_dir / "photo_copy2.jpg.txt").write_text(content2)
    
    print(f"Created files with 2 duplicate groups in: {test_dir}")
    subprocess.run(["python", "count_duplicates.py", str(test_dir)])
    
    # Cleanup
    shutil.rmtree(test_dir)


def test_4_multiple_duplicate_groups():
    """Test Case 4: Multiple groups of duplicates - should handle multiple duplicate sets."""
    test_dir = Path("test_data/multiple_groups")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Group 1: 3 copies
    group1_content = "Group 1 duplicate content."
    for i in range(3):
        (test_dir / f"group1_file{i}.txt").write_text(group1_content)
    
    # Group 2: 4 copies
    group2_content = "Group 2 has different content."
    for i in range(4):
        (test_dir / f"group2_copy{i}.dat").write_text(group2_content)
    
    # Group 3: 2 copies
    group3_content = "Third group content here."
    (test_dir / "group3_a.txt").write_text(group3_content)
    (test_dir / "group3_b.txt").write_text(group3_content)
    
    # Group 4: 5 copies
    group4_content = "Fourth group with most copies!"
    for i in range(5):
        (test_dir / f"group4_{i}.bin").write_text(group4_content)
    
    # Unique file
    (test_dir / "lone_wolf.txt").write_text("I am unique!")
    
    print(f"Created 4 duplicate groups + 1 unique file in: {test_dir}")
    subprocess.run(["python", "count_duplicates.py", str(test_dir)])
    
    # Cleanup
    shutil.rmtree(test_dir)


def test_5_deep_nested_structure():
    """Test Case 5: Deep nested directory structure - should recursively scan subdirectories."""
    test_dir = Path("test_data/nested_structure")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Create nested structure
    dirs_to_create = [
        "level1",
        "level1/level2a",
        "level1/level2b",
        "level1/level2a/level3a",
        "level1/level2a/level3b",
        "level1/level2b/level3c",
        "level1/level2a/level3a/level4",
        "level1/level2a/level3a/level4/level5",
    ]
    
    for dir_path in dirs_to_create:
        (test_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Place duplicates across different nesting levels
    dup_content = "Cross-directory duplicate!"
    (test_dir / "root.txt").write_text(dup_content)
    (test_dir / "level1" / "file.txt").write_text(dup_content)
    (test_dir / "level1" / "level2a" / "deep.txt").write_text(dup_content)
    (test_dir / "level1" / "level2a" / "level3a" / "level4" / "level5" / "very_deep.txt").write_text(dup_content)
    
    # Another duplicate group
    dup_content2 = "Another cross-folder duplicate!"
    (test_dir / "level1" / "data.txt").write_text(dup_content2)
    (test_dir / "level1" / "level2b" / "data_copy.txt").write_text(dup_content2)
    (test_dir / "level1" / "level2a" / "level3b" / "info.txt").write_text(dup_content2)
    
    # Some unique files in various locations
    (test_dir / "level1" / "unique.txt").write_text("Unique at level 1")
    (test_dir / "level1" / "level2a" / "level3a" / "level4" / "unique_deep.txt").write_text("Unique at level 4")
    (test_dir / "level1" / "level2b" / "level3c" / "special.txt").write_text("Unique at level 3c")
    
    print(f"Created deeply nested structure with duplicates across levels in: {test_dir}")
    subprocess.run(["python", "count_duplicates.py", str(test_dir)])
    
    # Cleanup
    shutil.rmtree(test_dir)


def main():
    """Run all test cases."""
    print("="*70)
    print("DUPLICATE FILE COUNTER - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Test 1: Empty Directory", test_1_empty_directory),
        ("Test 2: All Unique Files", test_2_all_unique_files),
        ("Test 3: Some Duplicate Files", test_3_some_duplicates),
        ("Test 4: Multiple Duplicate Groups", test_4_multiple_duplicate_groups),
        ("Test 5: Deep Nested Structure", test_5_deep_nested_structure),
    ]
    
    for test_name, test_func in tests:
        run_test(test_name, test_func)
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    main()
