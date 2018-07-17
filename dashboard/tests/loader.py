from django.utils import timezone
from django.contrib.auth.models import User

from dashboard.models import *

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def load_model_objects():
    user = User.objects.create_user(username='Karyn',
                                        password='specialP@55word')
    ds = DataSource.objects.create(title='Data Source for Test',
                                        estimated_records=2, state='AT',
                                        priority='HI')
    script = Script.objects.create(title='Test Download Script',
                                        url='http://www.epa.gov/',
                                        qa_begun=False, script_type='DL')
    exscript = Script.objects.create(title='Test Extraction Script',
                                   url='http://www.epa.gov/',
                                   qa_begun=False, script_type='EX')
    gt = GroupType.objects.create(title='Composition')
    dg = DataGroup.objects.create(name='Data Group for Test',
                                        description='Testing...',
                                        data_source = ds,
                                        download_script=script,
                                        downloaded_by=user,
                                        downloaded_at=timezone.now(),
                                        group_type=gt,
                                        csv='register_records_matching.csv')
    dt = DocumentType.objects.create(title='msds/sds', group_type=gt)
    doc = DataDocument.objects.create(title='test document',
                                            data_group=dg,
                                            document_type=dt)
    p = Product.objects.create(data_source=ds,
                                upc='Test UPC for ProductToPUC')

    puc = PUC.objects.create(gen_cat='Test General Category',
                              prod_fam='Test Product Family',
                              prod_type='Test Product Type',
                             description='Test Product Description',
                             last_edited_by = user)

    extext = ExtractedText.objects.create(
                                    prod_name='Test Extracted Text Record',
                                    data_document=doc,
                                    extraction_script=exscript
                                    )
    ut = UnitType.objects.create(title='percent composition')
    wft = WeightFractionType.objects.create(title= 'reported', description= 'reported')
    ec = ExtractedChemical.objects.create(raw_chem_name= 'Test Chem Name',
                                            extracted_text=extext,
                                            unit_type=ut,
                                            weight_fraction_type = wft)
    dsstox = DSSToxSubstance.objects.create(extracted_chemical=ec,
                                            true_chemname='Test Chem Name')
    pa = ProductAttribute.objects.create(title="Test Product Attribute")
    pd = ProductDocument.objects.create(product=p, document=doc)
    ing = Ingredient.objects.create(weight_fraction_type = wft,
                                     lower_wf_analysis = 0.123456789012345,
                                     central_wf_analysis = 0.2,
                                     upper_wf_analysis = 1)
    pi = ProductToIngredient.objects.create(product=p, ingredient=ing)
    dsi = DSSToxSubstanceToIngredient.objects.create(dsstox_substance=dsstox,
                                                        ingredient=ing)
    ehp = ExtractedHabitsAndPractices.objects.create(extracted_text=extext,
                                                     product_surveyed='Test Product Surveyed',
                                                     prevalence='Continuous')


    return dotdict({'user':user,
                    'ds':ds,
                    'script':script,
                    'exscript':exscript,
                    'dg':dg,
                    'doc':doc,
                    'p':p,
                    'puc':puc,
                    'extext':extext,
                    'ut':ut,
                    'wft':wft,
                    'ec':ec,
                    'dsstox':dsstox,
                    'pa':pa,
                    'pd':pd,
                    'ing':ing,
                    'pi':pi,
                    'dsi':dsi,
                    'dt':dt,
                    'gt':gt,
                    'ehp':ehp
                    })