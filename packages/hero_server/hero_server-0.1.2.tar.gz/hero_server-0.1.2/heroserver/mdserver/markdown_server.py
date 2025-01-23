from typing import Optional, Union
import os
from pathlib import Path
import traceback
import sys
import re
import pudb
try:
    import streamlit as st
except ImportError:
    raise ImportError("streamlit is required. Install with: pip install streamlit")

from mdcollections.base_types import MDPage, MDImage, MDCollection
from mdcollections.mdcollections import MDCollections
from .process_markdown import process_markdown, summary_load
from .tools import debug

def setup_static_dir(collections_path: str) -> None:
    """
    Set up static directory for serving images.
    Creates symbolic links from collections to static directory.
    """
    pass
    # static_dir = os.path.join(collections_path, "static")
    # if not os.path.exists(static_dir):
    #     os.makedirs(static_dir)
        
    # Create symlinks for each collection
    # collections = os.listdir(collections_path)
    # for collection in collections:
    #     collection_path = os.path.join(collections_path, collection)
    #     if os.path.isdir(collection_path) and not collection.startswith('.') and collection != 'static':
    #         # Create symlink from collection to static/collection
    #         static_link = os.path.join(static_dir, collection)
    #         if not os.path.exists(static_link):
    #             try:
    #                 os.symlink(collection_path, static_link)
    #             except OSError as e:
    #                 debug(f"Failed to create symlink from {collection_path} to {static_link}: {e}")

def process_markdown_content(content: str, base_path: str, collection_name: str) -> None:
    """
    Process and display markdown content.
    
    Args:
        content: The markdown content to process
        base_path: Base path for resolving relative paths
        collection_name: Name of the collection
    """
    st.markdown(content)

class MDServer:
    def __init__(self,collections_path:str):
        """Initialize the MDServer instance."""
        # Convert path to string if it's a Path object
        if not isinstance(collections_path, str):
            return RuntimeError("collections_path must be a string.")
        
        st.session_state.setdefault('current_collection', None)
        st.session_state.setdefault('current_page', None)
        st.session_state.setdefault('show_collections_view', False)
        st.session_state.setdefault('collections_manager', None)
        st.session_state.setdefault('debug_mode', True)        

        # Get the collections manager
        collections_path = os.path.expanduser(collections_path)

        print(f"Initializing collections manager for: {collections_path}")
            
        collections_manager = MDCollections(root_path=Path(collections_path))

        # Set up static directory for serving images
        setup_static_dir(collections_path)

        # Set up page config
        st.set_page_config(
            page_title="Markdown Server",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        st.session_state.collections_manager = collections_manager 

    @property
    def collections_manager(self) -> MDCollections:
        """
        Property to safely access the collections manager.
        Ensures collections_manager is initialized before access.
        
        Returns:
            MDCollections: The initialized collections manager
            
        Raises:
            RuntimeError: If collections_manager is not initialized
        """
        if not st.session_state.get('collections_manager'):
            raise RuntimeError("Collections manager not initialized. Please ensure MDServer is properly initialized.")
        return st.session_state.collections_manager

    @property
    def collections(self) -> list:
        """
        Property to safely access collections from the collections manager.
        
        Returns:
            list: List of available collections
            
        Raises:
            RuntimeError: If collections_manager is not initialized
        """
        return self.collections_manager.collections

    def handle_url_parameters(self) -> None:
        """
        Handle URL parameters to load specific pages.
        Expected format: ?page=collection_name__page_name.md
        Example: ?page=banking_whitepaper__web_3_vision.md
        """
        query_params = st.query_params
        requested_page = query_params.get('page', None)
        
        if not requested_page:
            return
            
        try:
            # Split the page parameter using '__' as delimiter
            if '__' not in requested_page:
                raise ValueError(f"Invalid page format. Expected format: collection_name__page_name.md, got: {requested_page}")
                
            collection_name, page_name = requested_page.split('__', 1)
            
            # Get the page using collections_manager's page_get method
            page = self.collections_manager.page_get(
                collection_name=collection_name,
                page_name=page_name
            )
                        
            page = process_markdown(page, collections=self.collections_manager)    
            
            st.session_state.current_collection = page.collection
            st.session_state.current_page = page
            
        except ValueError as e:
            # Handle invalid format or page not found errors
            st.warning(f"Could not load page: {requested_page}. Error: {str(e)}")

    def setup_sidebar(self, collections: MDCollections) -> None:
        """
        Set up the sidebar with collection selection.
        
        Args:
            collections: List of available collections
        """
        with st.sidebar:
            # Add Debug Mode toggle that persists across reloads
            debug_mode = st.toggle("Debug Mode", st.session_state.debug_mode)
            if debug_mode != st.session_state.debug_mode:
                st.session_state.debug_mode = debug_mode
                # Store in local storage to persist across reloads
                st.session_state['debug_mode'] = debug_mode
            
            # Add Collections View action
            if st.button("View All Collections"):
                st.session_state.show_collections_view = True
                st.session_state.current_page = None
                return

            collection_names = [c.name for c in self.collections]
            current_idx = collection_names.index(st.session_state.current_collection.name) if st.session_state.current_collection else 0
            
            selected_collection_name = st.selectbox(
                "Choose a collection:",
                collection_names,
                index=current_idx,
                key="collection_selector"
            )
            
            # Add sidebar content
            with st.sidebar:
                # Check for summary.md
                collection = self.collections_manager.collection_get(selected_collection_name)
                summary_page = summary_load(collection)
                st.markdown(summary_page.content, unsafe_allow_html=True)
                        
            # Get the selected collection by name
            st.session_state.current_collection = self.collections_manager.collection_get(selected_collection_name)
            
    def display_content(self) -> None:
        """Display the markdown content in the main area."""
        main_content = st.container()
        
        with main_content:
            try:
                if st.session_state.show_collections_view:
                    # Read and process collections view template
                    collections_view_path = Path(__file__).parent / "pages" / "collections_view.md"
                    with open(collections_view_path, 'r') as f:
                        template = f.read()
                    
                    # Replace placeholder with actual collections string representation
                    content = template.replace("{collections_str}", str(self.collections_manager))
                    st.markdown(content)

                elif st.session_state.current_page:                                         
                    st.markdown(st.session_state.current_page.content, unsafe_allow_html=True)
                    
                elif st.session_state.current_collection:
                    # Display collection summary and index when no specific page is selected
                    st.markdown("### Collection Index")
                    myindex_page = st.session_state.current_collection.index_page()
                    myindex_page = process_markdown(myindex_page, collections=self.collections_manager)     
                    st.markdown(myindex_page.content)
                else:
                    st.warning("Please select a collection.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    def serve_markdown(self) -> None:
        """
        Serve markdown content using Streamlit.
        """
        try:
            if not self.collections:
                st.error("No collections found.")
                return

            # Handle URL parameters
            self.handle_url_parameters()
            
            # Setup sidebar
            self.setup_sidebar(self.collections_manager)
            
            # Display content
            self.display_content()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
