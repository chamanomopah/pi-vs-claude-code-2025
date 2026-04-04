# Duplicate File Counter - Test Results

## Overview
Python script to identify and count duplicate files based on content hash (SHA256).

## Features
- **Content-based detection**: Uses SHA256 hash to identify exact duplicates
- **Recursive scanning**: Scans all subdirectories
- **Detailed reporting**: Shows total files, unique files, duplicates, and wasted space
- **Grouped results**: Lists all duplicate file groups with paths

## Test Results

### ✅ Test 1: Empty Directory
**Expected**: 0 files scanned, 0 duplicates
**Result**: 
```
Total files scanned:    0
Unique files:           0
Duplicate files found:  0
Wasted space:           0.0 B
Duplicate groups:       0
```
**Status**: PASSED

---

### ✅ Test 2: All Unique Files
**Setup**: 5 files with different content
**Expected**: 0 duplicates
**Result**:
```
Total files scanned:    5
Unique files:           5
Duplicate files found:  0
Wasted space:           0.0 B
Duplicate groups:       0
```
**Status**: PASSED

---

### ✅ Test 3: Some Duplicate Files
**Setup**: 7 total files with 2 duplicate groups
- Group 1: 3 copies of "This is duplicate content."
- Group 2: 2 copies of "Another duplicate set content."
- 2 unique files

**Result**:
```
Total files scanned:    7
Unique files:           4
Duplicate files found:  3
Wasted space:           82.0 B
Duplicate groups:       2

Group 1: 3 copies (26.0 B each)
  - copy_of_duplicate.txt
  - duplicate_a.txt
  - duplicate_b.txt

Group 2: 2 copies (30.0 B each)
  - photo_copy1.jpg.txt
  - photo_copy2.jpg.txt
```
**Status**: PASSED

---

### ✅ Test 4: Multiple Duplicate Groups
**Setup**: 15 total files with 4 duplicate groups + 1 unique
- Group 1: 3 copies
- Group 2: 4 copies
- Group 3: 2 copies
- Group 4: 5 copies

**Result**:
```
Total files scanned:    15
Unique files:           5
Duplicate files found:  10
Wasted space:           287.0 B
Duplicate groups:       4

Group 1: 5 copies (30.0 B each)
Group 2: 4 copies (30.0 B each)
Group 3: 3 copies (26.0 B each)
Group 4: 2 copies (25.0 B each)
```
**Status**: PASSED

---

### ✅ Test 5: Deep Nested Structure
**Setup**: Files across 5 directory levels with duplicates scattered throughout
- Root to level5: 4 copies of "Cross-directory duplicate!"
- Across different branches: 3 copies of "Another cross-folder duplicate!"
- 3 unique files at different levels

**Result**:
```
Total files scanned:    10
Unique files:           5
Duplicate files found:  5
Wasted space:           140.0 B
Duplicate groups:       2

Group 1: 4 copies (26.0 B each)
  - root.txt
  - level1/file.txt
  - level1/level2a/deep.txt
  - level1/level2a/level3a/level4/level5/very_deep.txt

Group 2: 3 copies (31.0 B each)
  - level1/data.txt
  - level1/level2a/level3b/info.txt
  - level1/level2b/data_copy.txt
```
**Status**: PASSED

---

## Usage

```bash
# Interactive mode
python count_duplicates.py

# Direct mode
python count_duplicates.py /path/to/directory

# Run all tests
python test_count_duplicates.py
```

## Key Features Demonstrated
1. ✅ Handles empty directories gracefully
2. ✅ Correctly identifies unique files
3. ✅ Finds duplicate groups of any size
4. ✅ Processes multiple duplicate groups in one scan
5. ✅ Recursively scans deeply nested directory structures
6. ✅ Calculates wasted storage space
7. ✅ Shows SHA256 hash for verification
8. ✅ Provides clear, formatted output

## Files Created
- `count_duplicates.py` - Main script (127 lines)
- `test_count_duplicates.py` - Test suite with 5 test cases
