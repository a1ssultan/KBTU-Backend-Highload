from django.db import models


class IndustryData(models.Model):
    year = models.IntegerField()
    industry_aggregation_nzsioc = models.CharField(max_length=255)
    industry_code_nzsioc = models.CharField(max_length=50)
    industry_name_nzsioc = models.CharField(max_length=255)
    units = models.CharField(max_length=50)
    variable_code = models.CharField(max_length=50)
    variable_name = models.CharField(max_length=255)
    variable_category = models.CharField(max_length=255)
    value = models.FloatField()
    industry_code_anzsic06 = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['year']),
            models.Index(fields=['industry_code_nzsioc']),
            models.Index(fields=['variable_code']),
            models.Index(fields=['value']),
        ]

    def __str__(self):
        return f"{self.year} - {self.industry_name_nzsioc}"
