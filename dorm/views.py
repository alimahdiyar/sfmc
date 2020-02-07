from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from zeep import Client
from datetime import datetime

import invoice.secret as sec
from dorm.models import DormUser, DormPayment
from furl import furl
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

terminal_id = sec.p_terminalID
user_name = sec.p_userName
user_password = sec.p_userPassword
operational_url = sec.p_operational_url
bank_url = sec.p_bank_url
payment_code = sec.p_payment_code

def home(request):
    return HttpResponseRedirect(reverse('login'))

def to_pay_amount(user):
    payed_amount = 0
    dorm_price = 0

    for dorm_user in DormUser.objects.filter(user=user):
        if dorm_user.day1:
            dorm_price += 30 * 10**3 * 10
        if dorm_user.day2:
            dorm_price += 30 * 10**3 * 10
    for dorm_payment in DormPayment.objects.filter(user=user):
        if dorm_payment.success:
            payed_amount += dorm_payment.amount

    return dorm_price - payed_amount
def dorm_users(request):
    if not request.user.is_authenticated:
        home(request)

    template = "dorm_users.html"

    if request.method != "POST":
        return render(request, template, {'dorm_users':DormUser.objects.filter(user=request.user), 'to_pay_amount':to_pay_amount(request.user)})

    for active_member in request.POST['active_members'].split(','):
        dorm_user = DormUser.objects.create(
            user=request.user,
            name=request.POST[f'member_{active_member}_name'].strip(),
            sex=int(request.POST[f'member_{active_member}_sex'].strip()),
            student_card_image=request.FILES[f'member_{active_member}_student_card_image'],
            national_card_image=request.FILES[f'member_{active_member}_national_card_image']
        )
        if f'member_{active_member}_day1' in request.POST:
            if request.POST[f'member_{active_member}_day1']:
                dorm_user.day1=True
        if f'member_{active_member}_day2' in request.POST:
            if request.POST[f'member_{active_member}_day2']:
                dorm_user.day2=True

        dorm_user.save()

    return HttpResponseRedirect(reverse("dorm:dorm_users"))

def pay_bill(request):
    if not request.user.is_authenticated:
        home(request)

    amount = to_pay_amount(request.user)

    if amount > 0:
        return start_transaction(request, amount)
    else:
        return HttpResponse("what to pay???")


@csrf_exempt
def callback(request):
    res_code = request.POST.get('ResCode', None)
    sale_reference_id = request.POST.get('SaleReferenceId', None)
    sale_order_id = request.POST.get('SaleOrderId', None)
    ref_id = request.POST.get('RefId', None)

    status = False
    message = ''
    if ref_id:
        dorm_payment = DormPayment.objects.filter(ref_id=ref_id)
        if not dorm_payment.exists():
            return home(request)
        dorm_payment = dorm_payment.first()
        if dorm_payment.success:
            return home(request)

        order_id = dorm_payment.pk

        dorm_payment.res_code = int(res_code)
        dorm_payment.sale_order_id = sale_order_id
        dorm_payment.sale_reference_id = sale_reference_id


        if res_code:
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
                    dorm_payment.success = True

                else:
                    try:
                        return HttpResponse("are you the bad guy: " + str(status) + '\n' + str(message))
                    except:
                        return HttpResponse("are you the bad guy: " + str(ResCode))
            else:
                dorm_payment.error_code = int(res_code)
                dorm_payment.error_description = message
        dorm_payment.save()

    return home(request)


def start_transaction(request, amount):

    local_date = datetime.now().strftime("%Y%m%d")
    local_time = datetime.now().strftime("%H%M%S")
    client = Client(operational_url)
    callback_url = furl(request.build_absolute_uri(reverse("dorm:callback")))

    dorm_payment = DormPayment.objects.create(user=request.user, amount=amount)
    order_id = dorm_payment.pk + 13000

    result = client.service.bpPayRequest(terminal_id, user_name, user_password, order_id,amount,
                                         str(local_date), str(local_time), '', callback_url, payment_code)
    res_code = int(result.split(',')[0].strip())
    status, error_message = res_code_status(res_code)
    ref_id = 0
    if status:
        ref_id = result.split(',')[1].strip()
    else:
        return HttpResponse('bank connection error: ' + status + '\n' + error_message)
    dorm_payment.ref_id= ref_id
    dorm_payment.save()
    #do sth
    template = "to_payment_page.html"
    return render(request, template, {'res_code' : res_code, 'error_message' : error_message, 'RefID': ref_id, 'BankURL': bank_url})



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
