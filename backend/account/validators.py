import os

def validate_files_extension(name):
    isValid = True

    ext = os.path.splitext(name)[-1]
    validate_extensions = ['.pdf']

    if not ext.lower() in validate_extensions:
        isValid = False

    return isValid