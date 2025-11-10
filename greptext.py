#!/usr/bin/env python3
import subprocess
import sys

if len(sys.argv) != 3:
    print("Usage: python3 grep_simple.py <search_term> <filename>")
    sys.exit(1)

search_term = sys.argv[1]
filename = sys.argv[2]

# Use -F for literal string match, and -- to avoid issues if filename starts with '-'
result = subprocess.run(
    ["grep", "-F", "--", search_term, filename],
    capture_output=True,
    text=True
)

# Print matching lines (full lines containing the term)
print(result.stdout, end="")

# Forward any errors (e.g., file not found)
if result.stderr:
    print(result.stderr, file=sys.stderr, end="")