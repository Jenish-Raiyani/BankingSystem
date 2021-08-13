from django.urls import path
from . import views
app_name = 'BankApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.customer_data, name='customer_data'),
    path('history/',views.history,name='history'),
    path('tansaction/<int:cust_id>',views.data,name='tansaction'),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    
]

