from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.

# model for creating advertisements
class advertisements(models.Model):
    PLACE=[
        ('mothijheel', 'Mothijheel'),
        ('bonosree', 'Bonosree'),
        ('mirpur', 'Mirpur'),
        ('khilgao', 'Khilgao'),
        ('gulshan', 'Gulshan'),
        ('badda', 'Badda'),
        ('uttora', 'Uttora'),
        ('banani', 'Banani'),
    ]
    place=models.CharField(max_length=30,choices=PLACE)
    address=models.CharField(max_length=50)
    bedroom=models.PositiveSmallIntegerField()
    bathroom=models.PositiveSmallIntegerField()
    rent=models.PositiveIntegerField()
    size=models.PositiveIntegerField()
    date_posted=models.DateTimeField(default=timezone.now)
    owner= models.ForeignKey(User,on_delete=models.CASCADE)
    number=models.PositiveIntegerField(null=True)
    
      
    def get_absolute_url(self):
        return reverse('advertisement_details', kwargs={'id':self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

# Model for uploading images
class images(models.Model):
    advertisement=models.ForeignKey(advertisements,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='house_pics/',blank=True, null=True)

    def __str__(self):
        return self.advertisement.place + "Image"


# Model for comment section
class Comment(models.Model):
    advertisement=models.ForeignKey(advertisements,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment' , null=True , related_name = "replies" , on_delete = models.CASCADE)
    content=models.TextField(max_length=200)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.advertisement.id, str(self.user.username))

    
    
