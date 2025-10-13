import base64
import mimetypes


def file_to_bytes(file_path: str) -> bytes:
    """Reads a file and returns its content as bytes."""
    with open(file_path, "rb") as f:
        return f.read()


def image_to_base64(filename: str, data: bytes):
    mime_type, _ = mimetypes.guess_type(filename)
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def image_base64_to_bytes(base64_str: str) -> bytes:
    header, encoded = base64_str.split(",", 1)
    return base64.b64decode(encoded)


def extract_mime_type(base64_str: str) -> str:
    header = base64_str.split(",", 1)[0]
    mime_type = header.split(";")[0].split(":")[1]
    return mime_type
