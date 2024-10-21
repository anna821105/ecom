#Session 是用來在不同的 HTTP 請求之間存儲和管理用戶數據的一種機制。
# 由於 HTTP 是一種無狀態的協議，每次請求都獨立存在，
# 因此如果你想要在用戶每次訪問網站時保持某些數據(例如購物車內容、用戶登錄狀態），就需要用到 Session。
#主要特點：持久化數據：Session 允許你在服務器端存儲用戶數據，而這些數據可以在多次請求之間保留，直到 Session 到期或被手動清除。
#與 Cookie 配合使用：Django 通常使用 Cookie 來保存 Session 的唯一標識符（sessionid），具體的數據保存在服務器端，而不會直接暴露在 Cookie 中。
#自動管理：Django 自帶的 Session 框架會自動處理 Session 的創建、存儲和清理工作。

from store.models import Product,Profile


class Cart():
    def __init__(self, request):
        self.session = request.session #獲取當前請求的會話對象
        # Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        
        #if the user is new, no session key! create one!
        if 'session_key' not in request.session :
            cart = self.session ['session_key'] = {}
        
        # make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self,product,quantity):
        product_id = str(product) 
        product_qyt = str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qyt)
            
        self.session.modified =  True
        
        # Deal With logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user  = Profile.objects.filter(user__id= self.request.user.id)
            # convert{'3':1,'6':2} to {"3":1,"6":2}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


    def add(self,product,quantity):
        #{'3':5,'6':2}
        product_id = str(product.id) # 字串
        product_qyt = str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qyt)
            
        self.session.modified =  True
        
        # Deal With logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user  = Profile.objects.filter(user__id= self.request.user.id)
            # convert{'3':1,'6':2} to {"3":1,"6":2}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
            
        
        
    def cart_total(self):
        # get product IDS
        product_ids = self.cart.keys()
        #lookup those keys in our products database models
        products = Product.objects.filter(id__in=product_ids)
        # get the quantities
        quantities = self.cart
        #start counting at 0
        total = 0   
        for key,value in quantities.items():
            # convert key string into so we can do math
            key = int(key)
            for product in products :
                if product.id == key:
                    if product.is_sale :
                        total = total + (product.sale_price*value)
                    else:
                        total = total + (product.price*value)
        return total
                       
    

    def __len__(self):
        return len(self.cart) 
    

    def get_prods(self):
        # get ids from
        product_ids = self.cart.keys()       
        # use ids to lookup products in datebase  model
        products = Product.objects.filter(id__in=product_ids)

        # return those looked up products
        return products
        
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    
    
    def update(self,product,quantity):
        product_id = str(product) # 將product 轉为字符串，作為字典格式
        product_qty = int(quantity) #將 quantity 轉為整数，作為商品數量
        
        # Get cart 獲取購物車
        ourcart = self.cart
        # update Dictionary/cart 更新購物車（字典）
        ourcart[product_id] = product_qty
        
        self.session.modified = True
        
        # Deal With logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user  = Profile.objects.filter(user__id= self.request.user.id)
            # convert{'3':1,'6':2} to {"3":1,"6":2}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
          
        thing = self.cart
        return thing
    
        
    def delete(self,product):
        #{'3':4,'2':2}
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True
        
        # Deal With logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user  = Profile.objects.filter(user__id= self.request.user.id)
            # convert{'3':1,'6':2} to {"3":1,"6":2}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
        
        
        
        
        
        
        
#>>> from django.contrib.sessions.models import Session   
#>>> session_k = Session.objects.get(pk='vupdg9kh91j4vdv4pcwmssb76xgdtmrt')                   
#>>> session_k.get_decoded()
#{'_auth_user_id': '1', '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
# '_auth_user_hash': '0079b650b7cec59a808e93c678a3453741ce408c868c8d6bd09330a0ee21058e',
# 'session_key': {}}

#----------
#from django.contrib.sessions.models import Session 
# k = Session.objects.get(pk='fmujuya34v22tjclv0tsolnlcms8gwva')
# k.get_decoded()
#{'session_key': {'2': {'price': '5555.00'}}, '_auth_user_id': '1', 
# '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
# '_auth_user_hash': '0079b650b7cec59a808e93c678a3453741ce408c868c8d6bd09330a0ee21058e'}