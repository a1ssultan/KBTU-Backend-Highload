from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render

from .tasks import process_csv_file
from django.contrib import messages


def upload_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]

        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_url = fs.url(filename)

        # Get the absolute file path
        file_path = fs.path(filename)

        process_csv_file.apply_async(args=[file_path])

        messages.success(request, f"CSV file uploaded successfully!")

        return redirect("upload_csv")

    return render(request, "upload_csv.html")
