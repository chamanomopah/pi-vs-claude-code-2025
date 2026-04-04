#!/usr/bin/env python3
"""
Git Commit Report Generator
A simple script to generate a readable report from git log output.
"""

import subprocess
import sys
from datetime import datetime
from typing import List, Dict


def get_git_log(limit: int = 50) -> List[Dict[str, str]]:
    """
    Get git log entries as structured data.
    
    Args:
        limit: Maximum number of commits to retrieve
        
    Returns:
        List of dictionaries containing commit information
    """
    try:
        # Get git log in a parseable format
        cmd = [
            'git', 'log',
            f'-{limit}',
            '--pretty=format:%H|%an|%ae|%ad|%s',
            '--date=short'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 5:
                commits.append({
                    'hash': parts[0][:8],  # Short hash
                    'author': parts[1],
                    'email': parts[2],
                    'date': parts[3],
                    'message': parts[4]
                })
        
        return commits
    
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git is not available.", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Git is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)


def generate_report(commits: List[Dict[str, str]], repo_path: str = None) -> str:
    """
    Generate a readable report from commit data.
    
    Args:
        commits: List of commit dictionaries
        repo_path: Optional repository path to display
        
    Returns:
        Formatted report string
    """
    if not commits:
        return "No commits found."
    
    lines = []
    
    # Header
    lines.append("=" * 80)
    lines.append("GIT COMMIT REPORT")
    lines.append("=" * 80)
    
    if repo_path:
        lines.append(f"Repository: {repo_path}")
    lines.append(f"Total commits: {len(commits)}")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # Author summary
    authors = {}
    for commit in commits:
        author = commit['author']
        authors[author] = authors.get(author, 0) + 1
    
    lines.append("-" * 80)
    lines.append("COMMITS BY AUTHOR:")
    for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {author}: {count} commit(s)")
    lines.append("")
    
    # Commit details
    lines.append("-" * 80)
    lines.append("COMMIT HISTORY:")
    lines.append("")
    
    for i, commit in enumerate(commits, 1):
        lines.append(f"[{i}] {commit['hash']}  |  {commit['date']}  |  {commit['author']}")
        lines.append(f"    {commit['message']}")
        lines.append("")
    
    lines.append("=" * 80)
    
    return '\n'.join(lines)


def get_repo_path() -> str:
    """Get the current git repository path."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Unknown"


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate a readable git commit report'
    )
    parser.add_argument(
        '-n', '--number',
        type=int,
        default=50,
        help='Number of commits to show (default: 50)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output to file instead of stdout'
    )
    
    args = parser.parse_args()
    
    # Get commit data
    commits = get_git_log(limit=args.number)
    repo_path = get_repo_path()
    
    # Generate report
    report = generate_report(commits, repo_path)
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
