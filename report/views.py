from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms 
from .forms import ProfileForm, UserCreateForm, LoginForm


class IndexView(TemplateView):
  template_name = 'report/day_list.html'

class MyLoginView(LoginView):
  form_class = forms.LoginForm
  template_name = 'report/login.html'

class MyLogoutView(LoginRequiredMixin, LogoutView):
  template_name = 'report/logout.html'

def register_user(request):
  user_form = UserCreateForm(request.POST or None)
  profile_form = ProfileForm(request.POST or None)
  if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():

    #Userモデル処理。ログインをできるようにis_activeをTrueにして保存
    user = user_form.save(commit=False)
    user.is_active = True
    user.save()

    # Profileモデルの処理。↑のUserモデルと紐づけましょう。
    profile = profile_form.save(commit=False)
    profile.user = user
    profile.save()
    return redirect("report:index")

  context = {
    "user_form": user_form,
    "profile_form": profile_form,
  }
  return render(request, 'register/user_create.html', context)
 