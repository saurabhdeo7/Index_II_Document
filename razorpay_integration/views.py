from django.shortcuts import render
from .models import Order
from django.views.decorators.csrf import csrf_exempt
import razorpay
from FindIndexIIWebsite.settings import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
)
from .constants import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
import json
from indexIIdocument.models import STATES, IndexIIdoc

# Create your views here.

a = ""
def home1(request):
    file = request.POST.get("fileLink")
    global a 
    a = str(file)
    return render(request, "index.html")


def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = 200
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100,
              "currency": "INR",
                "payment_capture": "1"}
        )
        response = client.customer.all(email)
        id = "No"
        for i in response["items"]:
            if i["email"] == email:
                id = i["id"]
                print(id)
        if(id == "No"):
            response = client.customer.create({
                "name": name,
                "contact": contact,
                "email": email,
                "fail_existing": 0,
                "notes": {
                    "notes_key_1": "Tea, Earl Grey, Hot",
                    "notes_key_2": "Tea, Earl Grey… decaf."
                }
            })
            id = response['id']

        custId = id
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/callback/",
                "razorpay_key": RAZORPAY_KEY_ID,
                "order": order,
                "custId":custId,
                "email":email,
                "contact":contact,
            },
        )
    return render(request, "payment.html")


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if  verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            print(order.status)
            order.save()
            return render(request, "callback.html", context={"status": order.status,"file": a})
        else:
            order.status = PaymentStatus.FAILURE
            print(order.status)
            order.save()
            return render(request, "callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        print(order.status)
        order.save()
        return render(request, "callback.html", context={"status": order.status})
