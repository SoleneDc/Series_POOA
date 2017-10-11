from django.http import HttpResponse
"""This class defines the controllers for the application
each fonction is supposed to process a page and send it to thhe url mapper"""

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)