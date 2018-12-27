from django.db import models

from .common_info import CommonInfo

class RawChem(CommonInfo):

    raw_cas = models.CharField("Raw CAS", max_length=100, null=True, blank=True)
    raw_chem_name = models.CharField("Raw chemical name", max_length=500,
                                                        null=True, blank=True)
    dss_tox = models.OneToOneField(to='DSSToxSubstance',
                                                    on_delete=models.CASCADE,
                                                    null=True, blank=True)