from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.conf import settings
import os


class FileUploadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_file_upload_success(self):
        self.client.login(username='testuser', password='password')

        file_content = "Year,Industry_aggregation_NZSIOC,Industry_code_NZSIOC\n2023,Level 3,CC32"
        uploaded_file = SimpleUploadedFile("test.csv", file_content.encode(), content_type="text/csv")

        response = self.client.post(reverse('upload_csv'), {'csv_file': uploaded_file})

        self.assertEqual(response.status_code, 302)  # Redirect after successful upload
        self.assertContains(response, "CSV file uploaded successfully!")  # Check success message

        # Check that the file was saved in the storage backend (optional)
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'test.csv')
        self.assertTrue(os.path.exists(file_path))

    def test_invalid_file_type(self):
        self.client.login(username='testuser', password='password')

        uploaded_file = SimpleUploadedFile("test.txt", b"Some random text.", content_type="text/plain")

        response = self.client.post(reverse('upload_csv'), {'csv_file': uploaded_file})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid file type. Only CSV files are allowed.")
