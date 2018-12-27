from django.db import models
from .raw_chem import RawChem
from django.core.exceptions import ValidationError
from .extracted_text import ExtractedText


class ExtractedFunctionalUse(RawChem):
    extracted_text = models.ForeignKey(ExtractedText, on_delete=models.CASCADE,
                                    related_name='uses')
    report_funcuse = models.CharField("Reported functional use",
                                        max_length=100, null=True, blank=True)

    def __str__(self):
        return self.raw_chem_name

    @classmethod
    def detail_fields(cls):
        return ['extracted_text','raw_cas','raw_chem_name','report_funcuse']

    def get_extractedtext(self):
        return self.extracted_text
