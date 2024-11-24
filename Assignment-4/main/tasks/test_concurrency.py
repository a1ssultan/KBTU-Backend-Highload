import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from threading import Thread


class ConcurrentFileUploadTests(TestCase):

    def simulate_file_upload(self):
        file_content = "Year,Industry_aggregation_NZSIOC,Industry_code_NZSIOC\n2023,Level 3,CC32"
        uploaded_file = SimpleUploadedFile("test.csv", file_content.encode(), content_type="text/csv")

        self.client.post(reverse('upload_csv'), {'csv_file': uploaded_file})

    def test_concurrent_file_uploads(self):
        threads = []
        for _ in range(5):
            thread = Thread(target=self.simulate_file_upload)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Check that the number of files processed is 5 (for each thread)
        self.assertEqual(len(os.listdir(settings.MEDIA_ROOT)), 5)
