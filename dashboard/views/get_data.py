
from django.shortcuts import render
from django.http import HttpResponse
import datetime
import csv
from dashboard.models import DSSToxSubstance, DataDocument, PUC, Product, ExtractedChemical, ExtractedText
from django.db.models import Count, Q, Value, IntegerField, Subquery, OuterRef
from django.forms.models import model_to_dict
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from django.contrib import messages





def get_data(request, template_name='get_data/get_data.html'):

    return render(request, template_name)



def stats_by_dtxsids(dtxs):
    """     
    PUCS.n
    The number of unique PUCs (product categories) the chemical is associated with

    datadocs.n
    "The number of data documents (e.g.  MSDS, SDS, ingredient list, product label) 
    the chemical is appears in"

    datadocs_w_wf.n
    "The number of data documents with associated weight fraction data 
    that the chemical appears in (weight fraction data may be reported or predicted data,
     i.e., predicted from an ingredient list)"

    products.n
    "The number of products the chemical appears in, where a product is defined as a 
    product entry in Factotum." 
    """
    print('List of DTXSIDs provided:')
    print(dtxs)

    # pucs_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
    #     annotate(pucs_n=Count('ingredient__product__puc')).values('sid','pucs_n')
    # pucs_n = list(pucs_n)
    pucs_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(pucs_n=Count('ingredient__product__puc')).values('sid','pucs_n')
    print('pucs_n:')
    print(pucs_n)

    dds_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(dds_n=Count('ingredient__product__datadocument')).values('sid','dds_n')
    print('dds_n:')
    print(dds_n)

    dds_wf_n = DSSToxSubstance.objects\
    .filter(sid__in=dtxs).values('sid')\
    .annotate(
        dds_wf_n = Subquery(
            ExtractedChemical
            .objects
            .filter(pk=OuterRef('extracted_chemical_id') )
            .filter(
                Q(raw_max_comp__isnull=False) | 
                Q(raw_min_comp__isnull=False) | 
                Q(raw_central_comp__isnull=False)
            )
            .values('extracted_text_id')
            .distinct()
            .annotate(dds_wf_n=Count('extracted_text_id') )
            .values('dds_wf_n')
        )
    )
    print('dds_wf_n:')
    print(dds_wf_n)

    products_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(products_n=Count('ingredient__product')).values('sid', 'products_n')
    print('products_n:')
    print(products_n)

    stats = pucs_n\
    .annotate(dds_n=Value(-1, output_field=IntegerField())) \
    .annotate(dds_wf_n=Value(-1, output_field=IntegerField())) \
    .annotate(products_n=Value(-1, output_field=IntegerField()))

    for row in stats:
        row['dds_n'] = int(dds_n.get(sid=row['sid'])['dds_n'] or 0)
        row['dds_wf_n'] = int(dds_wf_n.get(sid=row['sid'])['dds_wf_n'] or 0)
        row['products_n'] = int(products_n.get(sid=row['sid'])['products_n'] or 0)

    return stats

def download_chem_stats(stats):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chem_summary_metrics_%s.csv"' % (datetime.datetime.now().strftime("%Y%m%d"))
 
    writer = csv.writer(response)
    writer.writerow(['DTXSID',  'pucs_n', 'dds_n', 'dds_wf_n', 'products_n'])
    for stat in stats:
        writer.writerow([stat['sid'], stat['pucs_n'], stat['dds_n'], stat['dds_wf_n'], stat['products_n']])

    return response

def upload_dtxsid_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "get_data/get_data.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_dtxsid_csv"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("upload_dtxsid_csv"))

        file_data = csv_file.read().decode("utf-8")        

        lines = file_data.split("\n")
        #loop over the lines 
        dtxsids = []
        for line in lines:
            print(line)
            if DSSToxSubstance.objects.filter(sid=str.strip(line)).count() > 0:
                dtxsids.append(str.strip(line)) # only add DTXSIDs that appear in the database

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    stats = stats_by_dtxsids(dtxsids)
    resp = download_chem_stats(stats)
    print(resp)
    return resp