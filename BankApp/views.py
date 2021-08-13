from django.shortcuts import render, redirect
from django.contrib import messages
import re
from  .models import customer
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from  .models import transfer_history
from io import BytesIO


customerList = customer.objects.all()
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        current_user = request.user
        cust_id=current_user.id
        transaction_history=transfer_history.objects.get(id=50) 
        customers = customer.objects.get(id=6)
       
        
        data={
        
              'sender' :transaction_history.sender,
              'receiver' :transaction_history.receiver,
               'email':customers.email,
             
              'amount':transaction_history.amount,
            'timestamp' : transaction_history.timestamp,
            'order': transaction_history,
        }
        #print(transaction_history)
        #print(data)
        pdf = render_to_pdf('pdf_template.html',data)
        return HttpResponse(pdf, content_type='application/pdf')
        
def home(request):
    return render(request,'index.html',{'customers':customerList})

def data(request,cust_id):
    sender = customer.objects.get(id=cust_id)
    if request.method == 'POST':
        receiver_data = request.POST['receiver']
        amount = float(request.POST['amount'])
        if receiver_data != 'Select Customer':
            receiver = customer.objects.get(id=receiver_data)
            if amount > sender.balance:
                messages.error(request, 'Insufficient balance in your account')   
            elif amount == 0:
                messages.error(request, 'Please Enter Valid Amount')  
            else:
                receiver.balance = (receiver.balance+amount)
                receiver.save()
                sender.balance = (sender.balance-amount)
                sender.save()
                transfer_money = transfer_history(sender=sender,receiver=receiver,amount=amount)
                transfer_money.save()
                messages.success(request, 'Amount Transfered Successfuly')  
        else:
            messages.error(request, 'Please Select Customer')  
    return render(request,'tansaction.html',{'customer_list':customerList, 'sender':sender})

def customer_data(request):
    customerList = customer.objects.all().order_by('id')
    return render(request, 'customer.html',{'customers':customerList})

def history(request):
    transaction_history = transfer_history.objects.all().order_by('-id')
    return render(request,'history.html',{'transfer_history':transaction_history})
