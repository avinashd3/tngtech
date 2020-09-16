from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView,DetailView,View
from .models import TngProducts,OrderItem,Order,Address,Payment,Coupon,Refund,NewsLetter,OnlineBooking
from changes.models import Shophome,HotDeals,Category,SubCategory,Brand,TopSelling
from django.utils import timezone
from django.urls import reverse
from .forms import CheckoutForm,CouponForm,RefundForm,NewsletForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import send_mail,send_mass_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from datetime import datetime
from itertools import chain

import random
import requests
import xml.etree.ElementTree as ET
import string
import stripe
import json
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def add_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

# or query in i.Additional_Details.lower()  Error=NoneType cannot have lower bcoz Additional details of some prods are None(Empty)
def searchmatch(query, i):
    if query.lower() in i.Name.lower() or query.lower() in i.Details.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    prodt=TngProducts.objects.all()
    produ = []
    for i in prodt:
        if searchmatch(query,i):
            produ.append(i)
    context={
        'produ': produ
    }
    return render(request,'prod/search-prod.html',context)

def homenews(request):
    newsmail = request.POST.get('email')
    alr_qs = NewsLetter.objects.filter(email = newsmail)
    if alr_qs.exists():
        messages.warning(request, f'You have already been subscribed!')
        return redirect('/')
    else:
        send_mail(
            'Our monthly newsletter',
            'Thank you, for subscribing to our newsletter. Stay tuned for more blog updates and budget saving tips',
            settings.EMAIL_HOST_USER,
            [newsmail],
            fail_silently = False,
        )
        nl = NewsLetter.objects.create(email = newsmail)
        nl.save()
        messages.success(request, f'You have been subscribed!')
        return redirect('/')
    return redirect('homie')

def newsl(request):
    form = NewsletForm(request.POST)

    if request.method == 'POST':
        form = NewsletForm(request.POST)
        if form.is_valid():
            newsmail = form.cleaned_data.get("email")
            alr_qs = NewsLetter.objects.filter(email = newsmail)
            if alr_qs.exists():
                messages.warning(request, f'You have already been subscribed!')
                return redirect('/')
            else:
                send_mail(
                    'Our monthly newsletter',
                    'Thank you, for subscribing to our newsletter. Stay tuned for more blog updates and budget saving tips',
                    settings.EMAIL_HOST_USER,
                    [newsmail],
                    fail_silently = False,
                )
                nl = NewsLetter.objects.create(email = newsmail)
                nl.save()
                messages.success(request, f'You have been subscribed!')
                return redirect('/')
    return render(request,'prod/newsi.html',{'form':form})


class HomeView(ListView):
    model=TngProducts
    # paginate_by=8
    template_name='prod/home-page.html'
    fields=['email']

    def post(self, *args, **kwargs):
        form = NewsletForm(self.request.POST or NONE)
        if form.is_valid():
            newsmail = form.cleaned_data.get("email")
            alr_qs = NewsLetter.objects.filter(email = newsmail)
            if alr_qs.exists():
                messages.warning(self.request, f'You have already been subscribed!')
                return redirect('/')
            else:
                send_mail(
                    'Our monthly newsletter',
                    'Thank you, for subscribing to our newsletter. Stay tuned for more blog updates and budget saving tips',
                    settings.EMAIL_HOST_USER,
                    [newsmail],
                    fail_silently = False,
                )
                nl = NewsLetter.objects.create(email = newsmail)
                nl.save()
                messages.success(self.request, f'You have been subscribed!')
                return redirect('/')
        else:
            form = NewsletForm()
        return render(self.request,self.template_name,{'form':form})
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        shop_qs = Shophome.objects.all()[:3]
        context['shopc'] = shop_qs
        hdtime_qs = HotDeals.objects.all()[:1]
        context['hd'] = hdtime_qs
        newarr1 = TngProducts.objects.filter(label = 'D')[:3]
        context['newarr1'] = newarr1
        newarr2 = TngProducts.objects.filter(label = 'D')[3:6]
        context['newarr2'] = newarr2
        bestsell1 = TngProducts.objects.filter(label = 'P')[:3]
        context['bestsell1'] = bestsell1
        bestsell2 = TngProducts.objects.filter(label = 'P')[3:6]
        context['bestsell2'] = bestsell2
        hotdeal1 = TngProducts.objects.filter(label = 'H')[:3]
        context['hotdeal1'] = hotdeal1
        hotdeal2 = TngProducts.objects.filter(label = 'H')[3:6]
        context['hotdeal2'] = hotdeal2
        topsel = TopSelling.objects.all()[:4]
        context['ts1'] = topsel[0]
        context['ts2'] = topsel[1]
        context['ts3'] = topsel[2]
        context['ts4'] = topsel[3]
        if self.request.user.is_authenticated:
            if Order.objects.filter(user=self.request.user,ordered=False).exists():
                car_qs = Order.objects.get(user=self.request.user,ordered=False)
                context['ctq'] = car_qs
            return context
        else:
            return context

