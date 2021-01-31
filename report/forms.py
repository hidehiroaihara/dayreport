# ログイン機能（djangoに用意されているフォーム拡張機能
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserCreationForm # ユーザーモデルと紐づけるためのコード
from .models import Profile
from django import forms

class LoginForm(auth_forms.AuthenticationForm):
  # ログインフォーム
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs['placeholder'] = field.label

class UserCreateForm(UserCreationForm):
  pass

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = (
      "name", "gender", "phone"
    )
