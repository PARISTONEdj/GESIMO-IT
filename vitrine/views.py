from email import message
from itertools import count
from multiprocessing import context
from urllib import response
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Bien, Demandes, Blog, Commentaire, Messages
from django.contrib.auth.models import User
from account.models import Profile
from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from reportlab.pdfgen import canvas
import csv
import io
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import xlsxwriter
from io import BytesIO
from io import StringIO
import xlwt
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout



# Create your views here.
def nav(request):
    return render(request, 'navbar.html')

def acceuil(request):
    bien_list = Bien.objects.all()
    agent = Profile.objects.all().exclude(type = 2).exclude(type = 3)
    context = {
        "bien_list" : bien_list,
        'agent' : agent
    }
    return render(request, 'acceuil.html',  context)    

def vente(request):
    ven = Bien.objects.all().exclude(offre = "Location")
    context = {
        "ven" : ven
    }
    return render(request, 'vente.html', context)

def location(request):
    loc = Bien.objects.all().exclude(offre = "Vente")
    context = {
        "loc" : loc
    }
    return render(request, 'location.html', context)

def detail(request,  myid):
    if request.method == 'POST':
        mes = request.POST.get('message')
        recepteur = request.POST.get("recepteur")
        email = request.POST.get("email")
        raison = request.POST.get("raison")
        telephone = request.POST.get("telephone")

        mess = Messages.objects.create(message = mes, bien = myid, emetteur = request.user.username, recepteur = recepteur, email = email, raison = raison, telephone=telephone)
        mess.save()
    bien = Bien.objects.filter(id = myid)
    context = {
        "bien" : bien
    }
    return render(request, 'detail.html', context)

def agent_index(request):
   annonce = Bien.objects.all().filter(user = request.user).count()
   blog = Blog.objects.all().filter(user = request.user).count()
   commentaire = Commentaire.objects.all().filter(user = request.user).count()
   context = {
       'annonce' : annonce,
       'blog' : blog,
       'commentaire' : commentaire,
   }
   return render(request, 'agent/agent_index.html', context)

def client_index(request):
    return render(request, 'client/client_index.html')

@login_required(login_url='/user/accounts/login/')
def client_demande(request):
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        ina = request.POST.get("ina")
        print(contenu)
        
        if (contenu =="" or ina ==""):
            messages.success("renseigner le champs")
            return redirect('/client_demande')

    
        else:
            demandes = Demandes.objects.create(mademande = contenu, user = request.user)    
            demandes.save()
            return redirect('/client_demande')
        
        
    demande_list = Demandes.objects.all()
    context = {
        "demande_list" : demande_list
    }
    
    return render(request, 'client/demande.html', context)


def delete_demande(request, myid):
    demande = Demandes.objects.get(id = myid)
    demande.delete()
    # messages.info("demande annuler")
    return redirect('/client_demande')




def rech(request):
    if request.method == 'POST':
        querry = request.POST.get("querry")
        rech = Bien.objects.filter(titre = querry)
        context = {
            'rech' : rech
        }
    return render(request, 'agent/search_anonce.html', context)    
        
def rech_bien(request):
    if request.method == 'POST':
        ville = request.POST.get("ville")
        quartier = request.POST.get("ville")
        type = request.POST.get("ville")
        description = request.POST.get("ville")

        rech = Bien.objects.filter(ville = ville)
        type = Bien.objects.filter(type_bien = type)
        context = {
            'rech' : rech,
            'type' : type
        }
    return render(request, 'search.html', context)    
    
def annonce(request):
    bien_list = Bien.objects.all().filter(user = request.user)
    context = {
        "bien_list" : bien_list
    }
    return render(request, 'agent/liste_annonce.html', context)

def delete_bien(request, myid):
    bien = Bien.objects.get(id = myid)
    bien.delete()
    return redirect('/annonce')

def detail_bien(request, myid):
    bien = Bien.objects.filter(id = myid)
    context = {
        "bien" : bien
    }
    return render(request, 'agent/detail_bien.html', context)


