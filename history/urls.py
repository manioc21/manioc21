

from django.urls import path
from history.views import *

urlpatterns = [
    path('farmers/', farmers,name="history-farmers"),
    path('farmers-map/', farmers_map,name="history-farmers-map"),
    path('farmer/<int:id>', single_farmer,name="history-single-farmer"),
    path('',index,name="history-index"),
    path('fields/',fields,name="history-fields"),
    path('fields-map/',fields_map,name="history-fields-map"),
    path('field/<int:id>', single_field,name="history-single-field"),
    path('stock/',stock,name="history-stock"),
    path('stock-action/<str:action>',stock_action,name="history-stock-action"),
    path('stock-map/',stock_map,name="history-stock-map"),
    path('stock/<int:id>',single_stock,name="history-single-stock"),
    path('sales/',sales,name="history-sales"),
    path('sales-map/',sales_map,name="history-sales-map"),
    path('single-sale/<int:id>',single_sale,name="history-single-sale"),
    path('pests/',pest,name="history-pests"),
    path('pest-map/',pest_map,name="history-pest-map"),
    path('single-pest/<int:id>',single_pest,name="history-single-pest"),
    path('supplies/',supplies,name="history-supplies"),
    path('supply-map/',supply_map,name="history-supply-map"),
    path('single-supply/<int:id>',single_supply,name="history-single-supply"),
    path('transformed-products/',transformed_products,name="history-transformed-products"),
    path('single-product/<int:id>',single_product,name="history-single-product"),
    path('products-map/',products_map,name="history-products-map"),
    path('payments/',payments,name="history-payments"),
]