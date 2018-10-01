from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import Item, User, Vendor, Order
from .forms import ItemForm, UserForm, VendorForm, OrderForm

import csv


# Work in Progress
def index(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    return render(request, 'home/login.html', context={'password_fail':False, 'username_fail':False})
    return render(request, 'home/index.html')


def cancel_order(request, id):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')
    order = get_object_or_404(Order, id=id)

    subject = "Order Cancellation"
    to_email = [order.cust_email]
    from_email = settings.EMAIL_HOST_USER

    body = "Hello %s!\n\nYour order for %s is cancelled." %(order.cust_name, order.item)
    body += "\n\nPlease check your order details and place a new order."
    body += "\n\nContact us as %s for support." %(settings.EMAIL_HOST_USER)

    send_mail(
        subject,
        body,
        from_email,
        to_email,
        fail_silently=False,
    )

    order.confirmation = "Cancelled"
    order.save()

    return render(request, 'home/processOrder.html', context={'info_needed':False, 'order_placed':False, 'order_cancelled':True, 'order':order})


def confirm_order(request, id):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')
    order = get_object_or_404(Order, id=id)

    subject = "Order Confirmation"
    to_email = [order.cust_email]
    from_email = settings.EMAIL_HOST_USER

    body = "Hello %s!\n\nYour order for %s is confirmed for the %d prices. The amount for your order is $%s." %(order.cust_name, order.item, order.quantity, order.amount)
    body += "\n\n You can view your order details at http://localhost/order/%s" %(order.id)

    send_mail(
        subject,
        body,
        from_email,
        to_email,
        fail_silently=False,
    )

    order.confirmation = "Confirmed"
    order.save()

    return render(request, 'home/processOrder.html', context={'info_needed': False, 'order_cancelled':False, 'order_placed':True, 'order':order})


def process_order(request, id):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')
    order = get_object_or_404(Order, id=id)

    item_in_db = True
    quantity_available = False
    price_correct = False

    item = get_object_or_404(Item, sku=order.item)

    if item.quantity >= order.quantity:
        quantity_available = True

    if order.amount == (item.price * order.quantity):
        price_correct = True

    return render(request, 'home/processOrder.html', context={'item_in_db':item_in_db, 'info_needed':True, 'price_correct':price_correct, 'quantity_available':quantity_available, 'order':order})


def send_email(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')
    if request.method == "POST":

        subject = request.POST['subject']
        body = request.POST['body']
        email = request.POST['to-email']

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return render(request, 'home/mailer.html', context={'mail_sent':True})

    else:
        return HttpResponse('Hackers not wanted.')


def mailer(request, email):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')
    return render(request, 'home/mailer.html', context={'email':email, 'mail_sent':False})


def order_detail_view(request, id=""):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    if request.method == "POST":
        record = get_object_or_404(Order, id=request.POST['id'])
        order_form = OrderForm(request.POST, instance=record)

        if order_form.is_valid():
            record.save()

            return render(request, 'home/orderDetails.html', context={'form':order_form, 'update_succesful':True})

    elif request.method == "GET" and id != "":
        record = get_object_or_404(Order, id=id.upper())
        order_form = OrderForm(instance=record)
        return render(request, 'home/orderDetails.html', context={'form':order_form})

    else:
        return HttpResponse('Hacker not wanted.')


def vendor_detail_view(request, ext=""):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    if request.method == "POST":
        record = get_object_or_404(Vendor, extension=request.POST['extension'])
        vendor_form = VendorForm(request.POST, instance=record)

        if vendor_form.is_valid():
            record.save()

            return render(request, 'home/vendorDetails.html', context={'form':vendor_form, 'update_succesful':True})

    elif request.method == "GET" and ext != "":
        record = get_object_or_404(Vendor, extension=ext.upper())
        vendor_form = VendorForm(instance=record)
        return render(request, 'home/vendorDetails.html', context={'form':vendor_form})

    else:
        return HttpResponse('Hacker not wanted.')


def item_detail_view(request, sku=""):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    if request.method == "POST":
        record = get_object_or_404(Item, sku=request.POST['sku'])
        item_form = ItemForm(request.POST, instance=record)

        if item_form.is_valid():
            record.save()

            return render(request, 'home/itemDetails.html', context={'form':item_form, 'update_succesful':True})

    elif request.method == "GET" and sku != "":
        record = get_object_or_404(Item, sku=sku.upper())
        item_form = ItemForm(instance=record)
        return render(request, 'home/itemDetails.html', context={'form':item_form})

    else:
        return HttpResponse('Hacker not wanted.')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            print('FOUND')
            print(username)
            print(password)
            print(user.password)

            if user.password == password:
                print(True)
                request.session['session-active'] = True
                print('SESSION FAIL')
                return redirect('items-list')

            else:
                return render(request, 'home/login.html', context={'password_fail':True})
        except:
            return render(request, 'home/login.html', context={'username_fail':True})

    elif request.method == "GET":

        try:
            if request.session['session-active']:
                request.session['session-active'] = False
        except:
            return render(request, 'home/login.html')

        return render(request, 'home/login.html')


def logout(request):
    request.session['session-active'] = False
    return redirect('index')


def uploads(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    return render(request, 'home/uploads.html')


def items(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    records = list(Item.objects.all())
    no_of_records = len(records)
    return render(request, 'home/items.html', context={'records':records, 'no_of_records':no_of_records})


def orders(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    records = list(Order.objects.all())
    no_of_records = len(records)
    return render(request, 'home/orders.html', context={'records':records, 'no_of_records':no_of_records})


def vendors(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    records = list(Vendor.objects.all())
    no_of_records = len(records)
    return render(request, 'home/vendors.html', context={'records':records, 'no_of_records':no_of_records})


def upload_item(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    if request.method == "POST":
        file = request.FILES['sheetFile']

        content = list()
        headers = list()
        values = list()

        if file.name.split(".")[1] in ["xlsx", "xls"]:
            sheet = pyexcel.load_from_memory(file.name.split(".")[1], file.read())

            for row in sheet:
                for val in range(len(row)):
                    row[val] = str(row[val])
                values += [row]

            headers = values[0]
            values = values[1:]

        elif file.name.split(".")[1] == "csv":
            content = [i.strip() for i in file.read().decode("utf-8").split("\n")]
            headers = content[0].split(",")
            values = [i.split(",") for i in content[1:] if len(i.split(",")) > 1]

        else:
            return HttpResponse("File Format not supported. Please use .csv .xls .xlsx file types.")


        for item in values:
            item_data = Item()

            item_data.sku = item[0]
            item_data.title = item[1]
            item_data.vendor_ext = item[2]
            item_data.quantity = item[3]
            item_data.price = item[4]

            item_data.save()

        return render(request, 'home/uploads.html', context={'upload_successful':True})


def upload_vendor(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    if request.method == "POST":
        file = request.FILES['sheetFile']

        content = list()
        headers = list()
        values = list()

        if file.name.split(".")[1] in ["xlsx", "xls"]:
            sheet = pyexcel.load_from_memory(file.name.split(".")[1], file.read())

            for row in sheet:
                for val in range(len(row)):
                    row[val] = str(row[val])
                values += [row]

            headers = values[0]
            values = values[1:]

        elif file.name.split(".")[1] == "csv":
            content = [i.strip() for i in file.read().decode("utf-8").split("\n")]
            headers = content[0].split(",")
            values = [i.split(",") for i in content[1:] if len(i.split(",")) > 1]

        else:
            return HttpResponse("File Format not supported. Please use .csv .xls .xlsx file types.")


        for vendor in values:
            vendor_data = Vendor()

            vendor_data.name = vendor[0]
            vendor_data.extension = vendor[1]
            vendor_data.phone = vendor[2]
            vendor_data.email = vendor[3]
            vendor_data.website = vendor[4]

            vendor_data.save()

        return render(request, 'home/uploads.html', context={'upload_successful':True})


def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            if password != confirm_password:
                user_form = UserForm()
                return render(request, 'home/register.html', context={'form':user_form, 'password_match_fail':True, 'details_incorrect':False})

            user_form.save()

            return redirect('index')

        else:
            user_form = UserForm()
            return render(request, 'home/register.html', context={'form':user_form, 'password_match_fail':False, 'details_incorrect':True})

    if request.method == 'GET':
        user_form = UserForm()
        return render(request, 'home/register.html', context={'form':user_form})


def download_items(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    items = Item.objects.all()

    if request.method == "POST":
        vendor_ext = request.POST['vendor-extension'].upper()
        items = Item.objects.filter(vendor_ext=vendor_ext)


    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="listed_items.csv"'
    writer = csv.writer(response)

    writer.writerow([
        "ITEM SKU",
        "ITEM TITLE",
        "VENDOR EXTENSION",
        "QUANTITY AVAILABLE",
        "PRICE",
    ])

    for item in items:
        writer.writerow([
            item.sku,
            item.title,
            item.vendor_ext,
            item.quantity,
            item.price,
        ])

    return response


def download_vendors(request):

    try:
        if not request.session['session-active']:
            return redirect('login')
    except:
        return redirect('login')

    if request.method == "POST":
        return redirect('data-upload')

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="listed_vendors.csv"'
    writer = csv.writer(response)

    writer.writerow([
        "VENDOR NAME",
        "VENDOR EXTENSION",
        "PHONE",
        "EMAIL",
        "WEBSITE",
    ])

    for vendor in Vendor.objects.all():
        writer.writerow([
            vendor.name,
            vendor.extension,
            str(vendor.phone),
            vendor.email,
            vendor.website,
        ])

    return response
