#!/usr/bin/env python3
"""
Count duplicate files in a directory based on content hash.
Identifies files with identical content across the entire directory tree.
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple


def compute_file_hash(filepath: Path, chunk_size: int = 8192) -> str:
    """Compute SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError) as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return ""


def find_duplicates(directory: str) -> Tuple[Dict[str, List[Path]], int]:
    """
    Scan directory recursively and find duplicate files.
    
    Returns:
        Tuple of (hash_to_files dict, total_files_scanned)
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    hash_to_files: Dict[str, List[Path]] = defaultdict(list)
    total_files = 0
    
    # Recursively scan all files
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        for filename in files:
            filepath = root_path / filename
            if filepath.is_file():
                file_hash = compute_file_hash(filepath)
                if file_hash:  # Only add if hash was computed successfully
                    hash_to_files[file_hash].append(filepath)
                    total_files += 1
    
    return dict(hash_to_files), total_files


def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def print_duplicate_report(directory: str):
    """Print a comprehensive duplicate file report."""
    print(f"\n{'='*60}")
    print(f"DUPLICATE FILE ANALYSIS")
    print(f"{'='*60}")
    print(f"Scanning directory: {directory}\n")
    
    try:
        hash_to_files, total_files = find_duplicates(directory)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Find duplicates (files with same hash)
    duplicate_groups = {
        h: files for h, files in hash_to_files.items() if len(files) > 1
    }
    
    unique_files = len(hash_to_files)
    duplicate_count = sum(len(files) - 1 for files in duplicate_groups.values())
    total_duplicate_files = sum(len(files) for files in duplicate_groups.values())
    
    # Calculate wasted space
    wasted_space = 0
    for files in duplicate_groups.values():
        if len(files) > 1:
            file_size = files[0].stat().st_size
            wasted_space += file_size * (len(files) - 1)
    
    print(f"SUMMARY:")
    print(f"  Total files scanned:    {total_files}")
    print(f"  Unique files:           {unique_files}")
    print(f"  Duplicate files found:  {duplicate_count}")
    print(f"  Wasted space:           {format_size(wasted_space)}")
    print(f"  Duplicate groups:       {len(duplicate_groups)}")
    
    if duplicate_groups:
        print(f"\nDUPLICATE FILE GROUPS:")
        for i, (file_hash, files) in enumerate(sorted(
            duplicate_groups.items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        ), 1):
            file_size = files[0].stat().st_size
            print(f"\n  Group {i}: {len(files)} copies ({format_size(file_size)} each)")
            print(f"    Hash: {file_hash[:16]}...")
            for filepath in files:
                print(f"      - {filepath}")
    else:
        print(f"\n[*] No duplicate files found!")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = input("Enter directory path to scan: ").strip()
    
    print_duplicate_report(directory)
