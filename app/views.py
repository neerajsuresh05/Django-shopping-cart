from django.shortcuts import render, redirect
from app.models import products,usertable,cart
from django.http import HttpResponse
from django.contrib.auth import authenticate,logout

def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=usertable.objects.get(email=email)
        if user.password==password:
            request.session['member_id']=user.id
            return render(request, 'user.html', {
        'items': products.objects.all(),
        'user':user
    })
        else:
            return HttpResponse("login failed")
    return render(request,'userlogin.html')

def user_register(request):
    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        place=request.POST.get('place')
        mobile=request.POST.get('mobile')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if usertable.objects.filter(email=email).exists():
            return HttpResponse('User already exists!!')
        usertable.objects.create(
            firstname=firstname,
            lastname=lastname,
            place=place,
            mobile=mobile,
            email=email,
            password=password
        )
        return redirect('user_login')
    return render(request,'userregister.html')

def admin_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            return render(request, 'admin_panel.html', {
        'items': products.objects.all()
    })
        else:
            return HttpResponse("login failed")
    return render(request,'login.html')

def add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock=request.POST.get('stock')
        img = request.POST.get('img')
        if name and price and stock and img:
            products.objects.create(
                name=name,
                price=price,
                stock=stock,
                img=img
            )

        return redirect('add')

    return render(request, 'add.html', {
        'items': products.objects.all(),
    })  

def view(request):
    return render(request, 'view.html', {
        'items': products.objects.all()
    })

def delete(request,id):
    data=products.objects.get(id=id)
    data.delete()
    return redirect('view')

def update(request,id):
    data=products.objects.get(id=id)
    if request.method=='POST':
        data.name=request.POST['nname']
        data.price=request.POST['nprice']
        data.stock=request.POST['nstock']
        data.img=request.POST['nimg']
        data.save()
        return redirect('view')
    return render(request,'update.html',{'prod':data})

def admin_panel(request):
    return render(request,'admin_panel.html')

def logoutt(request):
    logout(request)
    return redirect('home')

def addcart(request):
    if request.method == "POST":
        usern = request.POST.get('user')
        itemn = request.POST.get('item')
        price = float(request.POST.get('price'))
        item_id = int(request.POST.get('id'))
        qty = int(request.POST.get('qty'))
        img = request.POST.get('img')  # assuming storing path
        userid = request.session.get('member_id')

        print(usern, itemn, price, item_id, qty)

        if usern and itemn and price and item_id and qty and userid:

            # ✅ Check if item already exists
            existing = cart.objects.filter(userid=userid, item_id=item_id).first()

            if existing:
                existing.qty += qty
                existing.save()
            else:
                cart.objects.create(
                    usern=usern,
                    price=price,
                    itemn=itemn,
                    item_id=item_id,
                    qty=qty,
                    userid=userid,
                    img=img
                )

        return redirect('userview')

    return render(request, 'user.html', {
        'items': products.objects.all(),
    })

def userview(request):
    userid = request.session.get('member_id')
    user = usertable.objects.get(id=userid)

    return render(request, 'user.html', {
        'items': products.objects.all(),
        'user': user
    })

def viewcart(request):
    userid = request.session.get('member_id')
    items = cart.objects.filter(userid=userid)
    total = 0
    for i in items:
        i.subtotal = i.price * i.qty 
        total += i.subtotal

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })

def remove_item(request, id):
    item = cart.objects.get(id=id)
    item.delete()
    return redirect('viewcart')

def place_order(request):
    cart = request.session.get('cart', {})

    items = []
    total = 0

    for key, value in cart.items():
        subtotal = value['price'] * value['qty']
        total += subtotal

        items.append({
            'itemn': value['name'],
            'qty': value['qty'],
            'subtotal': subtotal
        })

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        payment = request.POST.get('payment')

        # clear cart
        request.session['cart'] = {}

        return render(request, 'bill.html', {
            'name': name,
            'address': address,
            'payment': payment,
            'items': items,
            'total': total
        })

    return render(request, 'order.html')