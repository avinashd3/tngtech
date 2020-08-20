"""tngtech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from prod.sitemaps import TngprodSitemap
from prod import views as ob
from django.conf import settings
from django.conf.urls.static import static
from users import views as useroo
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

admin.site.site_header = 'My administration'

sitemaps = {
    "prods": TngprodSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ob.HomeView.as_view(),name='homie'),
    path('register/',useroo.register,name='userreg'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('product/<slug>/',ob.ProductsDetailView.as_view(),name='itemlist'),
    path('order-summary/',ob.OrderSummaryView.as_view(),name='order-summary'),
    path('checkout/',ob.CheckoutView.as_view(),name='checku'),
    path('payment/<payment_option>/',ob.PaymentView.as_view(),name='payment'),
    path('add-to-cart/<slug>/',ob.add_to_cart,name='addtocart'),
    path('add-to-cart-lout/',ob.add_to_cart_lout,name='addtocartlout'),
    path('add-coupon/',ob.AddCouponView.as_view(),name='addcoupon'),
    path('remove-from-cart/<slug>/',ob.remove_from_cart,name='removefromcart'),
    path('remove-item-from-cart/<slug>/',ob.remove_single_item_from_cart,name='removeitemfromcart'),
    path('request-refund/',ob.RequestRefundView.as_view(),name='request-refund'),
    path('profile/',ob.profile,name='profile'),
    path('view-orders/',ob.vieworder,name='vieworders'),
    path('password-change/',ob.UpdatePassword,name='passwordchange'),
    path('view-address/',ob.viewaddress,name='viewaddresses'),
    path('search/',ob.search,name='searchprod'),
    path('serv-prod/<slug>/',ob.catgdisp,name='servprod'),
    path('changeadd/<slug>/',ob.chanadd,name='changeadd'),
    path('about/',TemplateView.as_view(template_name='prod/about-us.html'),name='about'),
    path('t&c/',TemplateView.as_view(template_name='prod/tandc.html'),name='tandc'),
    path('privacy-policy/',TemplateView.as_view(template_name='prod/privacy.html'),name='privacy'),
    path('wdyc/',TemplateView.as_view(template_name='prod/whydoyoucare.html'),name='wdyc'),
    path('contact/',ob.contacto,name='contact'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('oauth/',include('social_django.urls',namespace='social')),
    path('paymento/',ob.pymto,name='paymento'),
    path('payto/',ob.payto,name='payto'),
    path('newsl/',ob.newsl,name='newsl'),
    path('homenews/',ob.homenews,name='homenews'),
    path('remadd/<slug>/',ob.remadd,name='remadd'),
    path('sitemap.xml',sitemap,{'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap'),
    path('online-booking/<slug>/',ob.onlinebooking,name='onlinebooking'),
    path('store/<slug>/',ob.shopp,name='store'),
    path('prod-sc/<slug>/',ob.prbysc,name='prbysc'),
    path('prod-br/<slug>/',ob.prbybr,name='prbybr'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
