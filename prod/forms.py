from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES=(
('S','Stripe'),
('P','Paymark')
)

DELIVERY_CHOICES=(
    ('Auckland','Delivery - Auckland'),
    ('Whangarei to Hamilton','Delivery - Whangarei to Hamilton'),
    ('Rest of north island','Delivery - Rest of north island'),
    ('Kaikoura to Timaru','Delivery - Kaikoura to Timaru'),
    ('Christchurch','Delivery - Christchurch'),
    ('Rest of south island','Delivery - Rest of south island')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False,widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    shipping_zip=forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(required=False,widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    billing_zip=forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option=forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)
    shiploc = forms.ChoiceField(choices=DELIVERY_CHOICES)

#widget=forms.CheckboxInput()

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Promo code',
        'aria-label':'Recipient\'s username',
        'aria-describedby':'basic-addon2'
    }))

class RefundForm(forms.Form):
    ref_code=forms.CharField()
    message=forms.CharField(widget=forms.Textarea(attrs={
        'rows':4
    }))
    email=forms.EmailField()

class NewsletForm(forms.Form):
    email = forms.EmailField()

    # class Meta:
    #     fields = ['email']
