"""
Add the source directory to sys.path so the tests can import everything.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
