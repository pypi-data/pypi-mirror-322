from pathlib import Path
from typing import List, Optional
from .base_types import MDCollection, MDPage, MDImage, MDItem
from .scanner import scan_directory
from .tools import name_fix

class MDCollections:
    """Manages multiple markdown collections."""
    def __init__(self, root_path: Path):
        """
        Initialize collections manager.
        
        Args:
            root_path: Root directory containing collections
        """
        self.root_path = root_path
        self.collections: List[MDCollection] = []
        self._scan_collections()

    def _scan_collections(self):
        """Scan root directory for collections."""
        if not self.root_path.exists():
            raise ValueError(f"Root path does not exist: {self.root_path}")
        
        # Scan immediate subdirectories only
        for path in sorted(self.root_path.iterdir()):
            if path.is_dir():
                # Skip directories starting with _ or containing 'archive' in lowercase
                if path.name.startswith('_') or 'archive' in path.name.lower():
                    continue

                items = scan_directory(path)
                if items:  # Only create collection if directory contains markdown files
                    collection = MDCollection(
                        path=path,
                        name=path.name,
                        items=sorted(items, key=lambda x: x.name)
                    )
                    self.collections.append(collection)
        
        # Sort collections by name
        self.collections.sort(key=lambda x: x.name)

    def collection_get(self, name: str) -> MDCollection:
        """
        Get a collection by name.
        
        Args:
            name: Name of the collection to find
            
        Returns:
            MDCollection object
            
        Raises:
            ValueError: If collection not found
        """
        for collection in self.collections:
            if collection.name == name:
                return collection
        raise ValueError(f"Collection not found: {name}")

    def page_get(self, collection_name: str, page_name: str) -> MDPage:
        """
        Get a page from a specific collection.
        
        Args:
            collection_name: Name of the collection
            page_name: Name of the page
            
        Returns:
            MDPage object
            
        Raises:
            ValueError: If collection or page not found
        """
        page_name=name_fix(page_name)
        collection_name=name_fix(collection_name)
        
        collection = self.collection_get(collection_name)
        return collection.page_get(page_name)

    def image_get(self, collection_name: str, image_name: str) -> MDImage:
        """
        Get an image from a specific collection.
        
        Args:
            collection_name: Name of the collection
            image_name: Name of the image
            
        Returns:
            MDImage object
            
        Raises:
            ValueError: If collection or image not found
        """
        # Handle image name that might contain collection prefix
        if "__" in image_name:
            image_name, collection_name = image_name.split("__", 1)
        
        image_name = name_fix(image_name)
        collection_name = name_fix(collection_name)
        
        collection = self.collection_get(collection_name)
        print(f"  -- image get: '{collection_name}' '{image_name}'")
        return collection.image_get(image_name)

    def __str__(self) -> str:
        """Returns a string representation of all collections."""
        if not self.collections:
            return "No collections found"
        
        return "\n\n".join(str(collection) for collection in self.collections)
