from django.template.defaulttags import register
from mainapp.models import Farmer,Field

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def edit_role(value):
    return '☑ '+value.replace(' '," ☑ ")

@register.filter
def get_name_from_enid(farmer):
	user = Farmer.objects.filter(data__CMID=farmer['ENID'])
	if not user.exists():
		return "admin"
	user = user.last()
	return user.data['details/firstName'] + " " +  user.data['details/surName']

@register.filter
def get_name_from_cmid(farmer):
	user = Farmer.objects.filter(data__CMID=farmer['CMID'])
	if not user.exists():
		return "admin"
	user = user.last()
	return user.data['details/firstName'] + " " +  user.data['details/surName']


@register.filter
def get_id_from_cmid(farmer):
	user = Farmer.objects.filter(data__CMID=farmer['CMID'])
	if not user.exists():
		return 0
	user = user.last()
	return user.data['_id']



@register.filter
def get_id_from_enid(farmer):
	user = Farmer.objects.filter(data__CMID=farmer['ENID'])
	if not user.exists():
		return 0
	user = user.last()
	return user.data['_id']


@register.filter
def get_pest_field(pest):
	field = pest.split('-')
	return field[0]

@register.filter
def get_pest_field_id(pest):
	f = Field.objects.filter(data__fieldID=pest['fieldID'])
	if f.exists():
		return f.last().data['_id']
	return 0

@register.filter
def get_field_registrar(field):
	farmer = Farmer.objects.filter(data__username=field.data['username']).last()
	if farmer:
		user = Farmer.objects.filter(data__CMID=farmer.data['ENID'])
		if user.exists():
			user = user.last()
			return user.data['details/firstName'] + " " +  user.data['details/surName']
	return "admin"

@register.filter
def get_field_registrar_id(field):
	farmer = Farmer.objects.filter(data__username=field.data['username']).last()
	if farmer:
		user = Farmer.objects.filter(data__CMID=farmer.data['ENID'])
		if user.exists():
			user = user.last()
			return user.data['_id']
	return 0

@register.filter
def get_pest_registrar(field):
	farmer = Farmer.objects.filter(data__username=field['username']).last()
	if farmer:
		user = Farmer.objects.filter(data__CMID=farmer.data['ENID'])
		if user.exists():
			user = user.last()
			return user.data['details/firstName'] + " " +  user.data['details/surName']
	return "admin"

@register.filter
def get_pest_registrar_id(field):
	farmer = Farmer.objects.filter(data__username=field['username']).last()
	if farmer:
		user = Farmer.objects.filter(data__CMID=farmer.data['ENID'])
		if user.exists():
			user = user.last()
			return user.data['_id']
	return 0

@register.filter
def get_field_owner(field):
	user = Farmer.objects.filter(data__CMID=field.data['CMID'])
	if not user.exists():
		return "admin"
	user = user.last()
	return user.data['details/firstName'] + " " +  user.data['details/surName']

@register.filter
def get_field_owner_id(field):
	user = Farmer.objects.filter(data__CMID=field.data['CMID'])
	if not user.exists():
		return "44444"
	user = user.last()
	return user.data['_id']

@register.filter
def roundoff(value):
	return round(float(value),2)

@register.filter
def roundoff_location(value):
	return [str(round(float(value[0]),6))+'°',str(round(float(value[1]),6))+'°']

@register.filter
def calculate_yield(value):
	return round(value*26,2)

@register.filter
def calculate_weight(product):
	return product['productDetails/quantity'] * product['productDetails/weight']

@register.filter
def get_landowner(number):
	if number:
		value = int(float(number)*100)
		return str(value) + "%"
	return ""

@register.filter
def get_lat(data):
	return data[0]

@register.filter
def get_lng(data):
	return data[1]

@register.filter
def get_suppliers(supply):
	details = []
	for s in supply['supplyDetails']:
		cmid = s.get('supplyDetails/CMID')
		if cmid:
			user = Farmer.objects.filter(data__CMID=cmid).last()
			data = {'phone':s.get('supplyDetails/CMID_confirm_details/CMID_confirm_phoneNr')}
			if user:
				data.update({'name':user.data['details/firstName'],'surname':user.data['details/surName']})
			details.append(data)
		else:
			details.append({'name':s.get('supplyDetails/details/firstName'),'surname':s.get('supplyDetails/details/surName'),'phone':s.get('supplyDetails/details/phoneNr')})
	return details
