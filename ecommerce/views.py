from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Product,Category,Cart,Order, OrderItem
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request,'index.html')

def cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {"items": items})

def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')

def detail(request):
    return render(request,'detail.html')

def shop(request):
    pro=Product.objects.all()
    return render(request,'shop.html',{'pros':pro})

def login(request):
        if request.method == 'POST':
            un=request.POST['uname']
            p1=request.POST['pass1']
            user=auth.authenticate(username=un,password=p1)

            if user is not None:
                auth.login(request,user)
                print('login successfully!!')
                return redirect('/')
            else:
                print('invalid username or password!!')
                redirect('/login/')

    


        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    print('Logout successfully!')
    return redirect('/')

def register(request):
    if request.method == 'POST':
        fn=request.POST['fname']
        ln=request.POST['lname']
        em=request.POST['email']
        un=request.POST['uname']
        p1=request.POST['pass1']
        p2=request.POST['pass2']
        if p1 != p2:
            print("Password doesn't Match!")
            return redirect('/register/')
        if User.objects.filter(username=un).exists():
            print('Username already exists! Try another Username')
            return redirect('/register/')
        if User.objects.filter(email=em).exists():
            print('Email already exists! Try Again')
            return redirect('/register/')
        User.objects.create_user(
                first_name=fn,
                last_name=ln,
                email=em,
                username=un,
                password=p1
        )
        print('UserID created Successfully')
        return redirect('/login/')

    # THIS LINE MUST BE OUTSIDE THE POST BLOCK
    return render(request,'register.html')
    
#product list
def product_list(request):
    products=Product.objects.all()
    return render(request,'product_list.html',{"products":products})

#add product
def add_product(request):
    
    categories=Category.objects.all()

    if request.method=='POST':
        pname = request.POST.get('pname')
        pdis= request.POST.get('pdis')
        pprice=request.POST.get('pprice')
        cat_id=request.POST.get('cat_id')
        pimage=request.POST.get('pimage')

        cat=Category.objects.all(cid=cat_id)

        Product.objects.all(
            pname=pname,
            pdis=pdis,
            pprice=pprice,
            pimage=pimage,
            cat=cat
        )
        messages.success(request,'Products added successfully')
        return redirect('products_list')
    
    return render(request,'add_products.html',{'categories':categories})

def edit_product(request,pid):
    product=get_object_or_404(Product,pid=pid)
    categories=Category.objects.all()

    if request.method=='POST':
        product.pname=request.POST.get('pname')
        product.pdis=request.POST.get('pdis')
        product.pprice=request.POST.get('pprice')
        product.cat_id=request.POST.get('cat')

        if request.FILES.get('pimage'):
            product.pimage=request.FILES.get('pimage')

        product.save()
        messages.success(request,"products updated successfully")
        return redirect('product_list')
    
    return render(request,'edit_product.html',{'products':product, 'categories':categories})

#delete 

def delete_product(request,pid):
    product=get_object_or_404(Product, pid=pid)
    product.delete()
    messages.success(request,'product deleted successfully')
    return redirect('product_list')

def add_to_cart(request, pid):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first.")
        return redirect('/login/')

    product = get_object_or_404(Product, pid=pid)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.pname} added to cart")
    return redirect('cart_page')



def cart_page(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    cart_items = Cart.objects.filter(user=request.user)

    subtotal = sum(item.product.pprice * item.quantity for item in cart_items)
    shipping = 50 if subtotal > 0 else 0
    total = subtotal + shipping

    for item in cart_items:
        item.total = item.product.pprice * item.quantity
        item.qty = item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })

def decrease_qty(request, pid):
    item = Cart.objects.get(user=request.user, product__pid=pid)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart_page')


def increase_qty(request, pid):
    item = Cart.objects.get(user=request.user, product__pid=pid)
    item.quantity += 1
    item.save()
    return redirect('cart_page')


def remove_item(request, pid):
    item = Cart.objects.get(user=request.user, product__pid=pid)
    item.delete()
    return redirect('cart_page')



def checkout_page(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect('cart_page')

    subtotal = sum(item.product.pprice * item.quantity for item in cart_items)
    shipping = 50 if subtotal > 0 else 0
    total = subtotal + shipping

    # Add extra attributes for template
    for item in cart_items:
        item.total = item.product.pprice * item.quantity
        item.qty = item.quantity

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })




def place_order(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country', 'United States')
        payment_method = request.POST.get('payment')

        cart_items = Cart.objects.filter(user=user)
        if not cart_items:
            messages.error(request, "Your cart is empty!")
            return redirect('cart_page')

        total_amount = sum(item.product.pprice * item.quantity for item in cart_items) + 50  # shipping

        # Create order
        order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            payment_method=payment_method,
            total_amount=total_amount
        )

        # Save order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.pprice
            )

        # Clear user's cart
        cart_items.delete()

        messages.success(request, f"Thank you {first_name}! Your order has been placed successfully.")
        return redirect('shop')

    else:
        return redirect('checkout_page')

