from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django import forms
from django.db.models import Max, Min, Sum, Avg
import os

from .models import User, listings, comments, WatchList, bidmodel, closedlistings

all_categories = [('electronics', 'electronics'), ('clothing', 'clothing'), ('utility','utility'), ('mobiles','mobiles')]

class CreateForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'style': 'text-align: left', 'placeholder': 'Name of item', 'id': 'name'}))
    price = forms.DecimalField(label="", max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'Price of item'}))
    picture = forms.URLField(label="",max_length=200,  required= False, widget=forms.URLInput(attrs={'placeholder': 'Url of picture'}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'style': 'text-align: left', 'placeholder': 'Product Description'}))
    categorylist = forms.CharField(label="Categories", widget=forms.Select(choices=all_categories))

class CommentForm(forms.Form): 
    comment = forms.CharField(label="", widget=forms.Textarea(attrs={'style': 'text-align: left', 'placeholder': 'Comment'}))

class BidForm(forms.Form): 
    amount = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Bid'}))

def index(request):
    all_listings = listings.objects.all() 
    return render(request, "auctions/index.html", {
        'all': all_listings
    })

def categories(request): 
    all = ['electronics', 'clothing', 'utility', 'mobiles']
    return render(request, "auctions/categories.html", {
        'all': all
    })

def categorypage(request, title): 
    item = listings.objects.filter(category=title)
    return render(request, "auctions/categorypage.html", {
        'item': item, 
        'title': title
    })
    
    

#add catergory page here. All entries sorted by each category. Make drop down for categories in form



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST": 
        all_listings = listings.objects.all()
        form = CreateForm(request.POST)
        if form.is_valid():
            obj = listings()
            obj.name = form.cleaned_data["name"] 
            obj.price = form.cleaned_data["price"]
            obj.picture = form.cleaned_data["picture"]
            obj.description = form.cleaned_data["description"]
            obj.category = form.cleaned_data["categorylist"]
            obj.seller = request.user.username
            obj.save()
                   
        return render(request, "auctions/index.html", {
        'all': all_listings
        })
    
    else: 
        return render(request, "auctions/create.html", {
            "form": CreateForm()
        })


@login_required
def close(request, id):
    if request.user.username: 
        winningbid = bidmodel.objects.filter(listingid=id).aggregate(Max('price'))
        winner = bidmodel.objects.get(listingid=id, price=winningbid['price__max'])
        obj3 = listings.objects.get(id=id)
        obj4 = closedlistings()
        #newclosedlistings add name, price, description, picture, listingid, seller, buyer
        obj4.name = obj3.name
        obj4.price = winningbid['price__max']
        obj4.description = obj3.description
        obj4.picture = obj3.picture 
        obj4.listingid = id 
        obj4.seller = request.user.username
        print(winner)
        obj4.buyer = winner.name
        obj4.category = obj3.category
        obj4.save()
        obj3.delete()
        return redirect("index")

def closed(request):
    all_listings = closedlistings.objects.all()
    return render(request, "auctions/closed.html", {
        'all': all_listings

    })

def listing(request, id):
    item = listings.objects.filter(id=id)
    highestbid = bidmodel.objects.filter(listingid=id).aggregate(Max('price'))
    listentry = listings.objects.get(id=id)
    numberbids = bidmodel.objects.filter(listingid=id).count()
    all_comm = comments.objects.filter(listingid=id)
    if request.user.username:
        try: 
            if WatchList.objects.get(name=request.user.username, listingid=id):
                added=False
        except:  
            added = True
    else: 
        added=False
    
    if request.user.username == listentry.seller:
        owner = True
    else: 
        owner = False
    
    return render(request, "auctions/listing.html", {
            'item': item,
            'form': CommentForm(), 
            'comments': all_comm, 
            'added': added,
            'form2': BidForm(), 
            'highest': highestbid['price__max'], 
            'numberbids': numberbids,
            'owner': owner,
            'close': close
        })

@login_required
def addcomment(request, id): 
    if request.method == "POST": 
        #fill up name, body, listing id
        c = comments()
        form = CommentForm(request.POST)
        if form.is_valid():
            c.name = request.user.username 
            c.body = form.cleaned_data["comment"]
            c.listingid = id
            c.save()
        return redirect("listing", id=id)      
    else:
        return render(request, "auctions/listing.html",{
            "product": product, 
            "comments": all_comm
        }) 

@login_required
def addwatchlist(request, id):
    if request.user.username:
        w = WatchList()
        w.listingid = id
        w.name = request.user.username
        w.save()
        messages.success(request, "Added to watchlist")
        return redirect("listing", id=w.listingid)
    else: 
        return redirect("index") 


@login_required
def removewatchlist(request, id):
    if request.user.username: 
        w = WatchList.objects.get(name=request.user.username, listingid=id)
        w.delete()
        return redirect("listing", id=id)
       
    else: 
        return redirect("index") 



@login_required
def watchlist(request): 
    all_results = listings.objects.all()
    if request.user.username: 
        w = WatchList.objects.filter(name=request.user.username)
        items = []
        for a in w:
            items.append(listings.objects.filter(id=a.listingid))

    return render(request, "auctions/watchlist.html", {
        "items": items
    })       


@login_required
def bid(request, id): 
    if request.user.username:
        form = BidForm(request.POST)
        if form.is_valid():
            obj2 = bidmodel()
            starting_bid = listings.objects.get(id=id)
            largest_bid = bidmodel.objects.filter(listingid=id).aggregate(Max('price'))
            obj2.name = request.user.username
            obj2.price = form.cleaned_data['amount']
            print(largest_bid['price__max'])
            if largest_bid['price__max'] == None:            
                if obj2.price < starting_bid.price:
                    messages.warning(request, "Bid is less than starting price. Bid rejected")
                    return redirect("listing", id=id)
            elif largest_bid['price__max'] != None: 
                if obj2.price <= largest_bid['price__max']:
                    messages.warning(request, "Bid is lower than or equal to highest bid. Bid rejected")
                    return redirect("listing", id=id)
            
            obj2.listingid = id
            obj2.save()
            messages.success(request, "Bid Accepted!")
            return redirect("listing", id=id)
    else: 
        return redirect("listing", id=id)

    
    

