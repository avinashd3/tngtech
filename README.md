# tngtech
This is an ecommerce website.

Start date of this project : 8-June-2020
End date of this project : This project is open to updates and hence not yet closed

Special thanks to:
  seniors(shubhamdhama sir): without his help and motivation this project would not be possible.

Keynotes of this project:
<!-- 1. The current template design is provided by Colorlib. (This will be updated and changed in upcoming updates) -->
1. The payment gateway that this project uses is Paymark.(No card details are stored .This will be provided in upcoming updates)
<!-- 3. Since the current payment gateway performs its services only in NewZealand, only users from NZ can buy products from this site.However this payment gateway be changed according to one's needs. -->
2. Technologies used are : Django , Python , HTML 5 , CSS 3 , JavaScript , Bootstrap 4 .
3. Deployment vps : Digital Ocean(Ubuntu 18)
4. Deployment OS : Linux
5. Deployment server : Apache

Features of this project:
1. Admin part:
  The admin can change/add following functions
    * The admin can add new products & services(images,description,price,discount-price,category:{new,bestseller})
    * The admin can alter user's details (except user's password)
    * The admin can view the user's order details
    * The admin can see and grant refund requests from user.
    * The admin can add new coupon codes.
    * The admin can view/change user's shipping and billing addresses.
    * The admin can view subscribed newsletter emails.
  
2. Site's functionality:
    * All products and services can be browsed in home-page of website.These products and services are placed category wised .
    * User can quickview and add products/services to his/her cart.
    * User can view his/her cart and alter the quantity of products and also remove the products from cart.
    * User can proceed to checkout and after entering details he/she can proceed to paymark gateway to buy the items.
    * A unique transaction id will be provided by paymark and a unique order id is provided by our website, which the user can view from accessing his profile.
    * A user can visit his profile and can access following features:
        > Can view orders placed by user.
        > Can change password.
        > Can Request Refund.
        > Can view/alter billing and shipping address.
    * If a user forgets his password , he can choose forget password option and an email containing link to change password will be sent to the user's mail.
    * A user can subscribe to newsletter.
    * A user can search products and services in this website.

Keynotes for backend:
1. The cart features(adding/removing item to cart , viewing items in cart) are handled by javascript when user is logged out and cart details are stored in localStorage functionality of javascript.
    However when user is logged in , these cart items and all functionality described above are carried out by functions written in python and handled by django.

This project is currently deployed at http://139.59.90.204:8080/
