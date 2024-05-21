from django.db import models
from django.contrib.gis.db import models as geo_models



# Create your models here.
class Posta(models.Model):
   # station_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    dénomination = models.CharField(max_length=250)
    
    commune = models.CharField(max_length=250)
    Classe = models.CharField(max_length=250)
  #  code =models.FloatField()

    def __str__(self):
        return self.commune
    
#nsyo
class Mobilis(models.Model):
    Nom_du_Site = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    Code_Site = models.CharField(max_length=250)
    Type = models.CharField(max_length=250)
    Typologie = models.CharField(max_length=250)
 
    T_Salle_Equip = models.CharField(max_length=250)
   
    Type_Gardiennage = models.CharField(max_length=250)
    Commune = models.CharField(max_length=250)
    Etat = models.CharField(max_length=250)
    D_Mise_en_Air = models.DateField(null=True)
    Propriétaire = models.CharField(max_length=250)

    def __str__(self):
        return self.Nom_du_Site
    
class Ooredoo2(geo_models.Model):
      commune=geo_models.CharField(max_length=250)
      #location = geo_models.PointField()
      latitude = models.FloatField()
      longitude = models.FloatField()
      code_site = geo_models.CharField(max_length=100)
      type = geo_models.CharField(max_length=100)
      adresse = geo_models.TextField()
      wilaya = geo_models.CharField(max_length=100)
      mise_en_service = geo_models.DateField()

      def __str__(self):
          return self.commune
      
class Algerie_Telecom(models.Model):  
    adresse_site= models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    commune= models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    def __str__(self):
          return self.adresse_site


class Djezzy(models.Model):
    Adresse= models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    commune= models.CharField(max_length=250)
  #  Date = models.DateField(null=True)
    Technologie = models.CharField(max_length=250)

  

    def __str__(self):
         return self.Adresse
          

class  Service_Universel(models.Model):
     localité= models.CharField(max_length=250)
     latitude = models.FloatField()
     longitude = models.FloatField()
     populations=models.CharField(max_length=250)
     municipality = models.CharField(max_length=255, blank=True, null=True)
     region = models.CharField(max_length=255, blank=True, null=True)
     commune = models.CharField(max_length=250)
     def __str__(self):
         return self.localité