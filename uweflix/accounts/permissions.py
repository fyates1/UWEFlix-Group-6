from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from .models import User

class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        user_required = view_kwargs.get('user_required', None)
        user_type_required = view_kwargs.get('user_type_required', None)

        if user_required or user_type_required:
            user = self.get_authenticated_user(request)
            if not user:
                return redirect(reverse('login') + '?message=Login Required')

            if user_type_required and user.userType != user_type_required:
                return redirect(reverse('home') + '?message=You do not have the relevant permissions')

    @staticmethod
    def get_authenticated_user(request):
        user_id = request.session.get('id', None)
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                return user
            except User.DoesNotExist:
                return None
        return None
