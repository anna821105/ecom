from django.contrib import admin
from .models import Category,Customer,Product,Order,Profile
from django.contrib.auth.models import User

# Register your models here. 模型註冊到 Django 管理後台，這樣可以在後台介面中管理這些模型的數據。
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile  #-----指定這個內嵌模型是 Profile。
    
    #ProfileInline這是一個內嵌類，使用 admin.StackedInline 來將 Profile 模型的資料內嵌到 UserAdmin 中。
    # 這樣在編輯 User 模型時，可以同時編輯與之相關聯的 Profile 資料。

    
    
# Extent User Model
class UserAdmin(admin.ModelAdmin):
    # UserAdmin 類，並使用了 admin.ModelAdmin。該類允許你自定義用戶模型的顯示和編輯方式。
    model = User
    field =["username","first_name","last_name","email"] 
    #指定在後台用戶編輯介面中顯示和編輯的欄位為用戶名、名字、姓氏和電子郵件。
    inlines = [ProfileInline] 
    #inlines = [ProfileInline] 將之前定義的 ProfileInline 內嵌類加入到用戶編輯介面，
    # 這樣可以在編輯用戶時也能直接編輯對應的 Profile 資料。
    
    
# Unregister the old way 是將 Django 自帶的 User 模型的默認註冊方式取消掉
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User,UserAdmin)
#通過 admin.site.register(User, UserAdmin) 使用自定義的 UserAdmin 類重新註冊 User 模型。這樣，
# 管理後台顯示的用戶編輯介面就使用了自定義的樣式，包含了 Profile 的內嵌編輯功能。