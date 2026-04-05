from django.core.exceptions import ValidationError
from .constant import ALLOWED_FILE_TYPES
import os
def validate_file_type(file):
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ALLOWED_FILE_TYPES:
        raise ValidationError(
            "Only PDF, DOCX, PPT, ZIP files are allowed."
        )

def validate_file_size(file):
    max_size =  10 * 1020 * 1024 #10MB
    if file.size > max_size:
        raise ValidationError(
            "File size must not exceed 10MB."
        )