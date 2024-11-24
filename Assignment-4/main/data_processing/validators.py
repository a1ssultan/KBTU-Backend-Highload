from django.core.exceptions import ValidationError
import mimetypes
import pyclamd


def validate_csv(file):
    file_extension = file.name.split('.')[-1].lower()
    if file_extension != 'csv':
        raise ValidationError("Only CSV files are allowed.")

    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type != 'text/csv':
        raise ValidationError("The file must be a CSV file.")


def scan_file(file):
    cd = pyclamd.ClamdUnixSocket()

    try:
        cd.ping()
    except pyclamd.ClamdError:
        raise ValidationError("ClamAV is not running. Please configure it first.")

    file_path = file.path
    result = cd.scan_file(file_path)

    if result is not None:
        raise ValidationError("Malware detected! The file cannot be uploaded.")