from django.shortcuts import render

# Create your views here.
def index(request):
    # Render index.html
    return render( request, 'calendar_app/index.html')

def WeekView(request):
    return render(request, 'calendar_app/week_view.html')