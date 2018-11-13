import csv
import datetime
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count, F, DateField, DateTimeField
from django.db.models.functions import Trunc

from dashboard.models import *

current_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
chart_start_datetime = datetime.datetime(datetime.datetime.now().year - 1,
                                            datetime.datetime.now().month + 1,
                                            1)

def index(request):

    doc_count = DataDocument.objects.count()
    extracted = DataDocument.objects.filter(extracted = True).count()
    prod_with_puc = ProductToPUC.objects.filter(classification_method='MA')
    stats = {
            'datagroup_count': DataGroup.objects.count(),
            'datasource_count': DataSource.objects.count(),
            'datadocument_count': doc_count,
            'datadocument_with_extracted_text_percent': extracted/doc_count*100,
            'datadocument_count_by_date': datadocument_count_by_date(),
            'datadocument_count_by_month': model_count_by_month(),
            'product_count': Product.objects.count(),
            'dss_tox_count': DSSToxSubstance.objects.count(),
            'chemical_count': ExtractedChemical.objects.count(),
            #TODO: This may need to be updated later to handle both manual and
            # automatically assigned PUCs
            'product_with_puc_count': prod_with_puc.count(),
            'product_with_puc_count_by_month': model_count_by_month(
                                                                model='product')
            }
    return render(request, 'dashboard/index.html', stats)


def datadocument_count_by_date():
    # Datasets to populate linechart with document-upload statistics
    # Number of datadocuments, that have been uploaded as of each date
    doc_count_date = DataDocument.objects.values('created_at')\
                                            .annotate(Count('id'))\
                                            .order_by('created_at')
    count = 0
    for x in doc_count_date:
        count += x['id__count']
        x['id__count']= count
    return doc_count_date

def model_count_by_month(model='document'):
    # GROUP BY issue solved with https://stackoverflow.com/questions/8746014/django-group-by-date-day-month-year
    if model == 'document':
        qs = DataDocument.objects.filter(created_at__gte=chart_start_datetime)
    if model == 'product':
        qs = ProductToPUC.objects.filter(classification_method__exact='MA')\
                                .filter(created_at__gte=chart_start_datetime)
    model_stats = list(qs.annotate(month_made = (Trunc('created_at', 'month')))\
                            .values('month_made') \
                            .annotate(Count('id')) \
                            .values('id__count', 'month_made') \
                            .order_by('month_made'))
    if len(model_stats) < 12:
        for i in range(0, 12):
            chart_month = chart_start_datetime + relativedelta(months=i)
            include_current = i + 1 > len(model_stats)
            if include_current or model_stats[i]['month_made'] != chart_month:
                model_stats.insert(i, { 'id__count' : '0',
                                        'month_made': chart_month})
    return model_stats

def download_PUCs(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PUCs.csv"'

    writer = csv.writer(response)
    cols = ['gen_cat','prod_fam','prod_type',
            'description','PUC_type','num_prods']
    writer.writerow(cols)
    for puc in PUC.objects.all():
        row = [puc.gen_cat, puc.prod_fam, puc.prod_type, puc.description,
                            puc.get_level(), puc.producttopuc_set.count()]
        writer.writerow(row)

    return response
