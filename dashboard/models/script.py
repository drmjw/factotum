from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db import models
from dashboard.models import DataDocument
from dashboard.models import ExtractedText


class Script(models.Model):

	TYPE_CHOICES = (('DL', 'download'),
					('EX', 'extraction'),
					('PC', 'product categorization'))

	title = models.CharField(max_length=50)
	url = models.CharField(max_length  = 100,
							null       = True,
							blank      = True,
							validators = [URLValidator()])
	qa_begun = models.BooleanField(default=False)
	script_type = models.CharField( max_length = 2,
									choices    = TYPE_CHOICES,
									blank      = False,
									default    = 'EX')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('extraction_script_edit', kwargs={'pk': self.pk})

	def get_datadocument_count(self):
		return DataDocument.objects.filter(
				extractedtext__extraction_script=self.pk).count()

	def get_qa_complete_extractedtext_count(self):
		return DataDocument.objects.filter(extractedtext__qa_checked=True, extractedtext__extraction_script=self.pk).count()

	def get_pct_checked(self):
		pct = (0 if self.get_datadocument_count() == 0
				else (self.get_qa_complete_extractedtext_count() /
						self.get_datadocument_count()) * 100)
		return "{0:.0f}%".format(pct) 

	def qa_button_text(self):
		return "Begin QA" if not self.qa_begun else "Continue QA"