class ProductsDetailView(DetailView):
    model=TngProducts
    template_name='prod/product-page.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        allpr_qs = TngProducts.objects.all()
        context['allprd'] = allpr_qs
        if self.request.user.is_authenticated:
            if Order.objects.filter(user=self.request.user,ordered=False).exists():
                car_qs = Order.objects.get(user=self.request.user,ordered=False)
                # if car_qs.exists():
                context['ctq'] = car_qs
            return context
        else:
            return context

""" class BaseoDetailView(ListView):
    model=TngProducts
    template_name='prod/base.html' """

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     allpr_qs = TngProducts.objects.all()
    #     context['allprd'] = allpr_qs
    #     if self.request.user.is_authenticated:
    #         car_qs = Order.objects.get(user=self.request.user,ordered=False)
    #         context['ctq'] = car_qs
    #         return context
    #     else:
    #         return context

def catgdisp(request):
    return redirect('servprod')

#Check if our user is authenticated

class OrderSummaryView(View):
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            try:
                order=Order.objects.get(user=self.request.user,ordered=False)
                context={
                    'object':order
                }
                return render(self.request,'prod/order-summary.html',context)
            except ObjectDoesNotExist:
                messages.warning(self.request,f'You do not have an active order')
                return redirect("/")
        else :
            prs = TngProducts.objects.all()
            context = {
                'prs': prs
            }
            return render(self.request,'prod/order-summary.html',context)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            form = CheckoutForm()
            context={
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM':True
            }

            shipping_address_qs = Address.objects.filter(user=self.request.user,address_type='S',default=True)
            if shipping_address_qs.exists():
                context.update({ 'default_shipping_address': shipping_address_qs[0] })

            billing_address_qs = Address.objects.filter(user=self.request.user,address_type='B',default=True)
            if billing_address_qs.exists():
                context.update({ 'default_billing_address': billing_address_qs[0] })

            return render(self.request,'prod/checkout-page.html',context)

        except ObjectDoesNotExist:
            messages.info(self.request,f'You do not have an active order')
            return redirect('checku')

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(user=self.request.user,address_type='S',default=True)
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request,"No default shipping address available")
                        return redirect('checku')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address=Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            zip=shipping_zip,
                            country=shipping_country,
                            address_type='S',
                            addr_code = add_ref_code()
                            )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            defaddr_qs = Address.objects.filter(user=self.request.user,address_type='S',default=True)
                            if defaddr_qs.exists():
                                defaddr_qs.update(default=False)
                                #defaddr_qs[0].save()
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request,"Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the default billing address")
                    address_qs = Address.objects.filter(user=self.request.user,address_type='B',default=True)
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request,"No default billing address available")
                        return redirect('checku')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address=Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            zip=billing_zip,
                            country=billing_country,
                            address_type='B',
                            addr_code = add_ref_code()
                            )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            defadb_qs = Address.objects.filter(user=self.request.user,address_type='B',default=True)
                            if defadb_qs.exists():
                                defadb_qs.update(default=False)
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(self.request,"Please fill in the required billing address fields")

                
                delcharges = form.cleaned_data.get('shiploc')
                if delcharges == 'Auckland':
                    delamt = 6.00
                elif delcharges == 'Whangarei to Hamilton':
                    delamt = 6.37
                elif delcharges == 'Rest of north island':
                    delamt = 11.99
                elif delcharges == 'Kaikoura to Timaru':
                    delamt = 19.14
                elif delcharges == 'Christchurch':
                    delamt = 12.00
                elif delcharges == 'Rest of south island':
                    delamt = 19.14

                payment_option=form.cleaned_data.get('payment_option')
                # TODO: add redirect to selected payment option
                if payment_option=='S':
                    return redirect('payment',payment_option='stripe')
                elif payment_option=='P':
                    amt = order.get_total() + delamt
                    payment = {'account_id': 13350,'username': settings.PAY_CLIENTID,'password': settings.PAY_PASS,'cmd': '_xclick','amount': amt,'return_url': 'https://tngtechsolutions.co.nz/paymento/'}
                    r = requests.post("https://secure.paymarkclick.co.nz/api/webpayments/paymentservice/rest/WPRequest", data=payment)
                    # payment = {'account_id': 625807,'username': 104374,'password': 'ml2IKsFGUhdhYiTO2','cmd': '_xclick','amount': amt,'return_url': 'http://127.0.0.1:8000/paymento/'}
                    # r = requests.post("https://uat.paymarkclick.co.nz/api/webpayments/paymentservice/rest/WPRequest", data=payment)
                    root = ET.fromstring(r.text)
                    return redirect(root.text)
                else:
                    messages.warning(self.request,f'Wrong payment choice')
                    return redirect('checku') #does redirect loses any data? Yes it does
        except ObjectDoesNotExist:
            messages.warning(self.request,f'You do not have an active order')
            return redirect('order-summary')

