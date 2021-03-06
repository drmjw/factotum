from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from dashboard.models import ProductToPUC, ProductToTag, PUCToTag

#When dissociating a product from a PUC, delete it's (PUC-dependent) tags
@receiver(post_delete, sender=ProductToPUC)
def delete_product_puc_tags(sender, **kwargs):
    instance = kwargs['instance']
    ProductToTag.objects.filter(content_object=instance.product).delete()

#When dissociating a puc from a tag, also disocciate any puc-related products from that tag
@receiver(post_delete, sender=PUCToTag)
def delete_related_product_tags(sender, **kwargs):
    instance = kwargs['instance']
    products = instance.content_object.products.all()
    products_to_tags = ProductToTag.objects.filter(tag=instance.tag).filter(content_object__in=products)
    products_to_tags.delete()
