import os
from pathlib import Path
from typing import Optional
from .mdcollections import MDCollections

def create_collections(path: Optional[str] = None) -> MDCollections:
    """
    Factory function to create and initialize an MDCollections instance.
    
    Args:
        path: Optional path to scan for collections. Defaults to "data/markdown"
        
    Returns:
        Initialized MDCollections instance
        
    Raises:
        ValueError: If path is None
    """
    if path is None:
        raise ValueError("Path cannot be None")
        
    # Expand ~ to home directory if present in path
    expanded_path = os.path.expanduser(path)
    return MDCollections(root_path=Path(expanded_path))

