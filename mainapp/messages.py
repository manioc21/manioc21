from mainapp.models import *


def find_fields(phone):
    phone = phone.replace('+','')
    farmer = Farmer.objects.filter(data__contains=[{'details/phoneNr',phone}]).last()
    fields = Field.objects.filter(data__CMID=farmer.data['CMID'])
    message = "Choose action:\n"
    for index,field in enumerate(fields):
    	message += "\n{index}. {name} is ready".format(index,field.data['fieldName'])
    length = len(fields)
    for field in fields:
    	message += "\n{index}. {name} is harvested".format(length,field.data['fieldName'])
    	length += 1
    return message


def handle_sms(request,message,phone):
    message = message.strip()
    if not request.session.get('page'):
        request.session['page'] = 1
        return "Choose :\n 1. Fields \n2. Payments"
    elif request.session.get('page') == 1:
        if int(message) == 1:
        	request.session['page'] == 2
        	return find_fields(phone)
        elif int(message) == 2:
        	request.session['page'] = 3
        	return "Enter amount you want"
        else:
        	return "Choose :\n 1. Fields \n2. Payments"
    elif request.message.get('page') == 3:
    	if message != '':
    		return "payment request recieved"



