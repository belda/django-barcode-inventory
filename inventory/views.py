# Create your views here.
from inventory.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import Template, Context, RequestContext
from django.conf import settings as settings
from django.views.decorators.cache import never_cache
from datetime import datetime

def list(request): 
    items = Item.objects.all()
    return render_to_response( "inventory/list.html" , { "items" : items }, context_instance = RequestContext(request))


@never_cache
def detail(request, id, barcode):
    try:
        item = Item.objects.get(pk=int(id))
    except Item.DoesNotExist:
        raise Http404
    
    iv = ItemView(item = item, barcode = barcode)
    iv.ip       = request.META['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.META else ""
    iv.host     = request.META['REMOTE_HOST'] if 'REMOTE_HOST' in request.META else ""
    iv.agent    = request.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in request.META else ""
    iv.save()
    
    if request.method == 'POST':
        form = ItemCommentsForm(request.POST)
        if form.is_valid():
            form.save()
            form = ItemCommentsForm() 
    else:
        form = ItemCommentsForm()
        
    return render_to_response( "inventory/detail.html", { "item" : item, "form" : form }, context_instance = RequestContext(request))

def print_stickers(request):
    items = Item.objects.all()
    return render_to_response( "inventory/print_tickets.html" , { "items" : items, "baseurl" : settings.BASEURL }, context_instance = RequestContext(request))
def print_sticker(request, id):
    items = Item.objects.filter(pk=int(id))
    return render_to_response( "inventory/print_tickets.html" , { "items" : items, "baseurl" : settings.BASEURL }, context_instance = RequestContext(request))