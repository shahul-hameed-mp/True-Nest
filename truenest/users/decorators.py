from django.contrib import messages
from django.shortcuts import redirect


def login_required(fn):
    """
    This decorator will check if the user is logged in.
    If not, it will redirect them to the login page.
    """
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.warning(request,"you must login first")
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper