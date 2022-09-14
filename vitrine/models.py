
from distutils.command.upload import upload
from email.policy import default
from tokenize import blank_re
from django.db import models

from account.models import Profile
from django.contrib.auth.models import User
# Create your models here.

class Bien(models.Model):
    titre = models.CharField(max_length=300)
    description = models.CharField(max_length=800)
    offre = models.CharField(max_length=100)
    type_bien = models.CharField(max_length=100)
    image = models.ImageField(null=False, blank=False)
    prix = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    date_publication = models.DateTimeField(auto_now_add=True)
    douche = models.TextField(default=0)
    sallon = models.TextField(default=0)
    chambre = models.TextField(default=0)
    superficie = models.TextField(default=0)
    autre_image = models.ImageField(null=False, blank=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Demandes(models.Model):
    mademande = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
  
    def __str__(self):
        return self.user.id 
    
class Blog(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.CharField(max_length=800)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Commentaire(models.Model):
    commentaire = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Messages(models.Model):
    message = models.CharField(max_length=500)
    bien  = models.CharField(max_length=100, default=0)
    emetteur = models.CharField(max_length=100)
    recepteur = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    raison = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
 