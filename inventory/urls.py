from django.conf.urls.defaults import *

urlpatterns = patterns('',            
    (r'^list/', 'inventory.views.list' ),
    (r'^detail/(?P<id>[0-9]*)/', 'inventory.views.detail', {'barcode' : False} ),
    (r'^barcode/(?P<id>[0-9]*)/', 'inventory.views.detail', {'barcode' : True} ),
    (r'^print_stickers/', 'inventory.views.print_stickers' ),
    (r'^print_sticker/(?P<id>[0-9]*)/', 'inventory.views.print_sticker' ),
)