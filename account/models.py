from email.policy import default
from django.db import models

from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    telephone = models.TextField(default=0)
    type  = models.SmallIntegerField(default=2)
    raison = models.TextField(default=0)
    nom = models.TextField(default=0)
    prenom = models.TextField(default=0)
    ville = models.TextField(default=0)
    quartier = models.TextField(default=0)
    sexe = models.TextField(default=0)
    description = models.TextField(default=0)
    image_profile = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.user.username 
    
    def __str__(self):
       return str(self.user)
        
    