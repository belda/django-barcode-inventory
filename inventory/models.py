from django.db import models
from django.forms import ModelForm


class Item(models.Model):
    name        = models.CharField(max_length=1023, help_text="The name of the item to be used")
    owner       = models.CharField(max_length=127, blank=True, null=True,help_text="Who actualy owns this item")
    location    = models.CharField(max_length=255, help_text="The default location of this item")
    description = models.TextField(blank=True, null=True, help_text="Additional information about this item")
    added       = models.DateTimeField(auto_now_add=True, editable=False)
    last_edit   = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.name+" ["+str(self.pk)+"]"
    
    def _last_view(self):
        ivs = ItemView.objects.filter(item=self).order_by('-date')
        if len(ivs)==0:
            return None
        else:
            return ivs[0].date
    last_view   = property(fget=_last_view)
    
    def _last_barcode(self):
        ivs = ItemView.objects.filter(item=self, barcode=True).order_by('-date')
        if len(ivs)==0:
            return None
        else:
            return ivs[0].date
    last_barcode = property(fget=_last_barcode)
    
    def _item_views(self):
        return ItemView.objects.all().order_by('-date')
    item_views = property(fget=_item_views)
    
    def _item_comments(self):
        return ItemComment.objects.all().order_by('-date')
    item_comments = property(fget=_item_comments)
    
    
    
class ItemView(models.Model):
    item        = models.ForeignKey(Item)
    date        = models.DateTimeField(auto_now_add=True, db_index=True)
    ip          = models.CharField(max_length=15)
    host        = models.CharField(max_length=255)
    user_agent  = models.CharField(max_length=255)
    barcode     = models.BooleanField(default=False)
    
class ItemComment(models.Model):
    item        = models.ForeignKey(Item)
    date        = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    comment     = models.TextField()

class ItemCommentsForm(ModelForm):
    class Meta:
        model = ItemComment