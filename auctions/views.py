from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Item, Category, Watchlist, Comment, Bid
from .forms import CreateListingForm, CommentForm, BidForm


def index(request):
    
    # kimonos = Item.objects.filter(category__name="GI")
    
    # Making category list for dropdown menu - Categories
    category_querySet =  Category.objects.values()
    category_list = [entry for entry in category_querySet]
    request.session["categories"] = category_list
    
    active_listings = Item.objects.filter(active=True)
    return render(request, "auctions/index.html", context={"active_listings": active_listings})


def listings(request, item_id):
    try:
        listing = Item.objects.get(pk=item_id)
    except:
        messages.warning(request, "Item doesn't exists.")
        return HttpResponseRedirect(reverse("index"))
    
    # All bids on current item order by price in descending order - highest is the first
    item_bids = Bid.objects.filter(item=listing).order_by('-offer')
    numb_of_bids = len(item_bids)
    print(numb_of_bids)
    user_current_bid = False
    if numb_of_bids > 0 :
        if item_bids[0].bidder == request.user:
            user_current_bid = True
        
    if request.method == "GET":
            # If user owns this listing it can close it and modify it
            user_listing = listing.created_by == request.user
            
            condition = listing.condition == "NEW"
            
            try:
                watchlist = Watchlist.objects.get(user=request.user, item=listing)
                listing_watched = watchlist.watched
            except:
                listing_watched = False
            
            item_is_active = listing.active
            if not item_is_active and user_current_bid:
                messages.success(request, f"Congratulations! You have bought this item for {item_bids[0].offer} €")
            # We want newest comment at the top
            comments = reversed(Comment.objects.filter(item=listing))
            
            return render(request, "auctions/listing.html",
                        context={"item": listing,
                                 "is_item_new": condition,
                                 "can_be_modified": user_listing,
                                 "item_on_watchlist": listing_watched,
                                 "comment_form": CommentForm(),
                                 "bid_form": BidForm(),
                                 "all_comments": comments,
                                 "number_of_bids": numb_of_bids,
                                 "user_current_bid":user_current_bid,
                                 "item_is_active": item_is_active,})
            
    elif request.method == "POST":
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        # Posting Comment via CommentForm
        if 'post_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                title = "No title"
                if not form.cleaned_data["title"] in ["", None]:
                    title = form.cleaned_data["title"]
                    
                comment = Comment.objects.create(
                    item=listing,
                    user=request.user,
                    title=title,
                    content=form.cleaned_data["content"])
        
        if 'place_bid' in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                bid = float(form.cleaned_data["price"])
                current_item_price = float(listing.price)
                
                # If there are no bids so far, starting price will be target_price,
                # otherwise every new target price should be 10% higher
                if numb_of_bids == 0:
                    target_price = current_item_price
                    tp_format = "{:.2f}".format(target_price)
                    # We will prepare error message if it occurs later on
                    error_message = f"Your bid needs to be at least as starting price ({tp_format} €)"
                else:
                    target_price = round(current_item_price * 1.1, 2)
                    tp_format = "{:.2f}".format(target_price)
                    error_message = f"Your bid needs to be at least 10% ({tp_format} €) higher than current price"

                # Checking whether user bid is at least as target price     
                if bid >= target_price:
                    messages.success(request, "Your bid is placed.")
                    # Listing current price will become that bid
                    listing.price = bid
                    listing.save()
                    # New bid is created in the model
                    Bid.objects.create(item=listing, bidder=request.user, offer=bid)
                else:
                    messages.warning(request, error_message)
                    
        return HttpResponseRedirect(reverse('listings', kwargs={'item_id':item_id}))
    

