"""Utils for coupons app."""
from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            TemporaryUploadedFile)

from .constants import IMAGE_EXTENTSIONS
from django.core.files.temp import NamedTemporaryFile


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
    
def deepcopy_temporary_uploaded_file(original_uploaded_file: TemporaryUploadedFile) -> TemporaryUploadedFile:
        """Make a copy of temporary uploaded file."""
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(original_uploaded_file.read())
        temp_file.close()

        copied_uploaded_file = TemporaryUploadedFile(
            name=original_uploaded_file.name,
            content_type=original_uploaded_file.content_type,
            size=original_uploaded_file.size,
            charset=original_uploaded_file.charset,
            content_type_extra=original_uploaded_file.content_type_extra,
        )
        
        copied_uploaded_file.file = temp_file

        return copied_uploaded_file

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

def has_image_extension(file_name: str) -> bool:
    """
    Check if file name has image extension.
    
    :param file_name: file name.
    :retun: True if image.
    """
    return any(file_name.lower().endswith(ext) for ext in IMAGE_EXTENTSIONS)
