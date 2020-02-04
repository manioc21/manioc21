
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from mainapp.models import *

# Create your views here.


@login_required(login_url='login')
def index(request):
	farmers = Farmer.objects.filter(history=True).values_list('data',flat=True)
	fields = Field.objects.filter(history=True).all()
	if request.user.is_admin == False:
		farmers = farmers.filter(data__coop=request.user.coop)
		fields = fields.filter(data__coop=request.user.coop)
	fields_total = fields.count()
	ready_fields = fields.filter(status='ready').count()
	not_ready_fields = fields.filter(status='not_ready').count()
	harvest_fields = fields.filter(status='harvest').count()
	farmers_total = len(farmers)
	context = {'fields':fields,'farmers':farmers,'farmers_total':farmers_total,'fields_total':fields_total,'ready_fields':ready_fields,'harvest_fields':harvest_fields,'not_ready_fields':not_ready_fields}
	return render(request,"history/index.html",context)


def get_images(obj):
	if obj.get('_attachments'):
		images = []
		for image in obj['_attachments']:
			images.append(image['small_download_url'])
		return images
	return "",""


@login_required(login_url='login')
def farmers(request):
	farmers = Farmer.objects.filter(history=True).values_list('data',flat=True)
	if request.user.is_admin == False:
		farmers = farmers.filter(data__coop=request.user.coop)
	status = request.GET.get('status')
	if status:
		farmers = farmers.filter(status=status)
	size = 0
	for farmer in farmers:
		size += farmer.get('farm/farmSize',0)
	return render(request,"history/farmers.html",{'farmers':farmers,'total_size':round(size,2),'status':status,'table':True})


@login_required(login_url='login')
def farmers_map(request):
	farmers = Farmer.objects.filter(history=True).values_list('data',flat=True)
	if request.user.is_admin == False:
		farmers = farmers.filter(data__coop=request.user.coop)
	return render(request,"history/farmers-map.html",{'farmers':farmers})


@login_required(login_url='login')
def single_farmer(request,id):
	farmer = get_object_or_404(Farmer,data___id=id,history=True)
	images = get_images(farmer.data)
	if request.GET.get('status'):
		farmer.status = request.GET.get('status')
		farmer.save()
	return render(request,"history/single-farmer.html",{'farmer':farmer.data,'status':farmer.get_status_display(),'images':images})


@login_required(login_url='login')
def fields(request):
	fields = Field.objects.filter(history=True).all()
	if request.user.is_admin == False:
		fields = fields.filter(data__coop=request.user.coop)
	status = request.GET.get('status')
	if status:
		fields = fields.filter(status=status) 
	return render(request,"history/fields.html",{'fields':fields,'table':True})


@login_required(login_url='login')
def fields_map(request):
	fields = Field.objects.filter(history=True).all()
	if request.user.is_admin == False:
		fields = fields.filter(data__coop=request.user.coop)
	return render(request,"history/fields-map.html",{'fields':fields})


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
	field = get_object_or_404(Field,data___id=id,history=True)
	points = get_field_points(field.data['trace'])
	if request.GET.get('status'):
		field.status = request.GET.get('status')
		field.save()
	return render(request,"history/single-field.html",{'field':field,'points':points})


@login_required(login_url='login')
def stock(request):
	stocks = Stock.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		stocks = stocks.filter(data__coop=request.user.coop)
	action = request.GET.get('action')
	if action:
		stocks = stocks.filter(data__action=action)
	return render(request,"history/stock.html",{'stocks':stocks,'table':True})


@login_required(login_url='login')
def single_stock(request,id):
	stock = get_object_or_404(Stock,data___id=id,history=True).data
	return render(request,"history/single-stock.html",{'stock':stock,'table':True})



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
	count = Stock.objects.filter(data__action='count',data__coop=coop,history=True).order_by('data__end').values_list('data', flat=True).last()
	date = count['end']
	received = Stock.objects.filter(data__action='receive',data__end__gt=date,data__coop=coop,history=True).values_list('data', flat=True)
	withdraw = Stock.objects.filter(data__action='withdraw',data__end__gt=date,data__coop=coop,history=True).values_list('data', flat=True)
	#import pdb;pdb.set_trace()
	for item in withdraw:
		for data in item['productDetails']:
			data['productDetails/quantity'] = data['productDetails/quantity']*-1
	total_data = [count] + list(received) + list(withdraw)
	return format_stock(total_data)