@login_required
def payto(request):
    tid = request.GET.get('tid')
    st = request.GET.get('st')
    dt = request.GET.get('dt')
    amt = request.GET.get('amt')
    order=Order.objects.get(user=request.user,ordered=False)
    #fdt = dt.strftime("%Y-%m-%d %H:%M:%S")
    context = {
        'tid': tid,
        'status': st,
        'dt': dt,
        'amt': amt
    }
    if st == 'SUCCESSFUL':
        payment=Payment()
        payment.stripe_charge_id = tid
        payment.user = request.user
        payment.amount = amt
        payment.save()

        order_items=order.tngproduct.all()
        order_items.update(ordered=True)
        for i in order_items:
            i.save()

        order.ordered = True
        order.payment = payment
        order.ref_code = create_ref_code()
        order.ordered_date = timezone.now()
        order.save()
        send_mail(
            'Thanks for ordering from TNGTech',
            'Thank you for letting us serve you,here are your details',
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
            html_message = render_to_string('prod/whydoyoucare.html',{'obj': order})
        )
    else:
        context={
            'status': st
        }
    return render(request,'prod/paymento.html',context)

@csrf_exempt
def pymto(request):
    if request.method == 'POST':
        tid = request.POST.get('TransactionId')
        status = request.POST.get('Status')
        dt = request.POST.get('TransactionDate')
        amt = request.POST.get('Amount')
        base_url = reverse('payto') 
        query_string =  urlencode({'tid': tid,'st': status,'dt': dt,'amt': amt})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url) 

