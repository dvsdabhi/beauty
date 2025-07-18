# utils/decorators.py
from django.shortcuts import redirect
from functools import wraps

def customer_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('customer_id'):
            return redirect(f"/login/?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper
