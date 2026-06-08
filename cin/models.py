from django.db import models
from django.contrib.auth.models import User

class DemandeCIN(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente de validation'),
        ('APPROUVE', 'Approuvé (À imprimer)'),
        ('REJETE', 'En attente de modification'),
        ('IMPRIME', 'Imprimé'),
    ]

    # --- Informations Textuelles (Photo 4) ---
    numero_cin = models.CharField(max_length=12, unique=True, verbose_name="Numéro de CIN")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom(s)")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    adresse = models.TextField(verbose_name="Adresse")
    nom_complet_pere = models.CharField(max_length=255, verbose_name="Nom complet du père", blank=True,null=True)
    nom_complet_mere = models.CharField(max_length=255, verbose_name="Nom complet de la mère", blank=True,null=True)
    est_duplicata = models.BooleanField(default=False, verbose_name="C'est un duplicata")
    telephone = models.CharField(max_length=15, verbose_name="Numéro de téléphone")

    # --- Fichiers Numérisés / Images (Photo 4) ---
    photo_identite = models.ImageField(upload_to='photos_identite/', verbose_name="Photo d'identité")
    scan_recto = models.ImageField(upload_to='scans_recto/', verbose_name="Fichier image Recto")
    scan_verso = models.ImageField(upload_to='scans_verso/', verbose_name="Fichier image Verso")

    # --- Suivi Métier & Statuts (Photos 3, 6, 7) ---
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name="Statut du dossier")
    
    # Traçabilité des opérateurs
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cin_saisies')
    valide_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cin_validees')
    
    # Dates de suivi
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de dépôt")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Demande de CIN"
        verbose_name_plural = "Demandes de CIN"
        ordering = ['-date_creation']

    def __str__(self):
        type_demande = "Duplicata" if self.est_duplicata else "Première demande"
        return f"CIN de {self.nom} {self.prenom} ({type_demande})"
# Create your models here.
