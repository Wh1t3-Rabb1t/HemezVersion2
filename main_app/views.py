from django.shortcuts import render

# Create your views here.
def lobby(request):
    return render(request, 'lobby.html')

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def chatrooms(request):
  return render(request, 'chatrooms.html')

def userpage(request):
  return render(request, 'userpage.html')