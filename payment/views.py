from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import  ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product,Profile
import datetime

# Import some paypal stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid  # unique user id for duplictate orders



def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order Item
        items = OrderItem.objects.filter(order=pk)
        
        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == "true":
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the order status
                now = datetime.datetime.now()
                order.update(shipped=True,date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the order status
                order.update(shipped= False)
            messages.success(request,"Shipping Status Updated")
            return redirect('home')
   
        return render(request,"payment/orders.html",{"order":order,"items":items})

    else:
        messages.success(request,"Access Denied")  #拒絕訪問" 或 "無權訪問
        return redirect('home')


def not_shipped_dash(request): #用來顯示未發貨的訂單
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
                status = request.POST['shipping_status']
                num = request.POST['num']
                # Get the order
                order = Order.objects.filter(id=num)
                # grab Date and Time
                now = datetime.datetime.now()
                # update order
                order.update(shipped= True,date_shipped=now)      
                # redirect
                messages.success(request,"Shipping Status Updated")
                return redirect('home')
            
        return render(request,"payment/not_shipped_dash.html",{"orders":orders})
    else:
        messages.success(request,"Access Denied")  #拒絕訪問" 或 "無權訪問
        return redirect('home')
  
  
    
def shipped_dash(request): #用來顯示已發貨的訂單
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped= True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the order
            order = Order.objects.filter(id=num)
            # grab Date and Time
            now = datetime.datetime.now()
            # update order
            order.update(shipped=False)      
            # redirect
            messages.success(request,"Shipping Status Updated")
            return redirect('home')      
   
        return render(request,"payment/shipped_dash.html",{"orders":orders})

    else:
        messages.success(request,"Access Denied")  #拒絕訪問" 或 "無權訪問
        return redirect('home')


#處理訂單的函式，通常用於電子商務網站中，處理用戶提交訂單的邏輯
def process_order(request):
    #接收POST請求
    if request.POST:
        # 1.獲取購物車中的商品信息：從 Cart 類別中取得購物車的商品信息，產品、數量（quantities）、和總價（totals）
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
    
        
        # 2.從PaymentForm表單中獲取[獲取付款信息 ]
        payment_form = PaymentForm(request.POST or None)
        
        # 3.獲取用戶的運輸信息（從 session 中獲取):運輸地址信息保存在用戶的session
        my_shipping = request.session.get('my_shipping')        
       
        # 4.提取訂單信息（姓名、郵箱和地址），根據用戶的登入狀態來創建訂單
        full_name = my_shipping['Shipping_full_name']
        email = my_shipping['Shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['Shipping_address1']}\n{my_shipping['Shipping_address2']}\n{my_shipping['Shipping_city']}\n{my_shipping['Shipping_state']}\n{my_shipping['Shipping_zipcode']}\n{my_shipping['Shipping_country']}"   
        amount_paid = totals
                
        # 5.創建訂單
        if request.user.is_authenticated:
            # logged in----如果用戶已登入，將訂單綁定到該用戶
            user = request.user
            #創建訂單
            create_order = Order(user=user,full_name=full_name, email= email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            
            # 6.添加訂單中的商品項目
            # Get the [order Id] 
            order_id = create_order.id
                # Get product Info
            for product in cart_products():
                # Get [product ID]
                product_id = product.id
                # Get [product price]
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                # Get [product quantity]
                for key,value in quantities().items(): 
                    if int(key) == product.id:
                       # create order item
                       create_order_item = OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price )
                       create_order_item.save() 
                    
                #解釋:
                # quantities() 返回一個字典，其中鍵是產品ID，值是該產品的數量。
                #.items() 返回這個字典的每一對鍵和值。
                #for key, value 用於遍歷這個字典，並在循環中對每個產品的 ID（key）和數量（value）進行處理。
                
                   
                # Delete our cart
                for key in list(request.session.keys()):
                    if key =="session_key":
                    # Delete the key
                        del request.session[key]
                        
                        
                # Delete cart from Datebase(old_cart field)
                current_user =Profile.objects.filter(user__id=request.user.id)
                # Delet shopping cart datebase (old_cart field)
                current_user.update(old_cart="")
                            
                messages.success(request,"Order Placed")
                return redirect('home')   
        else:
            # Not logged in
            # Create Order
            create_order = Order(full_name=full_name, email= email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            
            # Add order Items
            # Get the order Id
            order_id = create_order.id
            
            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                if product.is_saled:
                    price = product.sale_price
                else:
                    price = product.price
                
                # Get product quantity
                for key,value in quantities().items(): 
                    if int(key) == product.id:
                       # create order item
                       create_order_item = OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price )
                       create_order_item.save()
                       
                    # Delete our cart
                for key in list(request.session.keys()):
                    if key =="session_key":
                    # Delete the key
                        del request.session[key]   
                        
            messages.success(request,"Order Placed")
            return redirect('home')  
    
    else:
        #如果用戶以 GET 請求進入此頁面，顯示拒絕訪問消息
        messages.success(request,"Access Denied")
        return redirect('home')
    
    #(1)從購物車中提取商品、數量和總價格(2)從 session 中提取運輸信息(3)根據用戶是否已登錄創建訂單並保存(4)最後使用 Django 的 messages 模塊來顯示成功消息，並重定向到主頁。

#奇怪!! 影片34集
def billing_info(request):
    if request.POST :
        # Get the Cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        # Get the host
        host = request.get_host()
        #Create Paypal Form Dictionary
        paypal_dict = {
            'business' : settings.PAYPAL_RECEIVER_EMAIL,
            'amount' : totals,
            'item_name':'Book Order',
            'no_shipping':'2',
            'invoice': str(uuid.uuid4()),
            'currency_code':'USD',#EUR for Euros
            'notify_url':'https://{}{}'.format(host,reverse("paypal-ipn")),
            'return_url':'https://{}{}'.format(host,reverse("payment_success")),
            'cancel_return':'https://{}{}'.format(host,reverse("payment_failed")),
        }
        #Create actual paypal button 
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        #Check to see if user is logged in
        if request.user.is_authenticated :
            # Get Billing Form
            billing_form = PaymentForm()
            return render(request,"payment/billing_info.html",{"paypal_form":paypal_form,"cart_products": cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form })
        else: 
            billing_form = PaymentForm()
            return render(request,"payment/billing_info.html",{"paypal_form":paypal_form,"cart_products": cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form })
            
        #shipping_form = request.POST
        #return render(request,"payment/billing_info.html",{"cart_products": cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def checkout(request):
    # Get the Cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        # Checkout as logged in user
        # shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None ,instance=shipping_user)
        return render(request,"payment/checkout.html",{"cart_products": cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form  })
    else:
        #check as gest
        shipping_form = ShippingForm(request.POST or None ,instance=shipping_user)
        return render(request,"payment/checkout.html",{"cart_products": cart_products,"quantities":quantities,"totals":totals, "shipping_form":shipping_form })







def payment_success(request):
    return render(request,'payment/payment_success.html',{})


def payment_failed(request):
    return render(request,'payment/payment_failed.html',{})