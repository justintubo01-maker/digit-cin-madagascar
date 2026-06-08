# cin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import DemandeCIN
from django.http import HttpResponseForbidden

# ==========================================
# PHOTO 1 : PORTAIL GENERAL
# ==========================================
def index_portail(render_request):
    return render(render_request, 'cin/portail.html')

# ==========================================
# ESPACE SAISIE (Photos 2, 3, 4)
# ==========================================
def connexion_saisie(render_request):
    # Logique de connexion simplifiée pour l'instant
    return render(render_request, 'cin/saisie_connexion.html')


@login_required(login_url='/connexion/saisie/')
def dashboard_saisie(request):
    if not request.user.groups.filter(name='Saisie').exists() and not request.user.is_superuser:
        return HttpResponseForbidden("Accès interdit : Cet espace est réservé uniquement aux agents de SAISIE.")
    
    toutes_les_demandes = DemandeCIN.objects.all()
    context = {
        'demandes': toutes_les_demandes,
        'total': toutes_les_demandes.count(),
        'en_attente': DemandeCIN.objects.filter(statut='EN_ATTENTE').count(),
        'approuvees': DemandeCIN.objects.filter(statut='APPROUVE').count(),
        'rejetees': DemandeCIN.objects.filter(statut='REJETE').count(),
    }
    return render(request, 'cin/saisie_dashboard.html', context)

# cin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import DemandeCIN

def nouvelle_demande(render_request):
    if render_request.method == 'POST':
        # 1. Récupération des données textuelles
        numero_cin = render_request.POST.get('numero_cin')
        sexe = render_request.POST.get('sexe')
        nom = render_request.POST.get('nom')
        prenom = render_request.POST.get('prenom')
        date_naissance = render_request.POST.get('date_naissance')
        lieu_naissance = render_request.POST.get('lieu_naissance')
        adresse = render_request.POST.get('adresse')
        telephone = render_request.POST.get('telephone')
        
        # 2. Récupération des fichiers (Uniquement Photo, Recto et Verso)
        photo_identite = render_request.FILES.get('photo_identite')
        scan_recto = render_request.FILES.get('scan_recto')
        scan_verso = render_request.FILES.get('scan_verso')
        
        # 3. Création de l'enregistrement en BDD
        DemandeCIN.objects.create(
            numero_cin=numero_cin, sexe=sexe, nom=nom, prenom=prenom,
            date_naissance=date_naissance, lieu_naissance=lieu_naissance,
            adresse=adresse, telephone=telephone,
            photo_identite=photo_identite, 
            scan_recto=scan_recto, scan_verso=scan_verso,
            statut='EN_ATTENTE'
        )
        
        # 4. Redirection selon le bouton cliqué
        bouton_clique = render_request.POST.get('action_bouton')
        if bouton_clique == 'enregistrer_rester':
            return redirect('nouvelle_demande')
        else:
            return redirect('dashboard_saisie')
        
    return render(render_request, 'cin/saisie_formulaire.html')

# ==========================================
# ESPACE VALIDATION (Photos 5, 6, 7)
# ==========================================
def connexion_validation(render_request):
    return render(render_request, 'cin/validation_connexion.html')

@login_required(login_url='/connexion/validation/')
def dashboard_validation(request):
    if not request.user.groups.filter(name='Validation').exists() and not request.user.is_superuser:
        return HttpResponseForbidden("Accès interdit : Cet espace est réservé uniquement aux contrôleurs de VALIDATION.")
    
    demandes = DemandeCIN.objects.filter(statut='EN_ATTENTE')
    return render(request, 'cin/validation_dashboard.html', {'demandes': demandes})

# cin/views.py

def instruction_demande(render_request, pk):
    demande = get_object_or_404(DemandeCIN, pk=pk)
    
    if render_request.method == 'POST':
        decision = render_request.POST.get('action_decision')
        
        if decision == 'valider':
            demande.statut = 'APPROUVE'
        elif decision == 'refuser':
            demande.statut = 'REJETE'
            
        demande.save()
        return redirect('dashboard_validation')
        
    return render(render_request, 'cin/validation_instruction.html', {'demande': demande})

