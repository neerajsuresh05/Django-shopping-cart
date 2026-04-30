from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_register/', views.user_register, name='user_register'),
    path('myadmin/', views.admin_view, name='admin_view'),
    path('add/',views.add,name='add'),
    path('view/',views.view,name='view'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('update/<int:id>/',views.update,name='update'),
    path('admin_panel',views.admin_panel,name='admin_panel'),
    path('logout/',views.logoutt,name='logout'),
    path('addcart/',views.addcart,name='addcart'),
    path('userview/',views.userview,name='userview'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('remove/<int:id>/', views.remove_item, name='remove_item'),
    path('place_order/', views.place_order, name='place_order')
]