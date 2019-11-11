from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from mainapp.messages import handle_sms
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


def signin(request):
	error = None
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			login(request,user)
			return redirect('index')
		error = 'invalid username or password'
	return render(request,"login.html",{'error':error})


def signout(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def index(request):
	farmers = Farmer.objects.values_list('data',flat=True)
	fields = Field.objects.all()
	if request.user.is_admin == False:
		farmers = farmers.filter(data__coop=request.user.coop)
		fields = fields.filter(data__coop=request.user.coop)
	fields_total = fields.count()
	ready_fields = fields.filter(status='ready').count()
	not_ready_fields = fields.filter(status='not_ready').count()
	harvest_fields = fields.filter(status='harvest').count()
	farmers_total = len(farmers)
	context = {'fields':fields,'farmers':farmers,'farmers_total':farmers_total,'fields_total':fields_total,'ready_fields':ready_fields,'harvest_fields':harvest_fields,'not_ready_fields':not_ready_fields}
	return render(request,"index.html",context)


def get_images(obj):
	if obj.get('_attachments'):
		images = []
		for image in obj['_attachments']:
			images.append(image['small_download_url'])
		return images
	return "",""


@login_required(login_url='login')
def farmers(request):
	farmers = Farmer.objects.values_list('data',flat=True)
	if request.user.is_admin == False:
		farmers = farmers.filter(data__coop=request.user.coop)
	size = 0
	for farmer in farmers:
		size += farmer.get('farm/farmSize',0)
	return render(request,"farmers.html",{'farmers':farmers,'total_size':size,'table':True})


@login_required(login_url='login')
def farmers_map(request):
	farmers = Farmer.objects.values_list('data',flat=True)
	if request.user.is_admin == False:
		farmers = farmers.filter(data__coop=request.user.coop)
	return render(request,"farmers-map.html",{'farmers':farmers})


@login_required(login_url='login')
def single_farmer(request,id):
	farmer = get_object_or_404(Farmer,data___id=id).data
	images = get_images(farmer)
	return render(request,"single-farmer.html",{'farmer':farmer,'images':images})


@login_required(login_url='login')
def fields(request):
	fields = Field.objects.all()
	if request.user.is_admin == False:
		fields = fields.filter(data__coop=request.user.coop)
	status = request.GET.get('status')
	if status:
		fields = fields.filter(status=status) 
	return render(request,"fields.html",{'fields':fields,'table':True})


@login_required(login_url='login')
def fields_map(request):
	fields = Field.objects.all()
	if request.user.is_admin == False:
		fields = fields.filter(data__coop=request.user.coop)
	return render(request,"fields-map.html",{'fields':fields})


def get_field_points(trace):
	marks = trace.split(';')
	points = []
	for mark in marks:
		coords = mark.split()
		if coords == []:
			continue
		points.append({'lat':float(coords[0]),'lng':float(coords[1])})
	return points


@login_required(login_url='login')
def single_field(request,id):
	field = get_object_or_404(Field,data___id=id)
	points = get_field_points(field.data['trace'])
	return render(request,"single-field.html",{'field':field,'points':points})


@login_required(login_url='login')
def stock(request):
	stocks = Stock.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		stocks = stocks.filter(data__coop=request.user.coop)
	action = request.GET.get('action')
	if action:
		stocks = stocks.filter(data__action=action)
	return render(request,"stock.html",{'stocks':stocks,'table':True})


@login_required(login_url='login')
def single_stock(request,id):
	stock = get_object_or_404(Stock,data___id=id).data
	return render(request,"single-stock.html",{'stock':stock,'table':True})



def format_stock(stocks):
	details = []
	for stock in stocks:
		details.extend(stock['productDetails'])
	data = []
	for detail in details:
		pr = detail['productDetails/product']
		unit = detail.get('productDetails/unit',detail.get('productDetails/productUnit'))
		weight = detail['productDetails/weight']
		total_q = 0
		for detail in details:
			if pr == detail['productDetails/product'] and unit == detail.get('productDetails/unit',detail.get('productDetails/productUnit')) and weight == detail['productDetails/weight']:
				total_q += detail['productDetails/quantity']
		data.append({'productDetails/unit':unit,'productDetails/product':pr,'productDetails/weight':weight,'productDetails/quantity':total_q})
	return [dict(t) for t in {tuple(d.items()) for d in data}]


def available_stock(coop):
	count = Stock.objects.filter(data__action='count',data__coop=coop).order_by('data__end').values_list('data', flat=True).last()
	date = count['end']
	received = Stock.objects.filter(data__action='receive',data__end__gt=date,data__coop=coop).values_list('data', flat=True)
	withdraw = Stock.objects.filter(data__action='withdraw',data__end__gt=date,data__coop=coop).values_list('data', flat=True)
	#import pdb;pdb.set_trace()
	for item in withdraw:
		for data in item['productDetails']:
			data['productDetails/quantity'] = data['productDetails/quantity']*-1
	total_data = [count] + list(received) + list(withdraw)
	return format_stock(total_data)


def available_stock_all():
	count = Stock.objects.filter(data__action='count').order_by('data__end').values_list('data', flat=True).last()
	date = count['end']
	received = Stock.objects.filter(data__action='receive',data__end__gt=date).values_list('data', flat=True)
	withdraw = Stock.objects.filter(data__action='withdraw',data__end__gt=date).values_list('data', flat=True)
	#import pdb;pdb.set_trace()
	for item in withdraw:
		for data in item['productDetails']:
			data['productDetails/quantity'] = data['productDetails/quantity']*-1
	total_data = [count] + list(received) + list(withdraw)
	return format_stock(total_data)

actions = {'available':'Disponible','receive':'Recevoir','count':'Compter','withdraw':'Retirer'}

@login_required(login_url='login')
def stock_action(request,action):
	data = []
	if action == 'available':
		if not request.user.is_admin:
			data = available_stock(request.user.coop)
		else:
			data = available_stock_all()
	elif action == "all":
		return redirect('stock')
	else:
		stocks = Stock.objects.filter(data__action=action).values_list('data', flat=True)
		if request.user.is_admin == False:
			stocks = stocks.filter(data__coop=request.user.coop)
		data = format_stock(stocks)
	return render(request,"stock-action.html",{'product_details':data,'action':actions[action],'table':True})


@login_required(login_url='login')
def stock_map(request):
	stocks = Stock.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		stocks = stocks.filter(data__coop=request.user.coop)
	return render(request,"stock-map.html",{'stocks':stocks})


@login_required(login_url='login')
def pest(request):
	pests = Pest.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		pests = pests.filter(data__coop=request.user.coop)
	return render(request,"pests.html",{'pests':pests,'table':True})


@login_required(login_url='login')
def single_pest(request,id):
	pest = get_object_or_404(Pest,data___id=id).data
	images = get_images(pest)
	pest['geolocation'] = Field.objects.get(data__fieldID=pest['fieldID']).data['geolocation']
	return render(request,"single-pest.html",{'pest':pest,'images':images,'table':True})


@login_required(login_url='login')
def pest_map(request):
	pests = Pest.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		pests = pests.filter(data__coop=request.user.coop)
	for pest in pests:
		pest['geolocation'] = [None,None]
		field = Field.objects.filter(data__fieldID=pest['fieldID']).last()
		if field:
			pest['geolocation'] = field.data['geolocation']
	return render(request,"pest-map.html",{'pests':pests})


@login_required(login_url='login')
def sales(request):
	sales = Sales.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		sales = sales.filter(data__coop=request.user.coop)
	total_price = 0
	for sale in sales:
		total_price += int(sale["totalPrice"])
	return render(request,"sales.html",{'sales':sales,'total_price':total_price,'table':True})



@login_required(login_url='login')
def single_sale(request,id):
	sale = get_object_or_404(Sales,data___id=id).data
	return render(request,"single-sale.html",{'sale':sale,'table':True})


@login_required(login_url='login')
def sales_map(request):
	sales = Sales.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		sales = sales.filter(data__coop=request.user.coop)
	return render(request,"sales-map.html",{'sales':sales})


@login_required(login_url='login')
def supplies(request):
	supplies = Supply.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		supplies = supplies.filter(data__coop=request.user.coop)
	total_value = 0
	total_weight = 0
	for supply in supplies:
		total_value += int(supply['totalDelivery/totalValue'].replace(' XAF','').replace(' CDF',''))
		total_weight += float(supply['totalDelivery/totalWeight'].replace(' kg',''))
	return render(request,"supplies.html",{'supplies':supplies,'table':True,'total_value':total_value,'total_weight':total_weight})


@login_required(login_url='login')
def supply_map(request):
	supplies = Supply.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		supplies = supplies.filter(data__coop=request.user.coop)
	return render(request,"supply-map.html",{'supplies':supplies})

@login_required(login_url='login')
def single_supply(request,id):
	supply = get_object_or_404(Supply,data___id=id).data
	return render(request,"single-supply.html",{'supply':supply,'table':True})


@login_required(login_url='login')
def transformed_products(request):
	products = TransformedProduct.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		products = products.filter(data__coop=request.user.coop)
	total_weight = 0
	for product in products:
		total_weight += product['totalWeight_raw']
	return render(request,"transformed_products.html",{'products':products,'table':True,'total_weight':total_weight})


@login_required(login_url='login')
def single_product(request,id):
	product = get_object_or_404(TransformedProduct,data___id=id).data
	return render(request,"single-product.html",{'product':product,'table':True})

@login_required(login_url='login')
def products_map(request):
	products = TransformedProduct.objects.values_list('data', flat=True)
	if request.user.is_admin == False:
		products = products.filter(data__coop=request.user.coop)
	return render(request,"products-map.html",{'products':products})


def payments(request):
	payments = Payment.objects.all().order_by('-id')
	return render(request,"payments.html",{'payments':payments,'table':True})\


@login_required(login_url='login')
def change_password(request):
	user = request.user
	if request.method == 'POST':
		pass_1 = request.POST.get('password1')
		pass_2 = request.POST.get('password2')
		if pass_2 == pass_1:
			user.set_password(pass_1)
			user.save()
			logout(request)
			return redirect('login')
		error = 'Passwords dont match'
		return render(request,"change-password.html",{'error':error})
	return render(request,"change-password.html")


@login_required(login_url='login')
def create_account(request):
	coop = request.user.coop
	if not request.user.coop_admin:
		return redirect('index')
	if request.method == 'POST':
		pass_1 = request.POST.get('password1')
		pass_2 = request.POST.get('password2')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		phone = request.POST.get('phone')
		username = request.POST.get('username')
		if User.objects.filter(username=username).exists():
			error = 'Username exists, try another one'
			return render(request,"create-account.html",{'error':error})
		if pass_2 == pass_1:
			user = User.objects.create_user(username=username,password=pass_1,coop=coop)
			user.coop_admin = False
			user.fname = fname
			user.lname = lname
			user.phone = phone
			user.save()
			return redirect('user-accounts')
		error = 'Passwords dont match'
		return render(request,"create-account.html",{'error':error})
	return render(request,"create-account.html")

@login_required(login_url='login')
def user_accounts(request):
	if not request.user.coop_admin:
		return redirect('index')
	if request.GET.get('id'):
		u = User.objects.get(id=request.GET.get('id'))
		u.delete()
	users = User.objects.filter(coop=request.user.coop,is_admin=False)
	return render(request,"user-accounts.html",{'users':users})



@csrf_exempt
def webhook(request,table):
	body = request.body.decode('utf-8')
	data = json.loads(body)
	coop,created = User.objects.get_or_create(username=data['coop'],coop=data['coop'])
	if created:
		coop.set_password('admin')
		coop.save()
	if table == 'stock':
		Stock.objects.get_or_create(coop=coop,data=data)
	elif table == 'farmers':
		Farmer.objects.get_or_create(coop=coop,data=data)
	elif table == 'fields':
		Field.objects.get_or_create(coop=coop,data=data)
	elif table == 'pests':
		Pest.objects.get_or_create(coop=coop,data=data)
	elif table == 'sales':
		Sales.objects.get_or_create(coop=coop,data=data)
	elif table == 'supplies':
		Supply.objects.get_or_create(coop=coop,data=data)
	elif table == 'products':
		TransformedProduct.objects.get_or_create(coop=coop,data=data)
	return HttpResponse('ok')


from twilio import twiml
from twilio.rest import Client

account_sid = 'ACdbf0b9a6ea0df3c36c3d8085a9aa2485'
auth_token = 'a8e906d199d36f05a920fbedcd64d7a2'

from twilio.twiml.messaging_response import MessagingResponse

client = Client(account_sid, auth_token)

def send_sms(body,to):
	message = client.messages.create(
                              body=body,
                              from_='+12563636237',
                              to=to
                          )
	


@csrf_exempt
def message(request):
	body = request.POST.get('Body')
	phone = request.POST.get('From')
	message = Message(body=body,phone=phone)
	message.save()
	msg = None
	try:
		msg = handle_sms(body,phone)
	except:
		chat = Chat.objects.filter(phone=phone).last()
		if chat:
			chat.delete()
		msg = "Wrong message"
	resp = "<Response><Message>{}</Message></Response>".format(msg)
	return HttpResponse(resp, content_type='text/xml')