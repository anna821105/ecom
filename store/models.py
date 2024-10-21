from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #Django 默認的 User 模型中只有基本信息，如用户名、電子郵件等。
    #Profile 模型通过 OneToOneField關聯到 User 模型，允許你為每个用户存檔更多的個人信息，如電話號碼、地址等。
    date_modified = models.DateTimeField(User,auto_now=True) 
    #auto_now=True: 每次保存對象時都會更新字段為當前時間，適合紀錄 "最后修改時間"。
    #auto_now_add=True: 只在對象首次創建時設置為當前時間，適合紀錄 "創建時間"。
    phone = models.CharField(max_length=20,blank=True)
    address1 = models.CharField(max_length=200,blank=True)
    address2 = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=20,blank=True)
    zipcode = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)
    old_cart = models.CharField(max_length=20,blank=True,null=True)
    
    def __str__(self):
        return self.user.username
    
   
    
#創建用户時，自動生成用戶檔案
#  Create a user profile by default when user signs up
def create_profile(sender,instance,created,**kwargs):
    #sender（發送信號的模型類），instance（當前創建的用戶實例），created（表示是否是新創建的實例），以及其他的關鍵字參數 **kwargs。
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
# Automate the profile thing
post_save.connect(create_profile,sender=User)
 #這行代碼將 create_profile 函數與 User 模型的 post_save 信號連接起來。
 # 意思是，每當一個 User 實例被保存後，Django 會觸發 post_save 信號，
 # 然後自動調用 create_profile 函數。這確保了每次創建新用戶時，都會自動生成對應的用戶資料。   




# categories of Prodcts
class Category (models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural ='categories'

    

    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    passsword = models.EmailField(max_length=100)
    
    def __str__(self):
        return f'{self.first_name}{self.last_name}'
    

    
class Product(models.Model):
    name =models.CharField(max_length=100)
    price =models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description =models.CharField(max_length=250,default='',blank=True,null= True)
    image = models.ImageField(upload_to='uploads/product/')
    #add sale stuff
    is_sale = models.BooleanField(default=False)
    sale_price =models.DecimalField(default=0,decimal_places=2,max_digits=6)
    
    
    def __str__(self):
        return self.name
    

#customer orders
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) 
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100,default='',blank=True)
    phone = models.CharField(max_length=20,default='',blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
  
    def __str__(self):
        return self.product
    