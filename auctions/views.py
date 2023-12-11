from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Auction, Comment, Watchlist
from .forms import NewCommentForm, NewListingForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    return render(request, "auctions/index.html")

def posts(request):
    return render(request, "auctions/posts.html", {
        "auctions": Auction.objects.order_by('-creation_date')
    })
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # return successful message
            messages.success(request, f'Welcome, {username}. Login successfully.')

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
        profile_pic = request.POST["profile_pic"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, profile_pic=profile_pic)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login") 
def watchlist(request):
    # check the existence of the user's watchlist
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        auctions = watchlist.auctions.all().order_by('-id')
        # calculate the number of items in the watchlist
        watchingNum = watchlist.auctions.all().count()

    except ObjectDoesNotExist:
        # if watchlist does not exist
        watchlist = None
        auctions = None
        watchingNum = 0
    
    return render(request, "auctions/watchlist.html", {
        # return the listings in the watchlist
        "watchlist": watchlist,
        "auctions": auctions,
        "watchingNum": watchingNum
    })


@login_required(login_url="login")
def create(request):
    # check the request method is POST
    if request.method == "POST":
        # create a form instance with POST data
        form = NewListingForm(request.POST, request.FILES)

        # check whether it's valid
        if form.is_valid():
            # save the form from data to model
            new_listing = form.save(commit=False)
            # save the request user as seller
            new_listing.seller = request.user
            new_listing.save()

            # return successful message
            messages.success(request, 'Created the auction listing successfully.')

            # redirect the user to the index page
            return HttpResponseRedirect(reverse("index"))

        else:
            form = NewListingForm()

            # if the form is invalid, re-render the page with existing information
            messages.error(request, 'The form is invalid. Please resubmit.')
            return render(request, "auctions/create.html", {
                "form": form
            })
    
    # if the request method is GET
    else:
        form = NewListingForm()
        return render(request, "auctions/create.html", {
            "form": form
        })


def listing(request, auction_id):  
    try:
        # get the auction listing by id
        auction = Auction.objects.get(pk=auction_id)
        
    except Auction.DoesNotExist:
        return render(request, "auctions/error.html", {
            "code": 404,
            "message": "The auction does not exist."
        })

    # set watching flag be False as default
    watching = False

    # check if the auction in the watchlist
    if request.user.is_authenticated and Watchlist.objects.filter(user=request.user, auctions=auction):
        watching = True
    
    # get the page request user
    user = request.user

    # get all comments of the auction
    comments = Comment.objects.filter(auction=auction_id).order_by("-cm_date")
    
    # check the request method is POST
    if request.method == "GET":
        commentForm = NewCommentForm()

        return render(request, "auctions/listing.html", {
        "auction": auction,
        "user": user,
        "commentForm": commentForm,
        "comments": comments,
        "watching": watching
        }) 

    
    # listing itself does not support POST method
    else:
        return render(request, "auctions/error.html", {
            "code": 405,
            "message": "The POST method is not allowed."
        })
               

@login_required(login_url="login")
def comment(request, auction_id):
    # check to handle POST method only
    if request.method == "POST":

        # check the existence auction
        try:
            # get the auction listing by id
            auction = Auction.objects.get(pk=auction_id)     
            
        except Auction.DoesNotExist:
            return render(request, "auctions/error.html", {
                "code": 404,
                "message": "The auction does not exist."
            })
            
        # create a form instance with POST data
        form = NewCommentForm(request.POST, request.FILES)

        # check whether it's valid
        if form.is_valid():
            # save the comment from from data to model
            new_comment = form.save(commit=False)
            # save the request user who leaves the comment
            new_comment.user = request.user
            # save the auction for this comment
            new_comment.auction = auction
            new_comment.save()

            # return successful message
            messages.success(request, 'Commented successfully.')

            return JsonResponse({"message": "Comment added successfully", "status": "success"})
        
        # handle invalid comment form
        else:
            # if the form is invalid
            messages.error(request, 'Please submit a valid comment.')
     
    # comment view do not support get method
    else:
        return render(request, "auctions/error.html", {
            "code": 405,
            "message": "The GET method is not allowed."
        })

@login_required(login_url="login")
def addWatchlist(request, auction_id):   
    # Check if the request method is POST
    if request.method == "POST":
        # Get the auction item or return a 404 not found error
        auction = get_object_or_404(Auction, pk=auction_id)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        # If the auction listing is already in the watchlist return a JSON error
        if auction in watchlist.auctions.all():
            print(f"Auction {auction_id} is already in the watchlist")
            return JsonResponse({"status": "error", "message": "Already in watchlist"})
        else:
            # Otherwise add the listing to the user's watchlist and the watchlist icon should change state
            watchlist.auctions.add(auction)
            print(f"Auction {auction_id} added to the watchlist")
            return JsonResponse({"status":"success", "added": True})
    else:
        # If the request method is not a POST return a JSON error
        return JsonResponse({"status": "error", "message": "GET method not allowed"}, status=405)
    
@login_required(login_url="login")
def removeWatchlist(request, auction_id):  
    # Check if the request method is POST 
    if request.method == "POST":
        # Get the auction item or return a 404 not found error
        auction = get_object_or_404(Auction, pk=auction_id)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        # If the auction listing is in the watchlist, remove it and return a JSON success response. Icon should change state
        if auction in watchlist.auctions.all():
            watchlist.auctions.remove(auction)
            print(f"Auction {auction_id} removed from the watchlist")
            return JsonResponse({"status": "success", "removed": True})
        else:
            # Otherwise the listing was already removed so return a JSON error
            print(f"Auction {auction_id} not in the watchlist")
            return JsonResponse({"status": "error", "message": "Not in watchlist"})
    else:
        # If the request method is not a POST return a JSON error
        return JsonResponse({"status": "error", "message": "GET method not allowed"})


def get_comments(request, auction_id):
    try:
        comments = Comment.objects.filter(auction=auction_id).order_by("-cm_date")

        # Manually serialize the comments into a JSON format
        comments_data = [
            {
                'username': comment.user.username,
                'cm_date': comment.cm_date.strftime('%Y-%m-%d %H:%M:%S'),
                'message': comment.message,
            }
            for comment in comments
        ]

        return JsonResponse(comments_data, safe=False, content_type='application/json')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
@login_required(login_url="login")
def accountSettings(request):
    return render(request, 'auctions/account_settings.html')
    

@login_required(login_url="login")
def accountSettings(request):

    return render(request, 'auctions/account_settings.html')
    