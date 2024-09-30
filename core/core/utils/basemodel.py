from django.db import models

class TimeStampable(models.Model):
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        class Meta:
            abstract = True

class SoftDeletes(models.Model):
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        abstract = True
