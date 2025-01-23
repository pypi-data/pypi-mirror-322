from typing import Optional, Union
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from .markdown_server import MDServer  # Import directly from the module file


def serve_markdown(collections_path: str) -> None:
    """
    Legacy function to maintain backward compatibility.
    Creates an MDServer instance and serves the markdown content.
    
    Args:
        collections_path: Path to the collections directory. Can be a string or Path object.
    """
    server = MDServer(collections_path=collections_path)
    server.serve_markdown()
