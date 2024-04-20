from django.http import JsonResponse
from django.shortcuts import redirect,render
from app.models import slider
from app.models import banner_area,Main_Category,Product,Category,Color,Brand,Cupon
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Sum
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def BASE(request):
    
    return render(request, 'base.html')

def HOME(request):
    
    sliders = slider.objects.all().order_by('-id')[0:3]           #for updating latest sliders and banners
    banners = banner_area.objects.all().order_by('-id')[0:6]
    main_category = Main_Category.objects.all()
    product = Product.objects.filter(section__name = 'Top Deal of The Day')
    
    
    contexts = {
        
        'sliders': sliders,
        'banners': banners,
        'main_category': main_category,
        'product': product,
    }
    return render(request, 'Main/home.html',contexts)

def PRODUCT_DETAILS(request,slug):
    product = Product.objects.filter(slug = slug)
    if product.exists():
       product = Product.objects.get(slug = slug)
    else:
       return redirect('404')
    contexts = {
        
        'product': product,
    }
    return render(request,'product/product_detail.html',contexts)


def Error404(request):
    return render (request,'errors/404.html')

def MY_ACCOUNT(request):
    return  render (request,'account/myaccount.html')

from django.contrib.auth.models import User
from django.shortcuts import redirect

def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
             messages.error(request, 'User already exists!!')
             return redirect('login')
         
        if User.objects.filter(email=email).exists():
             messages.error(request, 'Email ID already exists!!')
             return redirect('login')
        
        
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        return redirect('login')

def LOGIN(request):
 if request.method == 'POST':
       
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            
        else:
            messages.error(request, 'Invalid username or password!!')
            pass
            return redirect('login')
@login_required(login_url='/account/login/')
def PROFILE(request):
    
    return render(request, 'profile/profile.html')
@login_required(login_url='/account/login/')
def PROFILE_UPDATE(request):
       
       if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, "Profile Updated Successfully!!")
        return redirect('profile')
       
def ABOUT(request):
    
    return render(request, 'Main/about.html')

def CONTACT(request):
    
    return render(request, 'Main/contact.html')
    
def PRODUCT(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    ColorID = request.GET.get('colorID')
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    elif ColorID: 
        product = Product.objects.filter(color = ColorID)
    
    else:
        product = Product.objects.all()
    
    
    contexts = {
        
        'category': category,
        'product': product,
        'min_price':min_price,
        'max_price':max_price,
        'FilterPrice':FilterPrice,
        'color':color,
        'brand':brand,
		
    }
    
    return render(request, 'product/product.html', contexts)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    product_num = request.GET.getlist('product_num[]')
    brand = request.GET.getlistt('brand[]')



    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
     allProducts = allProducts.filter(Categories__id__in-categories).distinct()
    
    if len(product_num) > 0:
     allproducts = allProducts.all().order_by('-id')[0:1]
     
    if len(brands) > 0:
     allProducts = allProducts.filter(Brand__id__in=brands).distinct()
    t = render_to_string('ajax/product.html', {'product': allProducts})
    return JsonResponse({'data': t})





@login_required(login_url="/account/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i.get('packing_cost', 0) for i in cart.values() if i)
    tax = sum(i.get('packing_cost', 0) for i in cart.values() if i)

    cupon = None
    valid_cupon = None
    invalid_cupon = None

    if request.method == 'GET':
        cupon_code = request.GET.get('cupon_code')
        if cupon_code:
            try:
                cupon = Cupon.objects.get(code=cupon_code)
                valid_cupon = "Applicable on current orders!"
            except Cupon.DoesNotExist:
                invalid_cupon = "Invalid Coupon Code!!"

    context = {  
        'packing_cost': packing_cost,
        'tax': tax,
        'cupon': cupon, 
        'valid_cupon': valid_cupon,
        'invalid_cupon': invalid_cupon,
    }

    return render(request, 'cart/cart.html', context)

                                     
def CHECKOUT(request):
    coupon_discount = None
    context = {}  # Define context variable

    if request.method == "POST":
        coupon_discount = request.POST.get('coupon_discount')
        cart = request.session.get('cart')
        packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
        tax = sum(i['tax'] for i in cart.values() if i)
        tax_and_packing_cost = packing_cost + tax
        context.update({
            'tax_and_packing_cost': tax_and_packing_cost, 
            'coupon_discount': coupon_discount,
        })

    return render(request, 'checkout/checkout.html', context)


    
    
