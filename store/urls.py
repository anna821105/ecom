from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('update_password/',views.update_password,name='update_password'),
    path('update_user/',views.update_user,name='update_user'),
    path('update_info/',views.update_info,name='update_info'),
    path('product/<int:pk>',views.product,name='product'), # product/ 開頭，後面跟著一個整數 (<int:pk>) 作為參數
    path('category/<str:foo>',views.category,name='category'),
    path('category_summary/',views.category_summary,name='category_summary'),
    path('search/',views.search,name='search'),
]



#<str:foo> 是動態部分，<str:> 指定參數的類型為字符串（str），foo 是參數名。
# 這意味著你可以在 URL 中傳遞任何字串（不包含 /），
# 例如 /category/electronics 或 /category/clothing。