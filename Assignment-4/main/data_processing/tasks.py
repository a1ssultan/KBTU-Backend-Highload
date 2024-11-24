import csv
from .models import IndustryData
from celery import shared_task


@shared_task
def process_csv_file(file_url):
    try:
        with open(file_url, 'r') as f:
            csv_reader = csv.DictReader(f)

            for row in csv_reader:
                try:
                    year = row['Year']
                    industry_name = row['Industry_name_NZSIOC']
                    value = row['Value']
                    industry_code = row['Industry_code_NZSIOC']
                    industry_aggregation = row['Industry_aggregation_NZSIOC']
                    variable_code = row['Variable_code']
                    variable_name = row['Variable_name']
                    variable_category = row['Variable_category']
                    industry_code_anzsic06 = row['Industry_code_ANZSIC06']
                    units = row['Units']

                    if not is_valid_number(value):
                        print(f"Invalid data in row (non-numeric value in 'Value'): {row}")
                        continue

                    value = float(value)

                    IndustryData.objects.create(
                        year=year,
                        industry_name_nzsioc=industry_name,
                        value=value,
                        industry_code_nzsioc=industry_code,
                        industry_aggregation_nzsioc=industry_aggregation,
                        variable_code=variable_code,
                        variable_name=variable_name,
                        variable_category=variable_category,
                        industry_code_anzsic06=industry_code_anzsic06,
                        units=units
                    )

                except KeyError as e:
                    print(f"Missing required field in row: {row} - Error: {e}")
                    continue

        return "CSV processed successfully"

    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return f"Error processing CSV file: {e}"


def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
