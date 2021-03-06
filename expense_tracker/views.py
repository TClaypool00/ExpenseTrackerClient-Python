from api.api import Api
from django.shortcuts import redirect, render
from forms import LoginForm, RegisterForm
from django.contrib.auth import logout, views as auth_views
from forms import RegisterForm
from django.contrib.auth.decorators import login_required
from api import api
from api.loan import loan_url
from api.bills import bill_url
from api.subs import sub_url
from api.misc import misc_url
from api.budgets import BudgetApi
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime


@login_required()
def index(request):
    user_id = request.user.userid
    user_budget = BudgetApi.get(BudgetApi, user_id, budget_id=None)
    today = datetime.now()
    if today.day == 1:
        BudgetApi.update_budget(BudgetApi, user_id, user_budget['savingsMoney'], user_budget['budgetId'])
    user_bills = api.Api.get_all(Api, bill_url, user_id, search=None, post_id=None)
    user_loans = api.Api.get_all(Api, loan_url, user_id, search=None, post_id=None)
    user_subs = api.Api.get_all(Api, sub_url, user_id, search=None, post_id=None)
    user_misc = api.Api.get_all(Api, misc_url, user_id, search=None, post_id=None)
    CONTEXT = {'bills' : user_bills, 'loans' : user_loans, 'subs' : user_subs, 'miscs' : user_misc, 'budget' : user_budget}
    if request.method == 'POST':
        BudgetApi.create_budget(Api, user_id)
        
        return redirect('/myBudget/edit')
    else:
        return render(request, "index.html", CONTEXT)


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/login')


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success('Your password was sucessfully changed!')
            return redirect('/')
        else:
            messages.error(request, 'Password was not updated.')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form' : form})