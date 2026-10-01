from django.shortcuts import render , redirect 
from django.views import View
from .models import OrderPlaced , cart , customer, Product
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

#def home(request):
# return render(request, 'app/home.html')
class ProductView(View):
 def get(self,request):
  topwear = Product.objects.filter(category='TW')
  bottomwear = Product.objects.filter(category='BT')
  Mobiles = Product.objects.filter(category = 'M')
  return render(request, 'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,'Mobiles':Mobiles})




 
#def product_detail(request):
# return render(request, 'app/productdetail.html')
class ProductDetailView(View):
 def get(self, request, pk ):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/productdetail.html' , {'product':product})




def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 cart(user=user, product = product).save()
 return redirect('showcart')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        carts = cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0 
        cart_product = [p for p in cart.objects.all() if p.user == user]
    if cart_product:
       for p in cart_product:
          tempamount = (p.quantity * p.product.selling_price)
          amount += tempamount
          total_amount = amount + shipping_amount
    #else:
    #   return render(request , 'app/emptycart.html')      


    return render(request, 'app/addtocart.html', {'carts': carts,'total_amount': total_amount, 'amount':amount })

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        c = cart.objects.get(
            product_id=prod_id,
            user=user
        )

        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0

        cart_product = cart.objects.filter(user=user)

        for p in cart_product:
            amount += p.quantity * p.product.selling_price

        total_amount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount
        }

        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        c = cart.objects.get(
            product_id=prod_id,
            user=user
        )

        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0

        cart_product = cart.objects.filter(user=user)

        for p in cart_product:
            amount += p.quantity * p.product.selling_price

        total_amount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount
        }

        return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        c = cart.objects.get(
            product_id=prod_id,
            user=user
        )

        
        c.delete()

        amount = 0.0
        shipping_amount = 70.0

        cart_product = cart.objects.filter(user=user)

        for p in cart_product:
            amount += p.quantity * p.product.selling_price

        total_amount = amount + shipping_amount

        data = {
            'amount': amount,
            'totalamount': total_amount
        }

        return JsonResponse(data)




    
def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
 add = customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active': 'btn-primary' })

def orders(request):
 return render(request, 'app/orders.html')


def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')

    elif data == 'iphone' or data == 'samsung':
        mobile = Product.objects.filter(
            category='M',
            brand=data
        )

    return render(
        request,
        'app/mobile.html',
        {'mobile': mobile}
    )
def login(request):
 return render(request, 'app/login.html')

#def customerregistration(request):
# return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):

    def get(self, request):
        form = CustomerRegistrationForm()
        return render(
            request,
            'app/customerregistration.html',
            {'form': form}
        )

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()

        return render(
            request,
            'app/customerregistration.html',
            {'form': form}
        )

def checkout(request):
    user = request.user
    add = customer.objects.filter(user=user)
    cart_items = cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.selling_price
            amount += tempamount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {
        'add': add,
        'totalamount': totalamount,
        'cart_items': cart_items,
    })



class ProfileView(View):

    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request,
            'app/profile.html',
            {'form': form, 'active': 'btn-primary'}
        )

    def post(self, request):
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            usr = request.user

            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']

            reg = customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zip_code=zip_code
            )

            reg.save()

            messages.success(
                request,
                'Congratulations !! Profile Update Successfully'
            )

        return render(
            request,
            'app/profile.html',
            {'form': form, 'active': 'btn-primary'}
        )



    