def update_bien(request, myid):
        
    bien = Bien.objects.get(id=myid)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(bien.image) > 0:
                os.remove(bien.image.path)
                bien.image = request.FILES['logo']
            bien.titre = request.POST.get('titre')
            bien.description = request.POST.get('description')
            bien.prix = request.POST.get('prix')
            bien.chambre = request.POST.get('chambre')
            bien.douche = request.POST.get('eau')
            bien.sallon = request.POST.get('sallon')
            bien.superficie = request.POST.get('superficie')

            bien.save()
        
        else:
            # bien.image = bien.image.url
            bien.titre = request.POST.get('titre')
            bien.description = request.POST.get('description')
            bien.prix = request.POST.get('prix')
            bien.chambre = request.POST.get('chambre')
            bien.douche = request.POST.get('eau')
            bien.sallon = request.POST.get('sallon')
            bien.superficie = request.POST.get('superficie')
            bien.save()
                    
        return redirect('/annonce')

    bien = Bien.objects.filter(id = myid)
    context = {
        "bien" : bien
    }
    return render(request, 'agent/update_bien.html', context)


def publication(request):
    
    if request.method == 'POST':
        data = request.POST
        # ville = request.POST.get('ville')
        # quartier = request.POST.get('quartier')
        # type = request.POST.get('type')
        # offre = request.POST.get('offre')
        # description = request.POST.get('description')
        logo = request.FILES.get('logo')
        # prix = request.POST.get("prix")
        # superficie = request.POST.get("superficie")
        # chambre = request.POST.get("chambre")
        # sallon = request.POST.get("sallon")
        # eau = request.POST.get("eau")
        images = request.FILES.get("image")

       
        if(logo == ""):
            return redirect('/')
        
        else:
            # for ima in images:
                
            biens = Bien.objects.create(
                offre = data['offre'], description = data['description'],
                quartier = data['quartier'], ville = data['ville'],
                douche = data['eau'], image = logo,
                type_bien = data['type'], 
                prix = data['prix'], sallon=data['sallon'],
                autre_image = images,
                titre = data['titre'],
                superficie = data['superficie'],
                chambre = data['chambre'],
                user = request.user) 
                
            return redirect('/annonce')
    
    return render(request, "agent/annonce.html")







def agent_profile(request):
    prof = Profile.objects.get(user = request.user)
    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(prof.image_profile) > 0:
                os.remove(prof.image_profile.path)
                prof.image_profile = request.FILES['image_profile ']
            prof.nom = request.POST.get('nom')
            prof.prenom = request.POST.get('prenom')
            prof.raison = request.POST.get('raison')
            prof.telephone = request.POST.get('telephone')
            prof.sexe = request.POST.get('sexe')
            prof.ville = request.POST.get('ville')
            prof.quartier = request.POST.get('quartier')
            prof.save()
        
        else:
            prof.image_profile = '1'
            prof.nom = request.POST.get('nom')
            prof.prenom = request.POST.get('prenom')
            prof.raison = request.POST.get('raison')
            prof.telephone = request.POST.get('telephone')
            prof.sexe = request.POST.get('sexe')
            prof.ville = request.POST.get('ville')
            prof.quartier = request.POST.get('quartier')
            prof.save()
                    
        return redirect('/agent_profile')

    return render(request, 'agent/agent_profile.html')

def update_profile(request):
    return render(request, 'agent/update_profile.html')



def add_blog(request):
    
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        
        for image in images:
            blog = Blog.objects.create(
                titre=data['titre'],
                contenu = data['contenu'],
                image=image,
                user = request.user
            )

        return redirect('add_blog')

    blog_list = Blog.objects.all().filter(user = request.user)
    context = {
        "blog_list" : blog_list
    }
    return render(request, 'agent/add_blog.html', context)

def blog_client(request):
    if request.method == 'POST':
        commentaire = request.POST.get("commentaire")
        blodid = request.POST.get("id")
        
        b = Blog.objects.get(id = blodid)
        comm = Commentaire.objects.create(user = request.user, commentaire = commentaire, blog = b)
        comm.save()
        
        return redirect('/blog_client')
    blog_list = Blog.objects.all()
    context = {
        "blog_list" : blog_list
    }
    return render(request, 'client/client_blog.html', context)

