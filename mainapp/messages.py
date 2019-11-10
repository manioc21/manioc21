from mainapp.models import *


def find_fields(phone):
    farmer = Farmer.objects.filter(data__contains={'details/phoneNr': phone}).last()
    fields = Field.objects.filter(data__CMID=farmer.data['CMID']).order_by('-id')
    message = "Choose field:\n"
    for i,field in enumerate(fields):
        message += "\n{}. {}".format(i+1,field.data['fieldName'])
    return message


def get_fields(phone):
    farmer = Farmer.objects.filter(data__contains={'details/phoneNr': phone}).last()
    fields = Field.objects.filter(data__CMID=farmer.data['CMID']).order_by('-id')
    return fields


def handle_sms( message, phone):
    phone = phone.replace('+', '')
    message = message.strip()
    chat = Chat.objects.filter(phone=phone).last()
    if not chat:
        chat = Chat.objects.create(phone=phone, page=1)
        return "Choose :\n1. Fields \n2. Payments\n\n0. exit"
    elif int(message) == 0:
        chat.delete()
        return "session ended"
    elif chat.page == 1:
        if message == '1':
            chat.page = 2
            chat.save()
            return find_fields(phone)
        elif message == '2':
            chat.page = 3
            chat.save()
            return "Enter amount you want"
        else:
            chat.delete()
            return "Choose :\n1. Fields \n2. Payments\n\n0. exit"
    elif chat.page == 2:
        try:
            n = int(message) -1
            field = get_fields(phone)[n]
            chat.page = 4
            chat.field = n
            chat.save()
            return "choose action for {}\n1. field is ready\n2. field is harvested\n\n0. exit".format(field.data['fieldName'])
        except:
            return "Enter correct field! \n"+find_fields(phone)
    elif chat.page == 3:
        try:
            amount = int(message)
            farmer = Farmer.objects.filter(data__contains={'details/phoneNr': phone}).last()
            p = Payment.objects.create(farmer=farmer,amount=amount)
            chat.delete()
            return "payment request for {} recieved, Thank you".format(amount)
        except:
            return "Enter correct amount"
    elif chat.page == 4:
        field_num = chat.field
        try:
            n = int(message)
            field = get_fields(phone)[field_num]
            if n == 1:
                field.status = 'ready'
            elif n == 2:
                field.status = 'harvest'
            else:
                return "choose correct status"
            field.save()
            chat.delete()
            return "field status updated for {}".format(field.data['fieldName'])
        except:
            return "choose correct status"
