from django.shortcuts import render

# Create your views here.
def exampleView(request):
    return render(request,'test.html')

def index(request):
    # Render index.html
    return render( request, 'calendar_app/index.html')

def WeekView(request):
    return render(request, 'calendar_app/week_view.html')