def categories(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        items = Item.objects.filter(category=category)
        return render(request, "auctions/categories.html", context={"items": items, "category": category.name})
    except:
        messages.warning(request, "No such category")
        return HttpResponseRedirect(reverse("index"))
        
        
# NEXT VIEWS ONLY LOGED IN USER CAN DO
def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            
            details = "No details available."
            if not form.cleaned_data["details"] in ["", None]:
                details = form.cleaned_data["details"]
                
            img_url = "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/bjj-logo-design-template-20f626b12d9207649f81a24f4ce48308_screen.jpg?ts=1678120477"
            if not form.cleaned_data["img_url"] in ["", None]:
                img_url = form.cleaned_data["img_url"]   
                             
            listing = Item.objects.create(
                name=form.cleaned_data["title"],
                price=form.cleaned_data["starting_price"],
                condition=form.cleaned_data["condition"],
                img_URL=img_url,
                created_by=request.user,
                category=form.cleaned_data["category"],
                details=details,
            )
            
            listing_id = Item.objects.get(name=form.cleaned_data["title"]).id
            
            return HttpResponseRedirect(reverse('listings', kwargs={'item_id': listing_id}))
        
    return render(request, "auctions/create.html", context={"form": CreateListingForm()})


def delete_listing(request, item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    try:
        item = Item.objects.get(pk=item_id)
        
        # Only user which created item and admin can delete item
        if item.created_by == request.user or request.user.is_superuser:
            item.delete()
            messages.success(request, "Item succesfully deleted")
        else:
            messages.warning(request, "You cannot delete this item")
        
        raise    
    except:
        return HttpResponseRedirect(reverse("index"))
   
        
def edit_listing(request, item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    try:
        item = Item.objects.get(pk=item_id)
    except:
        messages.warning(request, "Item doesn't exists.")
        return HttpResponseRedirect(reverse("index"))
        
    # Only user which created item and admin can delete item
    if item.created_by == request.user or request.user.is_superuser:
        if request.method == "GET":
            data = {
                'title': item.name, 
                'starting_price': item.price,
                'condition': item.condition,
                'img_url': item.img_URL,
                'category': item.category ,
                'details': item.details}
            return render(request, "auctions/edit.html", context={"form": CreateListingForm(initial=data), "listing_id": item.id})
        
        elif request.method == "POST":
            form = CreateListingForm(request.POST)
            if form.is_valid():
                item.name = form.cleaned_data["title"]
                item.price = form.cleaned_data["starting_price"]
                item.condition = form.cleaned_data["condition"]
                item.img_URL = form.cleaned_data["img_url"]
                item.category = form.cleaned_data["category"]
                item.details = form.cleaned_data["details"]
                item.save()
                messages.success(request, "Item succesfully edited")
    else:
        messages.warning(request, "You cannot edit this item")
    
    return HttpResponseRedirect(reverse('listings', kwargs={'item_id': item.id}))


def close_listing(request, item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    try:
        item = Item.objects.get(pk=item_id)
    except:
        messages.warning(request, "Item doesn't exists.")
        return HttpResponseRedirect(reverse("index"))
    
    if item.created_by != request.user:
        messages.warning(request, "You cannot close this item.")
        return HttpResponseRedirect(reverse('listings', kwargs={'item_id':item_id}))
    
    # Closing the item means it is currently active but won't be afterwards
    if item.active:
        item.active = False
        messages.success(request, "Listing is closed!")
        item.save()
    
    return HttpResponseRedirect(reverse('listings', kwargs={'item_id':item_id}))

        

        

# Only user can see its own watchlist
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    user_watchlist = Watchlist.objects.filter(user=request.user)
    
    listings = []
    for _ in user_watchlist:
        # Only watched == True item should be presented
        if _.watched:
            listings.append(_.item)
    
    return render(request, "auctions/user_listings.html", context={"user_listings": listings, "title": "My Watchlist"})


def watchlist_add(request, item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    try:
        watch_item = Item.objects.get(pk=item_id)
    except:
        messages.warning(request, "Item doesn't exists.")
        return HttpResponseRedirect(reverse("index"))
    
    # If there is already item in the watchlist database
    try:
        watchlist = Watchlist.objects.get(item=watch_item, user=request.user)
        # IF the item is already on the watchlist
        if watchlist.watched == True:
            messages.warning(request, "Item is already in the watchlist!")
            
    # Instead create watchlist item in database
    except:
        watchlist = Watchlist.objects.create(user=request.user, item=watch_item, watched=True)
        watchlist.save()
        messages.success(request, "Item successfully added on the watchlist!")
    
    return HttpResponseRedirect(reverse('listings', kwargs={'item_id': item_id}))
    

def watchlist_remove(request, item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    try:
        watch_item = Item.objects.get(pk=item_id)
    except:
        messages.warning(request, "Item doesn't exists.")
        return HttpResponseRedirect(reverse("index"))
    
    # To remove item from watchlist, it should already being there
    try:
        watchlist = Watchlist.objects.get(item=watch_item, user=request.user)
        # IF the item is watched, then it should be removed calling this view
        if watchlist.watched:
            watchlist.delete()
            messages.success(request, "Item successfully removed from the watchlist!")
            raise
    except:
        return HttpResponseRedirect(reverse('listings', kwargs={'item_id': item_id}))


def user_listings(request, username):
    user_listings = Item.objects.filter(created_by__username=username)
    
    title = f"{username} Listings"
    
    try:
        if username == request.user.username:
            title = "My Listings"
    except:
        title = f"{username} Listings"
    
    return render(request, "auctions/user_listings.html", context={"user_listings": user_listings, "title": title})
    

def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    try:
        comment = Comment.objects.get(pk=comment_id)
    except:
        messages.warning(request, "Comment doesn't exists.")
        
    # Only admin and user who created comment can delete comment
    if comment.user == request.user or request.user.is_superuser:
        item_id = comment.item.id
        comment.delete()
        messages.success(request, "Comment deleted.")
        return HttpResponseRedirect(reverse('listings', kwargs={'item_id':item_id}))
    else:
        messages.warning(request, "You cannot delete this comment.")

    return HttpResponseRedirect(reverse("index"))
        
    

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
