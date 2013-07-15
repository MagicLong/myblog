#-*- coding:utf8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Username or Password Error')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('User is not actived')

        return self.cleaned_data


@csrf_protect
def login(request, template_name="blog_login.html"):
    import pdb
    pdb.set_trace()

    form = {}
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            login(request, form.get_user())

            url = reverse('manage_index')
            return HttpResponseRedirect(url)

    return render_to_response(template_name, RequestContext(request, {
        'form' : form,
        }))


def manage_index(request, template_name="manage_index.html"):
    return render_to_response(template_name, RequestContext(request, {
        }))