# ==========================================
# ESPACE IMPRESSION (Création sur mesure)
# ==========================================
def connexion_impression(render_request):
    return render(render_request, 'cin/impression_connexion.html')

@login_required(login_url='/connexion/impression/')
def dashboard_impression(request):
    if not request.user.groups.filter(name='Impression').exists() and not request.user.is_superuser:
        return HttpResponseForbidden("Accès interdit : Cet espace est réservé uniquement aux opérateurs d'IMPRESSION.")
    
    demandes_a_imprimer = DemandeCIN.objects.filter(statut='APPROUVE')
    return render(request, 'cin/impression_dashboard.html', {'demandes': demandes_a_imprimer})

def marquer_comme_imprime(render_request, pk):
    demande = get_object_or_404(DemandeCIN, pk=pk)
    demande.statut = 'IMPRIME'
    demande.save()
    return redirect('dashboard_impression')

# ==========================================
# DECONNEXION GLOBAL
# ==========================================
def deconnexion_utilisateur(render_request):
    logout(render_request)
    return redirect('index_portail')


# À ajouter à la fin de cin/views.py

def dashboard_impression(render_request):
    # On ne récupère que les dossiers approuvés par la validation
    demandes_a_imprimer = DemandeCIN.objects.filter(statut='APPROUVE')
    return render(render_request, 'cin/impression_dashboard.html', {'demandes': demandes_a_imprimer})

def imprimer_carte(render_request, pk):
    demande = get_object_or_404(DemandeCIN, pk=pk)
    
    if render_request.method == 'POST':
        # Une fois imprimée, on peut changer son statut pour dire que c'est clos
        demande.statut = 'TERMINE'
        demande.save()
        return redirect('dashboard_impression')
        
    return render(render_request, 'cin/impression_carte.html', {'demande': demande})


    # À coller tout en bas de cin/views.py
from django.contrib.auth import authenticate, login, logout

def connexion_view(render_request, espace):
    erreur = None
    
    if render_request.method == 'POST':
        nom_util = render_request.POST.get('username')
        mot_passe = render_request.POST.get('password')
        
        # Django vérifie si l'utilisateur existe dans sa base de données
        user = authenticate(render_request, username=nom_util, password=mot_passe)
        
        if user is not None:
            # Si le mot de passe est bon, on connecte officiellement la session !
            login(render_request, user)
            
            # On redirige l'agent vers le bon tableau de bord selon l'espace choisi
            if espace == 'saisie':
                return redirect('dashboard_saisie')
            elif espace == 'validation':
                return redirect('dashboard_validation')
            elif espace == 'impression':
                return redirect('dashboard_impression')
        else:
            # Si les identifiants sont faux
            erreur = "Nom d'utilisateur ou mot de passe incorrect."
            
    return render(render_request, 'cin/connexion.html', {
        'espace': espace,
        'erreur': erreur
    })

def deconnexion_view(render_request):
    # On ferme la session Django
    logout(render_request)
    # On renvoie l'utilisateur sur le portail d'accueil général
    return redirect('index_portail')


    # À ajouter à la fin de cin/views.py

@login_required(login_url='/connexion/saisie/')
def modifier_demande(request, pk):
    demande = get_object_or_404(DemandeCIN, pk=pk)
    
    if request.method == 'POST':
        demande.numero_cin = request.POST.get('numero_cin')
        demande.nom = request.POST.get('nom')
        demande.prenom = request.POST.get('prenom')
        demande.telephone = request.POST.get('telephone')
        
        # Si de nouveaux fichiers sont soumis, on les met à jour
        if request.FILES.get('photo_identite'):
            demande.photo_identite = request.FILES.get('photo_identite')
            
        # On repasse automatiquement le dossier en attente si l'agent l'a corrigé
        demande.statut = 'EN_ATTENTE'
        demande.save()
        return redirect('dashboard_saisie')
        
    return render(request, 'cin/modifier_formulaire.html', {'demande': demande})

@login_required(login_url='/connexion/saisie/')
def supprimer_demande(request, pk):
    demande = get_object_or_404(DemandeCIN, pk=pk)
    demande.delete() # Supprime définitivement la ligne de la BDD
    return redirect('dashboard_saisie')

# Create your views here.
