from mainapp.models import *


def find_fields(phone):
    farmer = Farmer.objects.filter(data__contains={'details/phoneNr': phone}).last()
    fields = Field.objects.filter(data__CMID=farmer.data['CMID']).order_by('-id')
    message = "Choicez les Champs:\n"
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
        return "Choisez :\n1. Les Champs \n2. Payement\n\n0. sortie"
    elif int(message) == 0:
        chat.delete()
        return "session terminée"
    elif chat.page == 1:
        if message == '1':
            chat.page = 2
            chat.save()
            return find_fields(phone)
        elif message == '2':
            chat.page = 3
            chat.save()
            return "Entrez le montant que vous voulez"
        else:
            chat.delete()
            return "Choisez :\n1. Les Champs \n2. Payement\n\n0. sortie"
    elif chat.page == 2:
        try:
            n = int(message) -1
            field = get_fields(phone)[n]
            chat.page = 4
            chat.field = n
            chat.save()
            return "choisir une action pour {}\n1. le champ est prêt\n2. le champ est récolté\n\n0. sortie".format(field.data['fieldName'])
        except:
            return "Entrez le champ correct! \n"+find_fields(phone)
    elif chat.page == 3:
        try:
            amount = int(message)
            farmer = Farmer.objects.filter(data__contains={'details/phoneNr': phone}).last()
            p = Payment.objects.create(farmer=farmer,amount=amount)
            chat.delete()
            return "demande de paiement pour {} reçu, merci".format(amount)
        except:
            return "Entrez le montant correct\n\n0. sortie"
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
                return "choisir le bon statut\n\n0. sortie"
            field.save()
            chat.delete()
            return "statut du champ mis à jour pour {}".format(field.data['fieldName'])
        except:
            return "choisir le bon statut\n\n0. sortie"
