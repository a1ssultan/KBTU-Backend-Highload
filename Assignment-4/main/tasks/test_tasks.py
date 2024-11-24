from django.test import TestCase
from main.data_processing.tasks import process_csv_file
from unittest.mock import patch
from io import StringIO


class CeleryTaskTests(TestCase):

    @patch('data_processing.tasks.open', return_value=StringIO("Year,Industry_aggregation_NZSIOC,Industry_code_NZSIOC\n2023,Level 3,CC32"))
    def test_process_csv_file(self, mock_open):
        result = process_csv_file("test.csv")

        self.assertEqual(result, "Processing completed.")

        mock_open.assert_called_with('test.csv', 'r')
