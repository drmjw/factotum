from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from dashboard.models import (DSSToxSubstance)

@login_required()
def dsstox_substance_detail(request, pk,
                      template_name='chemicals/dsstox_substance_detail.html'):
    s = get_object_or_404(DSSToxSubstance, pk=pk, )
    return render(request, template_name, {'substance': s,  })
