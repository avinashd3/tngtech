from django import template
from prod.models import Order,TngProducts

register=template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs=Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            return qs[0].tngproduct.count()
    return 0

@register.inclusion_tag('base.html')
def prods_all():
    pr_qs = TngProducts.objects.all()
    # return pr_qs
    return {'prdall':pr_qs}

# register.assignment_tag(prods_all, name='proll')