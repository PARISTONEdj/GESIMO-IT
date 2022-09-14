from os import name
from xml.dom.minidom import Document
from django.urls import path, include
from .views import annonce, delete_bien, nav, acceuil, detail, vente, location, agent_index, client_index, client_demande, delete_demande, annonce, publication, agent_profile, update_profile, add_blog, list_blog, admin_index, admin_agent, admin_client, venu_pdf, export_users_xls, client_excel, admin_profile, delete_bien, detail_bien, update_bien, user_logout, message, detail_message, agent_demande, rech, delete_blog, rech_bien, blog_client, detail_blog



urlpatterns = [
    path('nav' , nav , name="nav"),
    path('', acceuil, name="acceuil"),
    path('vente', vente, name="vente"),
    path('location', location, name="location"),
    path('detail/<int:myid>/', detail, name="detail"),
    
    path('agent_index', agent_index, name="agent_index"),
    path('client_index', client_index, name="client_index"),
    path('client_demande', client_demande, name="client_demande"),
    path('delete_demande/<int:myid>/', delete_demande, name="delete_demande"),
    path('message', message, name="message"),
    path('detail_message/((?P<recepteur>.+)/)?$/', detail_message, name="detail_message"),
    path('rech_bien', rech_bien, name="rech_bien"),
    path('blog_client', blog_client, name="blog_client"),
    path('detail_blog/<int:myid>/', detail_blog, name='detail_blog'),

    
    path('delete_bien/<int:myid>/', delete_bien, name="delete_bien"),
    path('annonce', annonce, name="annonce"),
    path("publication", publication, name="publication"),
    path("detail_bien/<int:myid>/", detail_bien, name="detail_bien"),
    path("update_bien/<int:myid>/", update_bien, name="update_bien"),
    path("agent_demande", agent_demande, name="agent_demande"),
    path("rech", rech, name="rech"),
    
    
    path("agent_profile", agent_profile, name="agent_profile" ),
    path("update_profile", update_profile, name='update_profile'),
    path('add_blog', add_blog, name="add_blog"),
    path('list_blog', list_blog, name="list_blog" ),
    path('delete_blog/<int:myid>/', delete_blog, name="delete_blog"),
    
    
    path('admin_index', admin_index, name="admin_index"),
    path('admin_agent', admin_agent, name="admin_agent"),
    path('admin_client', admin_client, name="admin_client"),
    path('venu_pdf', venu_pdf, name='venu_pdf'),
    path('client_exel', client_excel, name='client_excel'),
    path('export_users_xls', export_users_xls, name="export_users_xls"),
    path('admin_profile', admin_profile, name="admin_profile"),
    
    path("logout", user_logout, name="logout")

] 

