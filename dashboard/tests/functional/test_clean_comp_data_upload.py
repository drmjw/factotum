import tempfile, csv, os, io

from django.urls import resolve
from django.http import HttpRequest
from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from dashboard import views
from dashboard.models import *


class UploadExtractedFileTest(TestCase):
    fixtures = ['00_superuser.yaml', '01_lookups.yaml',
                '02_datasource.yaml', '03_datagroup.yaml', '04_PUC.yaml',
                '05_product.yaml', '06_datadocument.yaml', '07_script.yaml',
                '08_extractedtext.yaml', '09_productdocument.yaml', 
                '10_extractedchemical', '11_dsstoxsubstance']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.c.login(username='Karyn', password='specialP@55word')

    def generate_valid_clean_comp_data_csv_string(self):
        csv_string = (
            "id,lower_wf_analysis,central_wf_analysis,upper_wf_analysis"
            "\n"
            "5,0.7777,.99999999,1.0"
            "\n"
            "8,.44,.23,.88")
        return csv_string

    def generate_invalid_clean_comp_data_csv_string(self):
        csv_string = (
            "id,lower_wf_analysis,central_wf_analysis,upper_wf_analysis"
            "\n"
            "5,1.7777,.99999999,1.0"
            "\n"
            "8,.44,.23,.88"
            "\n"
            "999,.44,.23,.88")
        return csv_string

    def generate_invalid_headers_clean_comp_data_csv_string(self):
        csv_string = (
            "id,bad_header1,bad_header2"
            "\n"
            "5,1.7777,.99999999"
            "\n"
            "8,.44,.23")
        return csv_string

    def test_valid_clean_comp_data_upload(self):
        sample_csv = self.generate_valid_clean_comp_data_csv_string()
        sample_csv_bytes = sample_csv.encode(encoding='UTF-8',errors='strict' )
        in_mem_sample_csv = InMemoryUploadedFile(
                io.BytesIO(sample_csv_bytes),
                field_name='clean_comp_data_file',
                name='clean_comp_data.csv',
                content_type='text/csv',
                size=len(sample_csv),
                charset='utf-8',
        )
        req_data = {'script_selection': 17,
                    'clean_comp_data_button': 'Submit',
                    }
        req = self.factory.post(path = '/datagroup/6/' , data=req_data)
        req.FILES['clean_comp_data_file'] = in_mem_sample_csv
        req.user = User.objects.get(username='Karyn')
        resp = views.data_group_detail(request=req, pk=6)
        self.assertContains(resp,'2 clean composition data records uploaded successfully.')

        self.assertEqual(Ingredient.objects.count(),2,"There should be only 2 Ingredient objects")

    def test_invalid_headers_clean_comp_data_upload(self):
        sample_csv = self.generate_invalid_headers_clean_comp_data_csv_string()
        sample_csv_bytes = sample_csv.encode(encoding='UTF-8',errors='strict' )
        in_mem_sample_csv = InMemoryUploadedFile(
                io.BytesIO(sample_csv_bytes),
                field_name='clean_comp_data_file',
                name='clean_comp_data.csv',
                content_type='text/csv',
                size=len(sample_csv),
                charset='utf-8',
        )
        req_data = {'script_selection': 17,
                    'clean_comp_data_button': 'Submit',
                    }
        req = self.factory.post(path = '/datagroup/6/' , data=req_data)
        req.FILES['clean_comp_data_file'] = in_mem_sample_csv
        req.user = User.objects.get(username='Karyn')
        resp = views.data_group_detail(request=req, pk=6)
        self.assertContains(resp,'The following columns need to be added or renamed in the csv')

    def test_invalid_clean_comp_data_upload(self):
        sample_csv = self.generate_invalid_clean_comp_data_csv_string()
        sample_csv_bytes = sample_csv.encode(encoding='UTF-8',errors='strict' )
        in_mem_sample_csv = InMemoryUploadedFile(
                io.BytesIO(sample_csv_bytes),
                field_name='clean_comp_data_file',
                name='clean_comp_data.csv',
                content_type='text/csv',
                size=len(sample_csv),
                charset='utf-8',
        )
        req_data = {'script_selection': 17,
                    'clean_comp_data_button': 'Submit',
                    }
        req = self.factory.post(path = '/datagroup/6/' , data=req_data)
        req.FILES['clean_comp_data_file'] = in_mem_sample_csv
        req.user = User.objects.get(username='Karyn')
        resp = views.data_group_detail(request=req, pk=6)
        self.assertContains(resp,'No ExtractedChemical matches id 999')

