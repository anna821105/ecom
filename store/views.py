from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.forms import SignUpForm,UpdateUserForm,changePasswordForm,UserInForm

from payment.forms import ShippingForm
from payment.models import  ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart



def search(request):
    # Determin if they filled out the form 判斷用戶是否已經填寫了表單
    if request.method == "POST":
        searched = request.POST.get('searched','')
        # Query The Products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))#大寫小都可以
        # Test for null
        if not searched:
            messages.success(request,"The Product Does Not Exisit ,Please Try Aagin !!!!")
            return render(request,'search.html',{})
        else:
            return render(request,'search.html',{'searched': searched })
    else:
        return render(request,'search.html',{})


#update_info函數的作用是處理用戶更新其個人資料或"其他信息"的邏輯
def update_info(request):#分兩部分(1)除了Django外基本資料(2)配送地址
    if request.user.is_authenticated:
        # Get Current User(1)
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current User's Shipping Info(2)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get Original User Form(1)
        form = UserInForm(request.POST or None ,instance=current_user)
        # Get User's Shipping Form(2)
        shipping_form = ShippingForm(request.POST or None ,instance=shipping_user)
        
        if form.is_valid() or shipping_form.is_valid(): #------兩部分
            # Save original form
            form.save()
            # Save shipping form
            shipping_form.save()
            
            messages.success(request,"User  Info Has Been Update !!!!")
            return redirect('home')
        return render(request,'update_info.html',{'form': form ,'shipping_form':shipping_form})       
    else:
        messages.success(request,"You Must Be Logged In To Access That  Page !!!!")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form 
        if request.method == 'POST':
            form = changePasswordForm(current_user,request.POST)
            #Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request,"Your Password Has Been Update !!!!")
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password')
                
        else:
            form = changePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,"You Must Be Logged In To View That  Page !!!!")
        return redirect('home')   


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None ,instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request,current_user)
            messages.success(request,"User Has Been Update !!!!")
            return redirect('home')
        return render(request,'update_user.html',{'user_form': user_form })       
    else:
        messages.success(request,"You Must Be Logged In To Access That  Page !!!!")
        return redirect('home')
    


def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html',{'categories': categories})

def category(request,foo):
    # replace Hyphens with spaces 將連字號替換為空格
    foo = foo.replace('-',' ')
    # Grab the category from url找對應的分類
    try:
        #這裡使用 Category 模型根據 foo 查找對應的分類，
        # 然後使用 Product 模型查找所有屬於該分類的產品。
        # 如果分類存在，則將 category 和 products 作為上下文傳遞給模板渲染。
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        # 正常返回分類頁面
        return render (request,'category.html',{'products':products,'category':category}) 
    
    
    except:
        messages.success(request,("The Category Doesn't Exist  !!"))
        return redirect('home')




def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            
            # 登入後，保留上次紀錄 Do some shopping cart stuff
            current_user = Profile.objects.get(user__id = request.user.id)
            # Get their saved cart from datebase
            saved_cart = current_user.old_cart
            # covert datebase string to python dictionary
            if saved_cart:
                #convert to dictionary using json
                converted_cart =json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # loop  through  the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)
                                        
            messages.success(request,("You Have Been Logged In !!"))
            return redirect('home')
        else:
            messages.success(request,("There was an error,please try again !!"))
            return redirect('login.html')      
        
    else:
        return render(request,'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out !!"))
    return redirect('home')

    
    
    
def register_user(request):
    form = SignUpForm()
    if request.method =="POST":
        form = SignUpForm(request.POST)
        if form.is_valid(): 
            #檢查表單是否有效，即確保所有欄位都正確填寫
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username,password=password) # 使用輸入的用戶名和密碼來驗證用戶
            login(request,user)  
            messages.success(request,("You Have Register Successfully!! Welcome ~~  Username  Created-Please Fill Out Your User Info Below......."))
            return redirect('update_info')
        else:
            messages.success(request,(" Whoops! There was a problem Registering,please try agin. "))
            return redirect('register')
    else:
        return render(request,'register.html',{'form':form})
    

