#!/usr/bin/env python3
"""
Test script to verify remarks file generation without user interaction
"""
import sys
import os
from pathlib import Path

# Mock input to always say 'no' to interactions
original_input = input
responses = iter(['n', 'n', 'n', 'n'])  # No to edit, yes to happy, etc.

def mock_input(prompt=""):
    print(prompt, end="", flush=True)
    response = next(responses, 'n')
    print(response)
    return response

# Monkey-patch input
import builtins
builtins.input = mock_input

# Now run interactive
import interactive

# Test with simple topic
sys.argv = ['test_interactive.py', '--topic', 'test-remarks', '--skeleton', '/dev/null']

try:
    interactive.main()
except StopIteration:
    print("\n[Test] Ran out of mock responses - that's OK")
except Exception as e:
    print(f"\n[Test] Error: {e}")
    import traceback
    traceback.print_exc()

# Check if remarks file was created
from src.config import Config
topic = 'test-remarks'
output_dir = Config.get_topic_output_dir(topic)
remarks_file = Path(output_dir) / "remarks.md"

print(f"\n[Test] Output directory: {output_dir}")
print(f"[Test] Remarks file path: {remarks_file}")
print(f"[Test] Remarks file exists: {remarks_file.exists()}")

if remarks_file.exists():
    print(f"[Test] ✅ SUCCESS - Remarks file was created!")
    with open(remarks_file) as f:
        content = f.read()
    print(f"[Test] Remarks file size: {len(content)} bytes")
else:
    print(f"[Test] ❌ FAIL - Remarks file was NOT created")
    print(f"[Test] Files in output directory:")
    for f in Path(output_dir).glob("*"):
        print(f"[Test]   - {f.name}")
