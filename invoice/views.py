from django.shortcuts import render
from django.http import HttpResponse
from zeep import Client
# Create your views here.


import invoice.secret as sec


terminal_id = sec.p_terminalID
user_name = sec.p_userName
user_password = sec.p_userPassword
operational_url = sec.p_operational_url
bank_url = sec.p_bank_url

def home(request):

    return HttpResponse('home')
    #return HttpResponseRedirect(reverse('sfmc:'))

def callback(request):
    res_code = request.POST.get('ResCode', None)
    sale_reference_id = request.POST.get('SaleReferenceId', None)
    sale_order_id = request.POST.get('SaleOrderId', None)
    ref_id = request.POST.get('RefId', None)

    status = False
    message = ''
    if ref_Id:
        invoice = Invoice.objects.filter(ref_id=ref_id)
        if not invoice.exist():
            return home(request)
        invoice = Invoice.first()
        if invoice.success:
            return home(request)

        Invoice.res_code = int(res_code)
        invoice.sale_order_id = sale_orderId
        invoice.sale_reference_id = sale_reference_id


        if ResCode:
            status, message = res_code_status(int(res_code))
            if status:
                client = Client(operational_url)
                result = client.service.bpVerifyRequest(terminal_id, user_name, user_password,
                                                        int(order_id), int(sale_order_id), int(sale_reference_id))
                try:
                    ResCode = int(result)
                    status, message = res_code_status(int(ResCode))
                except:
                    pass

                if status:
                    invoice.success = True

                else:
                    return HttpResponse("are you the bad guy?")

            else:
                invoice.error_code = int(ResCode)
                invoice.error_description = message
        invoice.save()

    return home(request)


def start_transaction(request, team, amounts):
    local_date = datetime.now().strftime("%Y%m%d")
    local_time = datetime.now().strftime("%H%M%S")
    client = Client(operational_url)
    callback_url = furl(request.build_absolute_uri(reverse("invoice:callback")))

    invoice = Invoice.objects.create(team=team, amount=amount)
    order_id = invoice.pk

    result = client.service.bpPayRequest(terminal_id, user_name, user_password, order_id,amount,
                                         str(local_date), str(local_time), '', callback_url, 0)
    res_code = int(result.split(',')[0].strip())
    status, message = res_code_status(res_code)
    ref_id = 0
    if status:
        ref_id = result.split(',')[1].strip()
    else:
        return HttpResponse('bank connection error')
    invoice.ref_id= ref_id
    invoice.save()
    #do sth
    template = "invoice/to_payment_page.html"
    return render(request, template, {'error_message' : error_description, 'RefID': ref_id, 'BankURL': bank_url})



def res_code_status(res_code):
    if res_code == 0:
        return True, 'تراکنش با موفقیت انجام شد.'
    elif res_code == 11:
        return False, 'شماره کارت نامعتبر است.'
    elif res_code == 12:
        return False, 'موجودی کافی نیست.'
    elif res_code == 13:
        return False, 'رمز نادرست است.'
    elif res_code == 14:
        return False, 'تعداد دفعات وارد کردن رمز بیش از حد مجاز است.'
    elif res_code == 15:
        return False, 'کارت نامعتبر است.'
    elif res_code == 16:
        return False, 'دفعات برداشت وجه بیش از حد مجاز است.'
    elif res_code == 17:
        return False, 'کاربر از انجام تراکنش منصرف شده است.'
    elif res_code == 18:
        return False, 'تاریخ انقضای کارت گذشته است.'
    elif res_code == 19:
        return False, 'مبلغ برداشت وجه بیش از حد مجاز است.'
    elif res_code == 111:
        return False, 'صادر کننده کارت نامعتبر است.'
    elif res_code == 112:
        return False, 'خطای سوییچ صادر کننده کارت'
    elif res_code == 113:
        return False, 'پاسخصی از صادر کننده کارت دریافت نشد.'
    elif res_code == 114:
        return False, 'دارنده کارت مجاز به انجام تراکنش نیست.'
    elif res_code == 21:
        return False, 'پذیرنده نامعتبر است.'
    elif res_code == 23:
        return False, 'خطای امنیتی رخ داده است.'
    elif res_code == 24:
        return False, 'اطلاعات کاربری پذیرنده نامعتبر است.'
    elif res_code == 25:
        return False, 'مبلغ نامعتبر است.'
    elif res_code == 31:
        return False, 'پاسخ نامعتبر است.'
    elif res_code == 32:
        return False, 'فرمت اطلاعات وارد شده صحیح نمی‌باشد.'
    elif res_code == 33:
        return False, 'حساب نامعتبر است.'
    elif res_code == 34:
        return False, 'خطای سیستمی'
    elif res_code == 35:
        return False, 'تاریخ نامعتبر است.'
    elif res_code == 41:
        return False, 'شماره درخواست تکراری است.'
    elif res_code == 42:
        return False, 'تراکنش sale یافت نشد.'
    elif res_code == 43:
        return True, 'قبلا درخواست verify داده شده است.'
    elif res_code == 44:
        return False, 'درخواست verify یافت نشد.'
    elif res_code == 45:
        return False, 'تراکنش settle شده است.'
    elif res_code == 46:
        return False, 'تراکنش settle نشده است.'
    elif res_code == 47:
        return False, 'تراکنش settle یافت نشد.'
    elif res_code == 48:
        return False, 'تراکنش reverse شده است.'
    elif res_code == 49:
        return False, 'تراکنش refund یافت نشد.'
    elif res_code == 412:
        return False, 'شناسه قبض نادرست است.'
    elif res_code == 413:
        return False, 'شناسه پرداخت نادرست است.'
    elif res_code == 414:
        return False, 'سازمان صادر کننده قبض نامعتبر است.'
    elif res_code == 415:
        return False, 'زمان جلسه کاری به پایان رسیده است.'
    elif res_code == 416:
        return False, 'خطا در ثبت اطلاعات'
    elif res_code == 417:
        return False, 'شناسه پرداخت کننده نامعتبر است.'
    elif res_code == 418:
        return False, 'اشکال در تعریف اطلاعات مشتری'
    elif res_code == 419:
        return False, 'تعداد دفعات ورود به اطلاعات از حد مجاز گذشته است.'
    elif res_code == 421:
        return False, 'ip نامعتبر است.'
    elif res_code == 51:
        return False, 'تراکنش تکراری است.'
    elif res_code == 54:
        return False, 'تراکنش مرجع موجود نیست.'
    elif res_code == 55:
        return False, 'تراکنش نامعتبر است.'
    elif res_code == 61:
        return False, 'خطا در واریز'
