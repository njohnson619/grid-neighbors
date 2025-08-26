import os
import sys
from pathlib import Path

import pytest

# Add the project source code to the python path so the tests have direct access.
# Note: this assumes the tests directory is at the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(project_root, "src"))

# also add top level test utilities
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
