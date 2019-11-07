

from django.urls import path
from .views import *

urlpatterns = [
    path('farmers/', farmers,name="farmers"),
    path('farmers-map/', farmers_map,name="farmers-map"),
    path('farmer/<int:id>', single_farmer,name="single-farmer"),
    path('',index,name="index"),
    path('fields/',fields,name="fields"),
    path('fields-map/',fields_map,name="fields-map"),
    path('field/<int:id>', single_field,name="single-field"),
    path('stock/',stock,name="stock"),
    path('stock-action/<str:action>',stock_action,name="stock-action"),
    path('stock-map/',stock_map,name="stock-map"),
    path('stock/<int:id>',single_stock,name="single-stock"),
    path('sales/',sales,name="sales"),
    path('sales-map/',sales_map,name="sales-map"),
    path('single-sale/<int:id>',single_sale,name="single-sale"),
    path('pests/',pest,name="pests"),
    path('pest-map/',pest_map,name="pest-map"),
    path('single-pest/<int:id>',single_pest,name="single-pest"),
    path('supplies/',supplies,name="supplies"),
    path('supply-map/',supply_map,name="supply-map"),
    path('single-supply/<int:id>',single_supply,name="single-supply"),
    path('transformed-products/',transformed_products,name="transformed-products"),
    path('single-product/<int:id>',single_product,name="single-product"),
    path('products-map/',products_map,name="products-map"),
    path('payments/',payments,name="payments"),
    path('login/',signin,name="login"),
    path('webhook/<str:table>',webhook,name="webhook"),
    path('logout/',signout,name="logout"),
    path('change-password/',change_password,name="change-password"),
    path('create-account/',create_account,name="create-account"),
    path('user-accounts/',user_accounts,name="user-accounts"),
    path('message',message,name="message")
]