def available_stock_all():
	count = Stock.objects.filter(data__action='count',history=True).order_by('data__end').values_list('data', flat=True).last()
	date = count['end']
	received = Stock.objects.filter(data__action='receive',data__end__gt=date,history=True).values_list('data', flat=True)
	withdraw = Stock.objects.filter(data__action='withdraw',data__end__gt=date,history=True).values_list('data', flat=True)
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
		stocks = Stock.objects.filter(data__action=action,history=True).values_list('data', flat=True)
		if request.user.is_admin == False:
			stocks = stocks.filter(data__coop=request.user.coop)
		data = format_stock(stocks)
	return render(request,"history/stock-action.html",{'product_details':data,'action':actions[action],'table':True})


@login_required(login_url='login')
def stock_map(request):
	stocks = Stock.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		stocks = stocks.filter(data__coop=request.user.coop)
	return render(request,"history/stock-map.html",{'stocks':stocks})


@login_required(login_url='login')
def pest(request):
	pests = Pest.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		pests = pests.filter(data__coop=request.user.coop)
	return render(request,"history/pests.html",{'pests':pests,'table':True})


@login_required(login_url='login')
def single_pest(request,id):
	pest = get_object_or_404(Pest,data___id=id,history=True).data
	images = get_images(pest)
	pest['geolocation'] = Field.objects.get(data__fieldID=pest['fieldID']).data['geolocation']
	return render(request,"history/single-pest.html",{'pest':pest,'images':images,'table':True})


@login_required(login_url='login')
def pest_map(request):
	pests = Pest.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		pests = pests.filter(data__coop=request.user.coop)
	for pest in pests:
		pest['geolocation'] = [None,None]
		field = Field.objects.filter(data__fieldID=pest['fieldID']).last()
		if field:
			pest['geolocation'] = field.data['geolocation']
	return render(request,"history/pest-map.html",{'pests':pests})


@login_required(login_url='login')
def sales(request):
	sales = Sales.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		sales = sales.filter(data__coop=request.user.coop)
	total_price = 0
	for sale in sales:
		total_price += int(sale["totalPrice"])
	return render(request,"history/sales.html",{'sales':sales,'total_price':total_price,'table':True})



@login_required(login_url='login')
def single_sale(request,id):
	sale = get_object_or_404(Sales,data___id=id,history=True).data
	return render(request,"history/single-sale.html",{'sale':sale,'table':True})


@login_required(login_url='login')
def sales_map(request):
	sales = Sales.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		sales = sales.filter(data__coop=request.user.coop)
	return render(request,"history/sales-map.html",{'sales':sales})


@login_required(login_url='login')
def supplies(request):
	supplies = Supply.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		supplies = supplies.filter(data__coop=request.user.coop)
	total_value = 0
	total_weight = 0
	for supply in supplies:
		total_value += int(supply['totalDelivery/totalValue'].replace(' XAF','').replace(' CDF',''))
		total_weight += float(supply['totalDelivery/totalWeight'].replace(' kg',''))
	return render(request,"history/supplies.html",{'supplies':supplies,'table':True,'total_value':total_value,'total_weight':total_weight})


@login_required(login_url='login')
def supply_map(request):
	supplies = Supply.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		supplies = supplies.filter(data__coop=request.user.coop)
	return render(request,"history/supply-map.html",{'supplies':supplies})

@login_required(login_url='login')
def single_supply(request,id):
	supply = get_object_or_404(Supply,data___id=id,history=True).data
	return render(request,"history/single-supply.html",{'supply':supply,'table':True})


@login_required(login_url='login')
def transformed_products(request):
	products = TransformedProduct.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		products = products.filter(data__coop=request.user.coop)
	total_weight = 0
	for product in products:
		total_weight += product.get('totalWeight_raw',0)
	return render(request,"history/transformed_products.html",{'products':products,'table':True,'total_weight':total_weight})


@login_required(login_url='login')
def single_product(request,id):
	product = get_object_or_404(TransformedProduct,data___id=id,history=True).data
	return render(request,"history/single-product.html",{'product':product,'table':True})

@login_required(login_url='login')
def products_map(request):
	products = TransformedProduct.objects.filter(history=True).values_list('data', flat=True)
	if request.user.is_admin == False:
		products = products.filter(data__coop=request.user.coop)
	return render(request,"history/products-map.html",{'products':products})


def payments(request):
	payments = Payment.objects.filter(history=True).all().order_by('-id')
	return render(request,"history/payments.html",{'payments':payments,'table':True})\


