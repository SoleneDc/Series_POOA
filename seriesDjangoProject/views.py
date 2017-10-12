from django.http import HttpResponse
from django.template import loader
"""This class defines the controllers for the application
each fonction is supposed to process a page and send it to thhe url mapper"""

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request=request))