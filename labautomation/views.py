from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello, World! Bem-vindo à LabAutomation by Routerfleet!")