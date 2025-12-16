from django.shortcuts import render,HttpResponseRedirect,reverse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from . models import *
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
import datetime  



def Home(request):
    prod = Products.objects.order_by('-id')[:3]
    return render(request,'home.html',{"spice":prod})


def payment(request):
    # print(request.POST['pk'])
    return render(request,'payment.html')


def addpayment(request):
    if request.method == "POST":
        buyer = Profile.objects.filter(user=request.user).first()
        amount = float(request.POST['amount'])  
        bought_from = request.POST['bought_from']
        bid = Bids.objects.filter(pk=request.POST['pk']).first()

        
        if buyer.balance < amount:
            messages.error(request, "Insufficient balance!")
            return HttpResponseRedirect(reverse('payment'))  

        bid.paid = True
        bid.save()
        buyer.balance -= amount
        buyer.save()

        user = User.objects.filter(username=bought_from).first()
        seller = Profile.objects.filter(user=user).first()
        seller.balance += amount
        seller.save()

        messages.success(request, "Payment successful!")  
        return HttpResponseRedirect(reverse('payment'))
    return render(request, 'dashboard.html')

def adminpage(request):
    spice=Products.objects.filter(is_approved=False).order_by('-id')
    return render(request,'admin.html',{"pending":spice})

def singleproduct_view(request,pk):
    spice=Products.objects.filter(id=pk).first()
    print(spice)
    return render(request,'singleproduct_view.html',{"product":spice})

def dashboard(request):
    pro = Profile.objects.filter(user=request.user).first()
    spices = Products.objects.filter(user=request.user).order_by('-id')
    product = Products.objects.filter(Q(user=request.user) & Q(is_ended=True))
    bids_user = Bids.objects.filter(user=request.user).order_by('-bid_price')
    details = []
    details2 = []
    
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d at %I:%M %p")
    for p in product:
        try:
            sold = Bids.objects.filter(product=p).order_by('-bid_price').first()
            if sold:
                ph = Profile.objects.filter(user=sold.user).first()
                details.append({
                    'name': sold.product.product_name,
                    'price': sold.bid_price,
                    'phone': ph.phoneNumber,
                    'date': "Jan 30, 2025",
                    'sold_to': sold.user.username,
                    'pk':sold.pk,
                    'paid':sold.paid
                })
                print(details)
                if not Notification.objects.filter(user=p.user, title=f"{sold.product.product_name} Sold!").exists():
                    Notification.objects.create(
                        user=p.user,
                        title=f"{sold.product.product_name} Sold!",
                        description=f"Your product '{sold.product.product_name}' was sold to {sold.user.username} on {current_datetime}. Thank you for selling with us!"
                    )
        except Exception as e:
            print(f"Error processing sold item: {e}")
    
  
    for b in bids_user:
        prod = Products.objects.filter(Q(is_ended=True) & Q(pk=b.product.pk))
        profile = Profile.objects.filter(user= request.user).first()
        for p in prod:
            try:
                sold = Bids.objects.filter(Q(product=p) & Q(user=request.user) & Q(status="winning")).order_by('-bid_price').first()
                if sold:
                    ph = Profile.objects.filter(user=sold.product.user).first()
                    dict_details = {
                        'name': sold.product.product_name,
                        'price': sold.bid_price,
                        'phone': ph.phoneNumber,
                        'date': "Jan 30, 2025",
                        'bought_from': sold.product.user.username,
                        'pk':sold.pk,
                        'paid':sold.paid
                    }
                    print(dict_details)
                     
                    if dict_details not in details2:
                        details2.append(dict_details)
                        
                        if not Notification.objects.filter(user=sold.user, title=f"{sold.product.product_name} Purchased!").exists():
                            Notification.objects.create(
                                user=sold.user, 
                                title=f"{sold.product.product_name} Purchased!",
                                description=f"Congratulations! 🎉 You bought {sold.product.product_name} from {sold.product.user.username} on {current_datetime}. Thank you for buying with us!"
                            )
            except Exception as e:
                print(f"Error processing bought item: {e}")
    
    bids = Bids.objects.filter(user=request.user).order_by('-id')
    return render(request, 'Dashboard.html', {'profile': pro,'listed': spices,'bids': bids,'bidsSold': details,'bidsBought': details2})

def updateprofile(request):
    if request.method == "POST":
       firstname = request.POST['firstname'] 
       print(firstname)
       lastname = request.POST['lastname'] 
       print(lastname)
       email = request.POST['email'] 
       print(email)
       phonenumber = request.POST['phone'] 
       print(phonenumber)
       address = request.POST['address']
       print(address)
       user=User.objects.filter(username=request.user).first()
       user.first_name=firstname
       user.last_name=lastname
       user.email=email
       user.save()
       pro=Profile.objects.filter(user=request.user).first()
       pro.address=address
       pro.phoneNumber=phonenumber
       pro.save()
    return redirect('dashboard')

def adminapproved(request):
    cards=Products.objects.filter(is_approved=True)
    return render(request,'adminapproved.html',{'spice':cards})

def listproduct(request):

    return render(request,'list-product.html')

def auction(request):
    cards=Products.objects.filter(is_approved=True)
    
    return render(request,'auction.html',{'spice':cards})

# @csrf_exempt
def register(request):
    user = None
    error_message = None
    print('not wrking')
    if request.method == "POST":
        # print(111111111111111111111111111111111111111111111111111111111111111111111,'wrking')
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        email = request.POST['email']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        phoneNumber = request.POST['phoneNumber']
        profilePic = request.FILES['profilePic']
        address = request.POST['address']
        # print(username)
        # try:
        user = User.objects.create_user(username=username,email=email,first_name=firstName,last_name=lastName)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user,phoneNumber=phoneNumber,profilePic=profilePic,address=address)
        Profile.objects.create(user=user)
        return redirect('login')
        # except Exception as e:
            # print("error")
            # return JsonResponse({"status":"error","message":"invalid email or password"})
    return render(request,'register.html',{'user': user, 'error_Message': error_message}) 



