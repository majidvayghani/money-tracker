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

class Model(TimeStampable, SoftDeletes, models.Model):
    class Meta:
        """
            the abstract = True option in the Meta class of a model is 
            used to define an abstract base class. An abstract base class
            is a model that is not meant to be instantiated or directly used to create database tables.
            
        """
        abstract = True