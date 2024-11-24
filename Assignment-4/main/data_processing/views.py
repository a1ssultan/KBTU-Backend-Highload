from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render

from .tasks import process_csv_file
from django.contrib import messages


def upload_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]
        file_name = csv_file.name

        # Check if the file has already been processed and cached
        cached_result = cache.get(file_name)
        if cached_result:
            # Return cached result if present
            messages.success(request, "Using cached result for the CSV file.")
            return render(request, "upload_csv.html", {'result': cached_result})

        # Otherwise, process the file

        # Process the file and cache the result
        result = process_csv_file.apply_async(args=[file_name])
        cache.set(file_name, result, timeout=3600)  # Cache result for 1 hour

        messages.success(request, f"CSV file uploaded and processed!")

        return render(request, "upload_csv.html", {'result': result})

    return render(request, "upload_csv.html")

