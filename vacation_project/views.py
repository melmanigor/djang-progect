from django.http import HttpResponse,HttpRequest
from django.shortcuts import render

# Create your views here.
def home(request:HttpRequest)->HttpResponse:
    """
    Render the homepage.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered homepage template.
    """
    return render(request, 'home.html')