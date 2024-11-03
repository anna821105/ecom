from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User



admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
#創建 OrderItemInline，用來在編輯 Order 的管理頁面時同時顯示和編輯與該訂單相關的 OrderItem。
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0  #不會預先顯示任何額外的空白行來添加新項目。只會顯示已經存在的 OrderItem 條目，若你想添加新條目，需要點擊「添加」按鈕。
    
# Extend our Order Model 
#擴展了 Order 模型的管理方式，將 OrderItemInline 作為 Order 的內聯模型。這樣可以在管理 Order 時同時管理其下的 OrderItem。   
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"] #這行代碼表示在 Django 管理後台中，date_ordered 欄位將設為只讀，這意味著後台管理員無法修改該欄位的值。
    fields = ["user","full_name","email","shipping_address","amount_paid","date_ordered","shipped","date_shipped","invoice","paid"]
    inlines =[OrderItemInline]
    
# Unregister Order Model
admin.site.unregister(Order)

# Re-Register our Order AND orderItems
admin.site.register(Order,OrderAdmin)
