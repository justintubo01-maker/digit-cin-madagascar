# cin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- Photo 1 : Portail d'accueil ---
    path('', views.index_portail, name='index_portail'),

    # À ajouter dans le urlpatterns de cin/urls.py
    path('connexion/<str:espace>/', views.connexion_view, name='connexion_espace'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),

    # --- Photos 2, 3, 4 : Espace Saisie ---
    path('saisie/connexion/', views.connexion_saisie, name='connexion_saisie'),
    path('saisie/dashboard/', views.dashboard_saisie, name='dashboard_saisie'),
    path('saisie/nouvelle/', views.nouvelle_demande, name='nouvelle_demande'),

    # --- Photos 5, 6, 7 : Espace Validation ---
    path('validation/connexion/', views.connexion_validation, name='connexion_validation'),
    path('validation/dashboard/', views.dashboard_validation, name='dashboard_validation'),
    path('validation/instruction/<int:pk>/', views.instruction_demande, name='instruction_demande'),

    # --- Espace Impression (Créé sur mesure) ---
    path('impression/connexion/', views.connexion_impression, name='connexion_impression'),
    path('impression/dashboard/', views.dashboard_impression, name='dashboard_impression'),
    path('impression/marquer-imprime/<int:pk>/', views.marquer_comme_imprime, name='marquer_comme_imprime'),
    
    # Déconnexion globale
    path('deconnexion/', views.deconnexion_utilisateur, name='deconnexion'),

    # À ajouter dans cin/urls.py
    path('impression/dashboard/', views.dashboard_impression, name='dashboard_impression'),
    path('impression/imprimer/<int:pk>/', views.imprimer_carte, name='imprimer_carte'),

    # À ajouter dans cin/urls.py
    path('saisie/modifier/<int:pk>/', views.modifier_demande, name='modifier_demande'),
    path('saisie/supprimer/<int:pk>/', views.supprimer_demande, name='supprimer_demande'),
]