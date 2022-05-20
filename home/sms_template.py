from bugalter.functions import sendSmsOneContact


def payment_clint_sms(request, client_name, summa, currency, kassa=None, bank=None):  #bank or kassa
    user = f'{request.user.first_name} - {request.user.last_name}'
    if currency == 'usd':
        currency = '$'
    elif currency == 'uzs':
        currency = "so'm"

    if kassa:
        message = f"{client_name} mijozdan {summa} {currency} kirim {user} tomonidan {kassa} kassaga to'lov qabul qilindi"

    elif bank:
        message = f"{client_name} mijozdan {summa} {currency} kirim {user} tomonidan {bank.name} {bank.shot_numbers} bank hisob raqamidan to'lov qabul qilindi!"

    sendSmsOneContact(+998901300444, message)


def outincomepayment_sms(request, summa, turi, kassa):
    #faqat kassa
    user = f'{request.user.first_name} - {request.user.last_name}'
    if turi == '1':
        currency = '$'
    elif turi == '2':
        currency = "so'm"
    message = f"Tashqi kirimda {summa} {currency} kirim {user} tomonidan {kassa} kassaga to'lov qabul qilindi!"
    sendSmsOneContact(+998901300444, message)


def chiqim_payment_sms(request, summa,currency, kassa):
    # faqat kassa
    user = f'{request.user.first_name} - {request.user.last_name}'
    if currency == 'usd':
        currency = '$'
    elif currency == 'uzs':
        currency = "so'm"
    message = f"Tashqi chiqimda : {summa} chiqim {user} tomonidan {kassa} kassadan qilindi!"
    sendSmsOneContact(+998901300444, message)


def paymentoutlay_sms(request, summa, currency, kassa=None, bank=None):
    # bank or kassa
    user = f'{request.user.first_name} - {request.user.last_name}'
    if currency == 'usd':
        currency = '$'
    elif currency == 'uzs':
        currency = "so'm"

    if kassa:
        message = f"AktOutlay uchun {summa} chiqim summasi {user} tomonidan {kassa} kassadan chiqim qilindi!"

    elif bank:
        message = f"AktOutlay uchun {summa} chiqim summasi {user} tomonidan {bank.shot_numbers} bank hisob raqamidan to'lov  qilindi!"
    sendSmsOneContact(+998901300444, message)


def paymentforwheat_sms(request, client_name, summa, currency, kassa=None, bank=None):
    # bank or kassa
    user = f'{request.user.first_name} - {request.user.last_name}'
    if currency == 'usd':
        currency = '$'
    elif currency == 'uzs':
        currency = "so'm"
    if kassa:
        messge = f"{client_name} Taminotchiga {summa} {currency} chiqim {user} tomonidan {kassa} kassadan chiqim qilindi!"
    elif bank:
        messge = f"{client_name} Taminotchiga {summa} {currency} chiqim {user} tomonidan {bank.bank_name} {bank.shot_numbers} bank hisob raqamidan to'lov chiqim qilindi!"

    sendSmsOneContact(+998901300444, messge)


def paymentforun_sms(request, summa, currency, client, kassa=None, bank=None):
    # bank or kassa
    user = f'{request.user.first_name} - {request.user.last_name}'
    if currency == 'usd':
        currency = '$'
    elif currency == 'uzs':
        currency = "so'm"

    if kassa:
        message = f"{client.name} Ta'minotchiga {summa} {currency} chiqim {user} tomonidan {kassa} kassadan chiqim qilindi!"
    elif bank:
        message = f"{client.name} Ta'minotchiga {summa} {currency} chiqim {user} tomonidan {bank.bank_name} {bank.shot_numbers} bank hisob raqamidan chiqim qilindi!"


def paymentforqop_sms(request, summa, currency, client, bank):
    #faqat bank
    user = f'{request.user.first_name} - {request.user.last_name}'
    if currency == 'usd':
        currency = '$'
    elif currency == 'uzs':
        currency = "so'm"

    message = f"{client.name} Taminotchiga: {summa} so'm chiqim {user} tomonidan {bank.bank_name} {bank.shot_numbers} bank hisob raqamidan chiqim qilindi!"
    sendSmsOneContact(+998901300444, message)