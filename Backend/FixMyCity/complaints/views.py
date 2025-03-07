from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Complaint

from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return HttpResponseRedirect("http://localhost:3000")

def get_all_complaints(request):
    complaints = Complaint.objects.all().values(
        'id', 'user__username', 'image', 'location', 'description', 'summary',
        'classified_domain__name', 'vote', 'assigned__username',
        'submitted_date', 'completed_date', 'status', 'severity_score'
    )
    return JsonResponse(list(complaints), safe=False)
