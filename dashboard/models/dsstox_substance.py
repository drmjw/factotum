from django.db import models
from .common_info import CommonInfo
from .extracted_chemical import ExtractedChemical
from django.urls import reverse
from .raw_chem import RawChem


class DSSToxSubstance(CommonInfo):

    true_cas = models.CharField(max_length=50, null=True, blank=True)
    true_chemname = models.CharField(max_length=500, null=True, blank=True)
    rid = models.CharField(max_length=50, null=True, blank=True)
    sid = models.CharField(max_length=50, null=True, blank=True)

    rawchem_ptr = models.OneToOneField(related_name='curated_chemical', 
        on_delete=models.CASCADE, to='dashboard.RawChem')

    def __str__(self):
        return self.true_chemname

    def get_datadocument_url(self):
        return (self.extracted_chemical.extracted_text
                        .data_document.get_absolute_url())

    def indexing(self):
        obj = DSSToxSubstanceIndex(
            meta={'id': self.id},
            chem_name=self.true_chemname,
            true_cas=self.true_cas,
            true_chem_name=self.true_chemname,
            facet_model_name='DSSTox Substance',
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def get_absolute_url(self):
        return reverse('dsstox_substance', kwargs={'pk': self.pk})

    def indexing(self):
        obj = DSSToxSubstanceIndex(
            meta={'id': self.id},
            title=self.true_chemname,
            facet_model_name='DSSTox Substance',
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    @property
    def extracted_chemical(self):
        return self.rawchem_ptr.extracted_chemical
    
    @property
    def raw_cas(self):
        return self.rawchem_ptr.raw_cas

    @property
    def raw_chem_name(self):
        return self.rawchem_ptr.raw_chem_name
    
    def get_extractedtext(self):
        return self.extracted_chemical.get_extractedtext