def loginview(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            error_message = "Both username and password are required."
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  
            else:
                error_message = "Invalid username or password."
    return render(request, "login.html", {"error_message": error_message})

def user_logout(request):
    logout(request)
    return redirect("home") 

def addproducts(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        category = request.POST.get("category")
        quality = request.POST.get("quality")
        starting_price = request.POST.get("starting_price")
        reserve_price = request.POST.get("reserve_price")
        quantity = request.POST.get("quantity")
        auction_duration = request.POST.get("auction_duration")
        listing_time = request.POST.get("listing_time")
        print(listing_time)
        certified = request.POST.get("certified")
        description = request.POST.get("description")
        origin = request.POST.get("origin")
        product_image = request.FILES['product_image']
        spice_video = request.FILES['video']
        account_number = request.POST.get("account_number")
        ifsc = request.POST.get("ifsc")

        product = Products.objects.create(
            user=request.user,
            product_name=product_name,
            category=category,
            quality=quality,
            starting_price=starting_price,
            reserve_price=reserve_price,
            quantity=quantity,
            auction_duration=auction_duration,
            created=listing_time,
            certified=certified,
            description=description,
            origin=origin,
            product_image=product_image,
            spice_video=spice_video,
            account_number=account_number,
            ifsc=ifsc,
            bid_price=starting_price
        )
        product.save()
        return redirect("listproduct") 
    return render(request, "list-product.html")

def conformbid(request,pk):
    if request.method == "POST":
        bidamount = float(request.POST.get("bidamount"))
        # print(bidamount)
        spice=Products.objects.filter(id=pk).first()
        Bids.objects.create(user = request.user,ends_in = spice.auction_duration,status = "pending",product = spice,bid_price =bidamount )
        if bidamount > spice.bid_price:
            spice.bid_price=bidamount
            spice.bid=spice.bid+1
            spice.save()
            #    //////////// bid winning loosing
            bids = Bids.objects.filter(product = spice).order_by('-bid_price')
            for index , bid in enumerate(bids):
                bid.status = "winning" if index == 0 else "losing"
                bid.save()

                if bid.status =="winning" and bid.product.is_ended:
                    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d at %I:%M %p")
                    Notification.objects.create(
                    user=bid.user,
                    title=bid.product.product_name+" Purchased",
                    descripton=f"Purchased! 🎉 You bought {bid.product.product_name} from {bid.product.user.username} on {current_datetime}. Enjoy your spices!"  
                    )
    return HttpResponseRedirect(reverse('auction'))

# def conformbid2(request):
#     if request.method == "POST":
#         bidamount = float(request.POST.get("bidamount"))
#         print(bidamount)
#         spice=Products.objects.filter(id=pk).first()
#         Bids.objects.create(user = request.user,ends_in = spice.auction_duration,status = "pending",product = spice,bid_price =bidamount )
#         if bidamount > spice.bid_price:
#            spice.bid_price=bidamount
#            spice.bid=spice.bid+1
#            spice.save()
#            notifications=Notification.objects.create
#         print(spice.bid)
#     return HttpResponseRedirect(reverse('auction'))

def notification(request):
    try:
        noti=Notification.objects.filter(user=request.user).order_by('-id')
    except:
        noti = ''
    return render(request, "notification.html",{'noti':noti})

def product_approve(request,pk):
        spice=Products.objects.filter(id=pk).first()
        spice.is_approved=True
        spice.save()
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d at %I:%M %p")
        print(current_datetime)
        print(spice.user)
        Notification.objects.create(
          user=spice.user,
          title=spice.product_name+" Approved",
          description=f"Your spice bid has been approved by the admin on {current_datetime}. Your listed product is now active and available for buyers.Thank you for being a valued seller!"  
        )
        return redirect('adminpage')

def cancellproduct(request,pk):
    studcon=Products.objects.filter(id=pk).first()
    studcon.is_approved=False
    studcon.save()
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d at %I:%M %p")
    Notification.objects.create(
          user=studcon.user,
          title=studcon.product_name+" Cancelled",
          description=f"Your spice bid has been canceled by the admin on {current_datetime}. Your listed product is no longer active and unavailable for buyers.Thank you for being a valued seller!"  
        )   
    return redirect('adminapproved')

@csrf_exempt
def update_auction_status(request, product_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product = Products.objects.get(id=product_id)
            product.status = "ended"
            product.is_ended = True  # Mark auction as ended
            product.save()
            return JsonResponse({"message": "Auction status updated successfully."})
        except Products.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)


def pricePrediction(request):
    return render(request,'pricePrediction.html')


import requests
def product_price_prediction(request):
    if request.method == 'POST':
        
        data = {
            'product_name': request.POST.get('product_name'),
            'category': request.POST.get('category'),
            'quality': request.POST.get('quality'),
            'starting_price': request.POST.get('starting_price'),
            'reserve_price': request.POST.get('reserve_price'),
            'quantity': request.POST.get('quantity'),
            'origin': request.POST.get('origin')
        }
        
       
        response = requests.post('https://craftapp.pythonanywhere.com/recommendation/', data=data)
        print(type(response.text))
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            result = {"error": "Invalid response format"}
        print()
        return render(request, 'productPricePrediction.html', {"result": result['result']})