def detail_blog(request, myid):
    blog_list = Blog.objects.filter(id = myid)
    co = Commentaire.objects.filter(blog = myid)
    context = {
        "blog_list" : blog_list,
        'co' : co
    }
    return render(request, 'client/detail_blog.html', context)

def list_blog(request):
    
    if request.method == 'POST':
        commentaire = request.POST.get("commentaire")
        blodid = request.POST.get("id")
        
        b = Blog.objects.get(id = blodid)
        comm = Commentaire.objects.create(user = request.user, commentaire = commentaire, blog = b)
        comm.save()
        
        co = Commentaire.objects.filter(blog_id = blodid)
        context = {
        "co" : co
        }
        return redirect('/list_blog', context)

    blog_list = Blog.objects.all()
    
    context = {
        "blog_list" : blog_list
    }
    return render(request, 'agent/list_blog.html', context)

def delete_blog(request, myid):
    blog = Blog.objects.get(id = myid)
    blog.delete()
    return redirect('/add_blog')


def admin_index(request):
    util = Profile.objects.count()
        
    agent = Profile.objects.all().exclude(type = 2 ).exclude(type = 3).count()
    
    client = Profile.objects.all().exclude(type = 1).exclude(type = 3).count()
    
    pub = Bien.objects.count()
    context = {
        "client" : client,
        "agent" : agent,
        "util" : util,
        "pub" : pub
    }
    
    return render(request, 'admin/admin_index.html', context)


def admin_client(request):
    
    client = Profile.objects.raw("select * from account_profile where type=2")
    context = {
        "client" : client
    }
    return render(request, 'admin/admin_client.html', context)


def admin_agent(request):
    agent = Profile.objects.raw("select * from account_profile where type=1")
    context = {
        "agent" : agent
    }
    return render(request, 'admin/admin_agent.html', context)

def venu_pdf(request):
    
    buf = io.BytesIO()
    
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    
    textob = c.beginText()
    
    textob.setTextOrigin(inch, inch)
    
    textob.setFont("Helvetica", 14)    
    venus = Profile.objects.all()
    
    lines = []
    
    for venu in venus:
        lines.append(str(venu.id))
        lines.append(venu.nom)
        lines.append(venu.prenom)
        lines.append(venu.user.email)
        lines.append(venu.user.username)
        lines.append(venu.telephone)
        lines.append("*****************")

    for line in lines:
        textob.textLine(line)  
          
    c.drawText(textob)
    
    c.showPage()
    
    c.save()
    
    buf.seek(0)
    
    return FileResponse(buf, as_attachment=True, filename="client.pdf" )


def client_excel(request):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="client.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nom', 'Prenom', 'username', 'Adresse email', 'ville' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # rows = Profile.objects.all().values_list('nom', 'prenom', 'profile.user.username', 'ville')
    rows = Profile.objects.all().values_list('nom', 'prenom', 'user__email' )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response
    
    



def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'First Name', 'Last Name', 'Email Address',  ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


def admin_profile(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        ville = request.POST.get('ville')
        quartier = request.POST.get('quartier')
        telephone = request.POST.get('telephone')
        image = request.FILES.get('profile')

        
        print(nom, prenom)
        prof = Profile.objects.update(nom = nom, prenom = prenom, telephone = telephone, ville = ville, quartier=quartier, image_profile = image)
        return redirect('/admin_profile')
    return render(request, 'admin/admin_profile.html')


def user_logout(request):
    logout(request)
    return redirect('/')

def message(request):
    message = Messages.objects.all()
    context = {
        "message" : message,
    }
    return render(request, 'client/client_message.html', context)

def detail_message(request, recepteur):
    recepteur = Messages.objects.filter(recepteur = recepteur)
    message = Messages.objects.all()
    context = {
        "recepteur" : recepteur,
        "message" : message,

    }
    return render(request, 'client/detail_message.html', context)


def agent_demande(request):
    demande_list = Demandes.objects.all()
    context = {
        "demande_list" : demande_list
    }
    return render(request, "agent/agent_demande.html", context)