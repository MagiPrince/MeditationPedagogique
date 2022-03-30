from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    # Get all lectures in the DB
    context = {
        'test': 'CECI EST UN TEST'
    }
    return render(request, "index.html", context)