class PaymentView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        order=Order.objects.get(user=self.request.user,ordered=False)
        if order.billing_address:
            context={
                'order':order,
                'DISPLAY_COUPON_FORM':False
            }
            return render(self.request,'prod/payment.html',context)
        else:
            messages.warning(self.request,"You have not added a billing address")
            return redirect('checku')

    def post(self,*args,**kwargs):
        order=Order.objects.get(user=self.request.user,ordered=False)
        token = self.request.POST.get('stripeToken')
        amount=int(order.get_total() * 100)


        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="nzd",
                source=token
                )
            #creating the payment
            payment=Payment()
            payment.stripe_charge_id=charge['id']
            payment.user=self.request.user
            payment.amount=order.get_total()
            payment.save()

            #assign payment to the order

            order_items=order.tngproduct.all()
            order_items.update(ordered=True)
            for i in order_items:
                i.save()

            order.ordered = True
            order.payment=payment
            order.ref_code=create_ref_code()
            order.ordered_date=timezone.now()
            order.save()
            send_mail(
                'Thanks for ordering from TNGTech',
                'Thank you for letting us serve you,here are your details',
                settings.EMAIL_HOST_USER,
                [self.request.user.email],
                fail_silently=False,
                html_message = render_to_string('prod/whydoyoucare.html',{'obj': order})
            )
            messages.success(self.request,f"Your Order was successful !")
            return redirect("/")

        except stripe.error.CardError as e:
          # Since it's a decline, stripe.error.CardError will be caught
          messages.warning(self.request,f"{e.error.message}")
          #print('Message is: %s' % e.error.message)
          return redirect("/")

        except stripe.error.RateLimitError as e:
          # Too many requests made to the API too quickly
          messages.warning(self.request,f"Rate Limit Error")
          return redirect("/")

        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          messages.warning(self.request,f"Invalid parameters")
          return redirect("/")

        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          messages.warning(self.request,f"Not Authenticated")
          return redirect("/")

        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          messages.warning(self.request,f"Network Error")
          return redirect("/")

        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email
          messages.warning(self.request,f"Something went wrong, You were not charged. Please try again")
          return redirect("/")

        except Exception as e:
          # Something else happened, completely unrelated to Stripe
          messages.warning(self.request,f"A serious error occured. We are notified")
          return redirect("/")


def add_to_cart_lout(request):
    if request.method == 'POST':
        carti = request.POST.get('cart')
        y=json.loads(carti)
        # print(y)
        for k in y.keys():
            i=int(k)
            qnt = y[k]
            p = TngProducts.objects.get(id=i)
            if request.user.is_authenticated:
                order_item, created=OrderItem.objects.get_or_create(tngproducts=p,user=request.user,ordered=False)
                order_qs=Order.objects.filter(user=request.user,ordered=False)  #it is query set filtering for current user and checking if product is not ordered
                if order_qs.exists():
                    order=order_qs[0]
                    # check if order item is in order
                    if order.tngproduct.filter(tngproducts__slug=p.slug).exists():
                        order_item.quantity += qnt
                        order_item.save()
                        # messages.success(request, f'Product added successfully!')
                        # return HttpResponseRedirect(reverse('itemlist', kwargs={'slug':p.slug}))
                        #return redirect('order-summary')
                    else:
                        order_item.quantity=qnt
                        order_item.save()
                        order.tngproduct.add(order_item)
                        # messages.success(request, f'Product added successfully!')
                        # return HttpResponseRedirect(reverse('itemlist', kwargs={'slug':p.slug}))
                        #return redirect('order-summary')
                else:
                    ordered_date=timezone.now()
                    order=Order.objects.create(user=request.user,ordered_date=ordered_date)
                    order_item.quantity=qnt
                    order_item.save()
                    order.tngproduct.add(order_item)
                    # messages.success(request, f'Product added successfully')
                    # return HttpResponseRedirect(reverse('itemlist', kwargs={'slug':p.slug}))
        # messages.success(request, f'Got the data')
    # return redirect('/')
    return HttpResponseRedirect(reverse('homie'))


@login_required
def add_to_cart(request,slug):
    tngproducts=get_object_or_404(TngProducts,slug=slug)
    #adding items as orderitem when calling this Function

    order_item, created=OrderItem.objects.get_or_create(tngproducts=tngproducts,user=request.user,ordered=False) #written created because it is returning a tuple

    #if user has item in his cart then we change the quantity
            #Checking not checkedout order
    order_qs=Order.objects.filter(user=request.user,ordered=False)  #it is query set filtering for current user and checking if product is not ordered
    if order_qs.exists():
        order=order_qs[0]
        # check if order item is in order
        if order.tngproduct.filter(tngproducts__slug=tngproducts.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f'Product added successfully!')
            return HttpResponseRedirect(reverse('itemlist', kwargs={'slug':slug}))
            #return redirect('order-summary')
        else:
            order.tngproduct.add(order_item)
            messages.success(request, f'Product added successfully!')
            return HttpResponseRedirect(reverse('itemlist', kwargs={'slug':slug}))
            #return redirect('order-summary')
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.tngproduct.add(order_item)
        messages.success(request, f'Product added successfully')
        return HttpResponseRedirect(reverse('itemlist', kwargs={'slug':slug}))
        #return redirect('itemlist')

