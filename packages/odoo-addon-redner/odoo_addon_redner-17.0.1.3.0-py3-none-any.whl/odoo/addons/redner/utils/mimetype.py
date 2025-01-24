import base64
import mimetypes

import magic


def b64_to_extension(b64_string):
    try:
        # Decode the Base64 string into binary data
        binary_data = base64.b64decode(b64_string)
        # Use python-magic to determine the MIME type
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(binary_data)
        # Get the file extension from the MIME type
        return mimetypes.guess_extension(mime_type)
    except Exception as e:
        print(f"Error detecting file type: {e}")
        return None


def get_file_extension(binary_data):
    """Determine the file extension from binary content."""
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(binary_data)

    # Mapping MIME types to extensions
    mime_to_ext = {
        "application/vnd.oasis.opendocument.text": ".odt",
        "application/pdf": ".pdf",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/msword": ".doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",  # noqa: E501
    }
    return mime_to_ext.get(
        file_type, ".odt"
    )  # Default to empty string if MIME type not found
