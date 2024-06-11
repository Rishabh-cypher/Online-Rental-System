import json

from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest

from base_app.models import (
    ApplicationUser,
    AdminUser,
    RenterUser,
    RenterRegisterRequests,
    RenterRegisterResults,
)


def home_view(request: HttpRequest):
    context = {}

    # Loading json data from base_app/vehicle_data.json ( Mock Data )
    with open("base_app/vehicle_data.json") as file:
        data = json.load(file)
        context["vehicle_mock_data"] = data[:5]

    if request.user.is_authenticated and not request.user.is_renter:
        register_requests = RenterRegisterRequests.objects.filter(
            application_user=request.user, is_reviewed=False
        )

        # If a request already exists then notify the program
        # that the request already exists
        if register_requests.exists():
            context["is_already_requested"] = True

    return render(request, "base_app/home.html", context)


def handle_create_renter_register_request(request: HttpRequest):
    """
    EXTRACT renter_register_request user=current user, is_reviewed=False
    CHECK if requests already exists
    IF IT DOES:
        REDIRECT to home
    ELSE :
        CREATE requests
    """
    register_requests = RenterRegisterRequests.objects.filter(
        application_user=request.user, is_reviewed=False
    )

    # not register_requests.exists() is equivalent to reigster_requests.exists() == False
    if not register_requests.exists():
        RenterRegisterRequests(application_user=request.user).save()

    return redirect(reverse("home"))


def handle_reject_register_request(request: HttpRequest):
    if request.method == "POST":
        """
        EXTRACT request_id from POST request ✅
        GET RenterRegisterRequests object using that request_id ✅
        CHANGE is_reviewed in RenterRegisterRequest to True ✅
        CREATE new RenterRegisterResult and set the is_approved to False ✅
        """
        request_id = request.POST["request_id"]
        register_request = RenterRegisterRequests.objects.get(reference_id=request_id)
        register_request.is_reviewed = True

        # Get ApplicationUser from request.user and get its
        # corresponding AdminUser object
        current_admin_user = AdminUser.objects.get(application_user=request.user)

        RenterRegisterResults(
            renter_request=register_request,
            reviewed_by=current_admin_user,
            is_approved=False,
        ).save()
        register_request.save()

    return redirect(reverse("admin_renter_register_list"))


def handle_accept_register_request(request: HttpRequest):
    if request.method == "POST":
        """
        EXTRACT request_id from POST request ✅
        GET RenterRegisterRequests object using that request_id ✅
        CHANGE is_reviewed to TRUE ✅
        CHANGE that user's is_renter value to True ✅
        RETRIEVE the current admin user ✅
        CREATE RenterRequest result and set is_approved to True ✅
        """

        request_id = request.POST["request_id"]
        register_request = RenterRegisterRequests.objects.get(reference_id=request_id)
        register_request.is_reviewed = True

        current_admin_user = AdminUser.objects.get(application_user=request.user)

        # current_application_user: ApplicationUser = request.user
        # HOW WAS IT FIXED: here's request.user returns the current user i.e admin
        # However, the value is_renter field to be changed is the ApplicationUser's not admin's
        # Hence, we use the value of register_request.application_user which gives back the user making the request
        current_application_user: ApplicationUser = register_request.application_user
        current_application_user.is_renter = True
        current_application_user.save()

        # TODO: Create a RenterUser

        RenterRegisterResults(
            renter_request=register_request,
            reviewed_by=current_admin_user,
            is_approved=True,
        ).save()
        register_request.save()

    return redirect(reverse("admin_renter_register_list"))


def admin_renter_register_requests_list_view(request: HttpRequest):
    # Checking if the current user is admin or not
    # If they aren't admin then, redirect to home
    # Otherwise let them through
    if request.user.is_authenticated and request.user.is_admin:
        register_requests = RenterRegisterRequests.objects.filter(is_reviewed=False)
        return render(
            request,
            "base_app/admin_renter_register_requests.html",
            {"requests": register_requests},
        )
    return redirect(reverse("home"))


def login_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "base_app/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            print("Logged in")

    return redirect(reverse("home"))

    """
        GET / Show Login
        POST /
        USERNAME, PASSWORD
        authenticate ->  User or None
        User check ( if user: )
        Login
    """


def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone_no = request.POST["phone_no"]
        password = request.POST["password"]

        ApplicationUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_no=phone_no,
            password=password,
        ).save()
        return redirect(reverse("login"))

    return render(request, "base_app/register.html")

    """
        GET / Show Login Done
        POST / Done
        Extraction Done
        Create Done
        redirect to Login Done
    """


def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse("home"))