@login_required
def remove_from_cart(request,slug):
    tngproducts=get_object_or_404(TngProducts,slug=slug)

    #checking whether there are any unordered products in cart(i.e. order here) for the current User
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #checking whether those unordered products contain the one which the user is removing
        if order.tngproduct.filter(tngproducts__slug=tngproducts.slug).exists():
            order_item=OrderItem.objects.filter(tngproducts=tngproducts,user=request.user,ordered=False)[0]
            order.tngproduct.remove(order_item)
            order_item.delete()
            messages.success(request, f'Product removed successfully')
            return redirect('order-summary')
        else:
            #message====> order(cart) does not contain order_item(product)
            messages.warning(request, f'Your cart does not contain this product')
            return redirect('itemlist',slug=slug)
    else:
        #message====> all items in cart are ordered-----OR----- no items currently in your cart
        messages.warning(request, f'No items currently in your cart')
        return redirect('itemlist',slug=slug)

@login_required
def remove_single_item_from_cart(request,slug):
    tngproducts=get_object_or_404(TngProducts,slug=slug)

    #checking whether there are any unordered products in cart(i.e. order here) for the current User
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #checking whether those unordered products contain the one which the user is removing
        if order.tngproduct.filter(tngproducts__slug=tngproducts.slug).exists():
            order_item=OrderItem.objects.filter(tngproducts=tngproducts,user=request.user,ordered=False)[0]
            if order_item.quantity>1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.tngproduct.remove(order_item)
            messages.success(request, f'Product quantity was updated')
            return redirect('order-summary')
        else:
            #message====> order(cart) does not contain order_item(product)
            messages.warning(request, f'Your cart does not contain this product')
            return redirect('itemlist',slug=slug)
    else:
        #message====> all items in cart are ordered-----OR----- no items currently in your cart
        messages.warning(request, f'No items currently in your cart')
        return redirect('itemlist',slug=slug)

def get_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request,f'This coupon does not exist')
        return redirect('checku')

class AddCouponView(View):
    def post(self,*args,**kwargs):
        form = CouponForm(self.request.POST or NONE)
        if form.is_valid():
            try:
                code=form.cleaned_data.get('code')
                order=Order.objects.get(user=self.request.user,ordered=False) #we use request.user in functions and self.request.user in CBV
                order.coupon = get_coupon(self.request,code)
                order.save()
                messages.success(self.request,f'Successfully added coupon')
                return redirect('checku')
            except ObjectDoesNotExist:
                messages.info(self.request,f'You do not have an active order')
                return redirect('checku')

class RequestRefundView(View):
    def get(self,*args,**kwargs):
        form=RefundForm()
        context={
            'form':form
        }
        return render(self.request,'prod/request_refund.html',context)

    def post(self,*args,**kwargs):
         form=RefundForm(self.request.POST)
         if form.is_valid():
             ref_code=form.cleaned_data.get('ref_code')
             message=form.cleaned_data.get('message')
             email=form.cleaned_data.get('email')
             #editing the order
             try:
                 order=Order.objects.get(ref_code=ref_code)
                 order.refund_requested=True
                 order.save()
                 refund=Refund()
                 refund.order=order
                 refund.reason=message
                 refund.email=email
                 refund.save()
                 messages.info(self.request,"Your request was received")
                 return redirect('request-refund')
             except ObjectDoesNotExist:
                 messages.info(self.request,"This order does not exist")
                 return redirect('request-refund')

