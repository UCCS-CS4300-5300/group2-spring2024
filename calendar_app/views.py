from django.shortcuts import render

# Create your views here.
def exampleView(request):
    return render(request,'test.html')
