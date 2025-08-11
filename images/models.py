from django.db import models

class StoredImage(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=255, default="Unnamed Image")

    def __str__(self):
        return self.name
    
class StoredImage(models.Model):  
    image = models.ImageField(upload_to="uploads/")  
    tags = models.CharField(max_length=255, blank=True)  