@login_required
def profile(request):
    return render(request,'prod/profile.html',{'obj': request.user})

@login_required
def vieworder(request):
    order_qs=Order.objects.filter(user=request.user,ordered=True)
    rct = order_qs.last()
    if order_qs.exists():
        context={
            'object':order_qs,
            'rct':rct
        }
    else:
        messages.warning(request,f'You do not have an order')
        context={
            'object':order_qs
        }
    return render(request,'prod/view-orders.html',context)

@login_required
def UpdatePassword(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your password has been changed successfully')
            return redirect('/')

    return render(request, 'users/password_change_form.html', {
        'form': form,
    })

@login_required
def viewaddress(request):
    addr_qs=Address.objects.filter(user=request.user)
    #addres_qs=Address.objects.filter(user=request.user,address_type='B')
    if addr_qs.exists():
        context={
            'object':addr_qs
        }
        return render(request,'prod/view-address.html',context)
    else:
        messages.warning(request,f'You do not have an address')
        # return redirect('viewaddresses')
    return render(request,'prod/view-address.html')

def catgdisp(request,slug):
    scbset = set()
    brandset = set()
    sbcatimg = SubCategory.objects.all()
    brandimg = Brand.objects.all()
    context = {
        'scbset': scbset ,
        'brandset': brandset
    }
    if slug == 'All':
        prdi = TngProducts.objects.all()
        context = {
            'prody': prdi
        }
    elif slug == 'hotdeals':
            p='H'
            prody = TngProducts.objects.filter(label=p)
            context = {
                'prody': prody
            }
    # elif slug == 'serv':
    #     mr = TngProducts.objects.filter(category='MR')
    #     lr = TngProducts.objects.filter(category='LR')
    #     tr = TngProducts.objects.filter(category='TR')
    #     prdtri = list(chain(mr,lr,tr))
    #     context = {
    #         'prody': prdtri,
    #         'kya': 'services'
    #     }
    # elif slug == 'prdcts':
    #     ma = TngProducts.objects.filter(category='MA')
    #     da = TngProducts.objects.filter(category='DA')
    #     cs = TngProducts.objects.filter(category='CS')
    #     prdtri = list(chain(ma,da,cs))
    #     context = {
    #         'prody': prdtri,
    #         'kya': 'prdcts'
    #     }
    else:
        if slug == 'MobRep':
            p='MR'
            prody = TngProducts.objects.filter(category=p)
            scbset , brandset = subcbrand(p)
            context = {
                'prody': prody,
                'scbset': scbset ,
                'brandset': brandset,
                'kya': p,
                'sbcatimg': sbcatimg,
            'brandimg': brandimg
            }
        if slug == 'LapRep':
            p='LR'
            prody = TngProducts.objects.filter(category=p)
            scbset , brandset = subcbrand(p)
            context = {
                'prody': prody,
                'scbset': scbset ,
                'brandset': brandset,
                'kya': p,
                'sbcatimg': sbcatimg,
            'brandimg': brandimg
            }
        if slug == 'TabRep':
            p='TR'
            prody = TngProducts.objects.filter(category=p)
            scbset , brandset = subcbrand(p)
            context = {
                'prody': prody,
                'scbset': scbset ,
                'brandset': brandset,
                'kya': p,
                'sbcatimg': sbcatimg,
            'brandimg': brandimg
            }
        if slug == 'MobileAccessories':
            p='MA'
            prody = TngProducts.objects.filter(category=p)
            scbset , brandset = subcbrand(p)
            context = {
            'prody': prody,
            'scbset': scbset ,
            'brandset': brandset,
            'kya': p,
            'sbcatimg': sbcatimg,
            'brandimg': brandimg
        }
        elif slug == 'LaptopAccessories':
            p='LA'
            prody = TngProducts.objects.filter(category=p)
            scbset , brandset = subcbrand(p)
            context = {
            'prody': prody,
            'scbset': scbset ,
            'brandset': brandset,
            'kya': p,
            'sbcatimg': sbcatimg,
            'brandimg': brandimg
        }
        elif slug == 'TabletAccessories':
            p='TA'
            prody = TngProducts.objects.filter(category=p)
            scbset , brandset = subcbrand(p)
            context = {
            'prody': prody,
            'scbset': scbset ,
            'brandset': brandset,
            'kya': p,
            'sbcatimg': sbcatimg,
            'brandimg': brandimg
        }
        elif slug == 'ElectronicGadgets':
            p='EG'
            prody = TngProducts.objects.filter(category=p)
            scbset , brandset = subcbrand(p)
            context = {
            'prody': prody,
            'scbset': scbset ,
            'brandset': brandset,
            'kya': p,
            'sbcatimg': sbcatimg,
            'brandimg': brandimg
        }
        elif slug == 'LatestAccessories':
            p='NA'
            scbset , brandset = subcbrand(p)
            prody = TngProducts.objects.filter(category=p)
            context = {
                'prody': prody,
                'scbset': scbset ,
                'brandset': brandset,
                'kya': p,
                'sbcatimg': sbcatimg,
            'brandimg': brandimg
            }
    return render(request,'prod/item-display.html',context)

def subcbrand(p):
    prod = TngProducts.objects.filter(category = p)
    scbset = set()
    brandset = set()
    for i in prod:
        scbset.add(i.subcategory)
        brandset.add(i.brand)
    return scbset,brandset

def contacto(request):
    if request.method == 'POST':
        name = request.POST.get('form-name')
        email = request.POST.get('form-email')
        subject = request.POST.get('form-Subject')
        message = request.POST.get('form-text')
        message1 = (subject,message+'\n Sender name: '+name+'\n Sender email: '+email, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
        message2 = ('We have noted down your request', 'We will contact to you very soon', settings.EMAIL_HOST_USER, [email])
        send_mass_mail((message1, message2), fail_silently=False)
        #mail_admins('kholo dost','Aur bhai mil gya swaad!',fail_silently=False)
        context = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }#context are required when we have to show these values in form used in template
        messages.info(request,f'We have noted down your request,will contact you soon')
    return render(request,'prod/contact-us.html')

@login_required
def chanadd(request,slug):
    if slug == 'S':
        if request.method == 'POST':
            ship_street_address = request.POST.get('street_address')
            ship_apartment_address = request.POST.get('apartment_address')
            ship_zip = request.POST.get('zip')
            set_default_address = request.POST.get('set_default_address')
            if set_default_address == 'Y':
                defadb_qs = Address.objects.filter(user=request.user,address_type='S',default=True)
                if defadb_qs.exists():
                    defadb_qs.update(default=False)
                ad_qs = Address.objects.create(user=request.user, street_address=ship_street_address, apartment_address=ship_apartment_address, address_type='S', zip=ship_zip, default=True, addr_code=add_ref_code())
                ad_qs.save()
            else:
                ad_qs = Address.objects.create(user=request.user, street_address=ship_street_address, apartment_address=ship_apartment_address, address_type='S', zip=ship_zip, default=False, addr_code=add_ref_code())
                ad_qs.save()
            messages.info(request,f'Your adddress has veen added')
            return redirect('viewaddresses')
    elif slug == 'B':
        if request.method == 'POST':
            bill_street_address = request.POST.get('street_address')
            bill_apartment_address = request.POST.get('apartment_address')
            bill_zip = request.POST.get('zip')
            set_default_address = request.POST.get('set_default_address')
            if set_default_address == 'Y':
                defadb_qs = Address.objects.filter(user=request.user,address_type='B',default=True)
                if defadb_qs.exists():
                    defadb_qs.update(default=False)
                ad_qs = Address.objects.create(user=request.user, street_address=bill_street_address, apartment_address=bill_apartment_address, address_type='B', zip=bill_zip, default=True, addr_code=add_ref_code())
                ad_qs.save()
            else:
                ad_qs = Address.objects.create(user=request.user, street_address=bill_street_address, apartment_address=bill_apartment_address, address_type='B', zip=bill_zip, default=False, addr_code=add_ref_code())
                ad_qs.save()
            messages.info(request,f'Your adddress has veen added')
            return redirect('viewaddresses')
    return render(request,'prod/change_address.html',{'sl': slug})

@login_required
def remadd(request,slug):
    addr_qs = Address.objects.filter(addr_code = slug)
    if addr_qs.exists():
        addr_qs.delete()
        messages.success(request,f'Your address has been removed')
    return redirect('viewaddresses')

def onlinebooking(request,slug):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        brand = request.POST.get('devicebrand')
        contact = request.POST.get('contact')
        device_type = request.POST.get('url_type')
        device_model = request.POST.get('type')
        repair_type = request.POST.get('repair')
        time = request.POST.get('time')
        OnlineBooking.objects.create(Name=name,email=email,brand=brand,contact=contact,
            device_model=device_model,device_type=device_type,repair_type=repair_type,time=time)
        message1 = ('New Repair booking','Brand : '+brand+'\n Contact :'+contact+'\n Device Type :'+device_type+'\n Device Model :'+device_model+'\n Repair Type :'+repair_type+'\n Time chosen : '+time+'\n Sender name: '+name+'\n Sender email: '+email, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
        message2 = ('We have noted down your request', 'We will contact to you very soon.Details for your repair service request are: \n'+
            'Brand : '+brand+'\n Contact :'+contact+'\n Device Type :'+device_type+'\n Device Model :'+device_model+'\n Repair Type :'+repair_type+'\n Time chosen : '+time, settings.EMAIL_HOST_USER, [email])
        send_mass_mail((message1, message2), fail_silently=False)
        messages.success(request,f'Your service has been booked')
        return redirect('homie')
    return render(request,'prod/online-booking.html',{'ob':slug})

def shopp(request,slug):
    thisset = set()
    if slug == 'product.php':
        thisset = {"Mobile Accessories", "Laptop Accessories", "Tablet Accessories","Electronic Gadgets","Latest Accessories"}
    elif slug == 'service.php':
        thisset = {"Mobile Repair","Laptop/Computer Repair","iPad/Tablet Repair"}
    ma_qs = Category.objects.get(name='Mobile Accessories')
    la_qs = Category.objects.get(name='Laptop Accessories')
    ta_qs = Category.objects.get(name='Tablet Accessories')
    eg_qs = Category.objects.get(name='Electronic Gadgets')
    na_qs = Category.objects.get(name='Latest Accessories')
    mr = Category.objects.get(name='Mobile Repair')
    lr = Category.objects.get(name='Laptop/Computer Repair')
    tr = Category.objects.get(name='iPad/Tablet Repair')
    return render(request,'prod/store.html',{'ts':thisset,'ma':ma_qs,'la':la_qs,'ta':ta_qs,
    'eg':eg_qs,'na':na_qs,'mr':mr,'lr':lr,'tr':tr})

def prbysc(request,slug):
    modelset = set()
    pr = slug[:2]
    subc = slug[2:]
    print(pr)
    print(subc)
    prod = TngProducts.objects.filter(category = pr,subcategory = subc)
    for i in prod:
        modelset.add(i.model)
    return render(request,'prod/prod-sc.html',{'prod':prod,'modelset':modelset,'cat':pr,'subcat':subc})

def prbybr(request,slug):
    modelset = set()
    pr = slug[:2]
    subc = slug[2:]
    prod = TngProducts.objects.filter(category = pr,brand = subc)
    for i in prod:
        modelset.add(i.model)
    return render(request,'prod/prod-br.html',{'prod':prod,'modelset':modelset,'cat':pr,'subcat':subc})

def modelprod(request,categoryslug,catandbrandslug,slug):
    kya = catandbrandslug[:2]
    bryasc = catandbrandslug[2:]
    if kya == 'sc':
        prod = TngProducts.objects.filter(category = categoryslug,subcategory = bryasc,model = slug)
    elif kya == 'br':
        prod = TngProducts.objects.filter(category = categoryslug,brand = bryasc,model = slug)
    return render(request,'prod/modelprod.html',{'prod':prod})