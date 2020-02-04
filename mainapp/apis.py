import requests



auth = ('danielkimassai','mylenana')


def get_geopoint(trace):
	if trace:
		trace = trace.split(";")
		trace = trace[0].split(" ")
		return trace
	return None

def get_fields():
	res = requests.get('https://api.ona.io/api/v1/data/401002',auth=auth)
	fields = res.json()
	for field in fields:
		try:
			field['geolocation'] = get_geopoint(field.get('trace'))
			field['manager'] = field['ownershipDetails/manager']
			field['owner'] = field['ownershipDetails/owner']
			field['ownershipType'] = field['ownershipDetails/ownershipType']
			field['variety'] = field['varietyDetails/variety']
			field['harvestdate'] = field.get('schedule/harvestDate',field.get('harvestdate'))
		except KeyError:
			field['geolocation'] = get_geopoint(field.get('trace'))
			field['manager'] = field.get('fieldDetails/manager')
			field['owner'] = field.get('fieldDetails/owner')
			field['ownershipType'] = field.get('fieldDetails/ownershipType')
			field['variety'] = field.get('varietyDetails/variety')
			field['harvestdate'] = field.get('schedule/harvestDate',field.get('harvestdate'))
	return fields

def get_farmers():
	res = requests.get('https://api.ona.io/api/v1/data/401455',auth=auth)
	farmers = res.json()
	return farmers

def get_stock():
	res = requests.get('https://api.ona.io/api/v1/data/401824',auth=auth)
	stocks = res.json()
	return stocks

def get_sales():
	res = requests.get('https://api.ona.io/api/v1/data/401351',auth=auth)
	sales = res.json()
	return sales

def get_supplies():
	res = requests.get('https://api.ona.io/api/v1/data/439613',auth=auth)
	supplies = res.json()
	return supplies

def get_transformedproducts():
	res = requests.get('https://api.ona.io/api/v1/data/401156',auth=auth)
	products = res.json()
	return products

def get_pests():
	res = requests.get('https://api.ona.io/api/v1/data/401801',auth=auth)
	pests = res.json()
	return pests


