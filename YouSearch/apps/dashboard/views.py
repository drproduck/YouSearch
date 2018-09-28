from django.shortcuts import render
from django.http.response import HttpResponse
from  django.contrib.auth.decorators import login_required
from YouSearch.settings import DOCUMENT_ROOT

import os
# Create your views here.


@login_required
def main(request):
    user = request.user
    username = user.username
    path = os.path.join(DOCUMENT_ROOT, username)
    if not os.path.exists(path):
        os.makedirs(path)
    file_list = [f for f in os.listdir(path)]
    return render(request, template_name='dashboard/main.djt', context={'user': user})
