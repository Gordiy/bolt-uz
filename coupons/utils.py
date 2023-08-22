"""Utils for coupons app."""
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile


def is_integer(s: str) -> bool:
    """Check if string is integer."""
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s: str) -> bool:
    """Check if string is float."""
    try:
        float(s)
        return True
    except ValueError:
        return False


def convert_to_temporary_uploaded_file(inmemory_uploaded_file: InMemoryUploadedFile) -> TemporaryUploadedFile:
    """
    Convert InMemoryUploadedFile to TemporaryUploadedFile.
    
    :param inmemory_uploaded_file: InMemoryUploadedFile.
    :return TemporaryUploadedFile:
    """
    temp_uploaded_file = TemporaryUploadedFile(
        inmemory_uploaded_file.name, inmemory_uploaded_file.content_type, inmemory_uploaded_file.size,
        inmemory_uploaded_file.charset, inmemory_uploaded_file.content_type_extra
    )
    temp_uploaded_file.file = inmemory_uploaded_file.file
    
    return temp_uploaded_file
