from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save,pre_save
#post_save 和 pre_save 是 Django 提供的信號（signals），
#用來在模型保存之前或之後執行一些自定義的操作。
#這些信號通常用來實現邏輯，比如自動填充字段、發送通知、更新其他模型等等。
#pre_save: (1)作用:當模型的 save() 方法被調用之前觸發。(2)用途: 可以用來進行一些數據的處理、驗證，或在保存之前自動設置某些字段的值。
#post_save:(1)作用: 當模型的 save() 方法被成功調用且模型數據已經保存到數據庫之後觸發。(2)用途: 可以用來執行一些操作，如創建關聯模型的實例、發送電子郵件通知、或記錄日誌。
from django.dispatch import receiver
import datetime



# -------在網路購物系統或電子商務應用中，Shipping Address（配送地址） 是用來記錄用戶希望商品送達的具體地點
class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Shipping_full_name = models.CharField(max_length=255)
    Shipping_email = models.CharField(max_length=255)
    Shipping_address1 = models.CharField(max_length=255)
    Shipping_address2 = models.CharField(max_length=255,null= True,blank=True)
    Shipping_city = models.CharField(max_length=255)
    Shipping_state = models.CharField(max_length=255,null= True,blank=True)# null=True允許如果沒有值
    Shipping_zipcode = models.CharField(max_length=255,null= True,blank=True)
    Shipping_country = models.CharField(max_length=255)
    
    # Don't pluralize address
    class Meta :
        verbose_name_plural = "Shipping Address"
    # verbose_name_plural----Django會自動為模型名稱加上「s」來生成複數形式。
    # 例如，模型 ShippingAddress 的複數名稱會變成 ShippingAddresss，這樣顯然是不合語法的
    
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
    #f'...' 是 Python 的一種" 格式化字串語法"， 稱為「f-strings」，它允許你在字串中直接插入變量或表達式
    #語法:在字串前加上 f 或 F，並在字串內使用大括號 {} 將變量或表達式包裹起來，Python 會自動將大括號內的內容替換為對應的值。
 
#  Create a user Shipping Addresss by default when user signs up
def create_shipping(sender,instance,created,**kwargs):
    #sender（發送信號的模型類），instance（當前創建的用戶實例），created（表示是否是新創建的實例），以及其他的關鍵字參數 **kwargs。
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping,sender=User)
 
 
   
# Create Order Model 訂單
class Order(models.Model):
    # Foreignkey
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7,decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False) #默認值是未發貨
    date_shipped = models.DateTimeField(blank=True,null=True)#發貨日期，允許為空（blank=True, null=True），當 shipped 設為 True 時可以用來記錄發貨日期。
    
    def __str__(self):
        return f'Order - {str(self.id)}'

# Auto Add shipping Date
@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender,instance,**kwargs):
    if instance.pk:     #檢查訂單是否已經存在於數據庫中，確保這是更新操作而不是創建新訂單（instance.pk 只有在對象存在於數據庫中時才有值）。
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped =  now

#初始訂單創建時：shipped=False、date_shipped 不設置 ; 後續標記為已發貨時：更新 shipped=True，且自動將 date_shipped 設為當前時間。


# Create Order Items Model 
class OrderItem(models.Model):
    # Foreign Key
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7,decimal_places=2)

    def __str__(self):
        return f'Order Item -{str(self.id)}'
    