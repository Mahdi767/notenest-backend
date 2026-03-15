RESOURCE_TYPE_CHOICES = (
    ('lecture_note', 'Lecture Note'),
    ('assignment', 'Assignment'),
    ('lab_report', 'Lab Report'),
    ('question_bank', 'Question Bank'),
    ('book', 'Book'),
)

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

ALLOWED_FILE_TYPES = [
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".zip",
]