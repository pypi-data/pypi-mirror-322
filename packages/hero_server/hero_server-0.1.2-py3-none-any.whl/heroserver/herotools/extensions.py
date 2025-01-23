import mimetypes
import os

def check_and_add_extension(file_path: str) -> str:
    # Only check if there's no extension
    if not os.path.splitext(file_path)[1]:
        # Read the file content
        with open(file_path, 'rb') as f:
            content = f.read(2048)  # Read the first 2048 bytes for detection

        # Detect content type
        content_type = detect_content_type(content)
        extension = mimetypes.guess_extension(content_type)

        if extension:
            new_file_path = file_path + extension
            os.rename(file_path, new_file_path)
            return new_file_path
    
    return file_path

def detect_content_type(content: bytes) -> str:
    # Simple content-based detection
    if content.startswith(b'\xff\xd8'):
        return 'image/jpeg'
    if content.startswith(b'\x89PNG'):
        return 'image/png'
    if content.startswith(b'GIF'):
        return 'image/gif'
    # Add more checks as needed
    return 'application/octet-stream'