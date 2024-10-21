from .cart import Cart

#create context processors so our cart can work on at all pages on site 
# 創建上下文處理器，以便購物車可以在網站的所有頁面上使用

def cart(request):
    # return the default data from our Cart 返回來自 Cart 的默認數據
    return {'cart': Cart(request)}











