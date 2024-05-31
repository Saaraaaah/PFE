from django.http import HttpResponse ,HttpResponseRedirect  #fournit des utilitaires pour gérer les requêtes et les réponses HTTP.
from django.shortcuts import render,redirect
import folium
from folium import TileLayer     #bibliothèque principale pour créer des cartes Web interactives.
from core.models import Djezzy, Posta,Mobilis,Ooredoo2,Algerie_Telecom,Service_Universel  #importe des modèles
from folium.plugins import MarkerCluster, Fullscreen, LocateControl, Geocoder #classes des plugins folium pour ajouter des fonctionnalités telles que des calques
import geopandas as gpd #bibliothèque permettant de travailler avec des données géospatiales dans des trames de données de type pandas.
import random #utilisé pour générer des couleurs aléatoires dans le code.
from django.contrib.auth import authenticate,login,logout #Fournit des fonctions d'authentification des utilisateurs (connexion, déconnexion).
from django.contrib.auth.models import User #importe le modèle User pour la gestion des utilisateurs.
from folium.plugins import MousePosition ,MiniMap,MeasureControl #plugins supplémentaires pour afficher la position de la souris
from geopy.distance import distance ,geodesic
from django.template.loader import render_to_string
from folium.plugins import Draw
from folium.plugins import Search

##################################################################################################


def api_view(request):
   
 
    return render(request, 'sss.html')


def homePage(request):
	return render(request,'index.html')

##################################################################################################


def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        


        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    
    return render(request, 'signup.html')


##################################################################################################

def LoginPage(request):
    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['pass']
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/index')
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request,'login.html')



##################################################################################################


def LogoutPage(request):
    logout(request)
    return redirect('login')



##################################################################################################
# Create your views here.
    
def choose_cat(cat):
    if cat=='posta':
        return Posta.objects.all()
    elif cat=='Mobilis':
        return Mobilis.objects.all()
    elif cat=='Algerie_Telecom':
        return Algerie_Telecom.objects.all()
    
def testfunc(request):  

    if request.method == 'POST':
        location_key =  request.POST.get('location_option')
        categories= choose_cat(location_key)
        print(location_key)
       
   
        location =  float(36.2034), float(3.8106)
        location2 = float(36.7624192), float(3.445690)
        shortest=99999999999
        for category in categories:
        
            if category.latitude and category.longitude:
                desired_location = float(category.latitude), float(category.longitude)
                d= int(distance(location, desired_location).km)
                if d < shortest:
                    shortest =  d
                    location2 = float(category.latitude), float(category.longitude)

          
            

        # create a Folium map centred at the above location
        map=folium.Map(location=[36.1867,3.8480],zoom_start=10, control_scale=True, width=1100, height=600)
        # add marker at the locations
        folium.Marker(location, popup="me").add_to(map)
        folium.Marker(location2, popup="destination").add_to(map)

        # add line between points
        folium.PolyLine((location,location2)).add_to(map)

        folium.LayerControl(position='topleft').add_to(map)
        Fullscreen().add_to(map)
        LocateControl().add_to(map)
        Geocoder().add_to(map)
        folium.LatLngPopup().add_to(map)

        map = map._repr_html_()

        context = {
            'map': map
        } 


        return render  (request,"index.html",context)
    else:

        # create a Folium map centred at the above location
        map=folium.Map(location=[36.1867,3.8480],zoom_start=10, control_scale=True, width=1100, height=600)
        # add marker at the locations
      

        folium.LayerControl(position='topleft').add_to(map)
        Fullscreen().add_to(map)
        LocateControl().add_to(map)
        Geocoder().add_to(map)
        folium.LatLngPopup().add_to(map)

        map = map._repr_html_()

        context = {
            'map': map
        } 


        return render  (request,"index.html",context)
##################################################################################################


#Fonction pour générer une couleur de remplissage aléatoire pour les zones
def get_zone_color(x):
    r = lambda: random.randint(0,255) # Générer un nombre aléatoire entre 0 et 255 (valeurs RVB)
    fill_color = '#%02X%02X%02X' % (r(),r(),r()) # Formater le code couleur
# Définir les styles de couleur de remplissage et de ligne
    style={'fillColor':fill_color,
           'lineColor':'#c9d91e'
           }
    return style

blue_tile = TileLayer(
         tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
         attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
         name='Blue Map',
         overlay=True,
         opacity=0.7
    )
def generate_map(latitude=36.1867,logitude=3.8480,start_point=None,end_point=None,data_route=None,message_start_point='Your Current',message_end_point='end point', zoom_start=10,width=1100,height=600,print=False):
        midpoint=None
        if start_point and end_point and data_route:
    # Créez la carte de base centrée sur des coordonnées spécifiques avec le niveau de zoom et le contrôle de l'échelle
            midpoint_lat = (float(start_point[0]) + float(end_point[0])) / 2
            midpoint_lon = (float(start_point[1]) + float(end_point[1])) / 2
            midpoint = (midpoint_lat, midpoint_lon)
        
        if print == True:
            map=folium.Map(location= midpoint if midpoint is not None else [latitude,logitude],zoom_control=False,zoom_start=zoom_start,control_scale=False,  width=width, height=height)
        else:
            
            map=folium.Map(location= midpoint if midpoint is not None else [latitude,logitude],zoom_control=True,zoom_start=zoom_start,control_scale=True,  width=width, height=height)
            Draw(export=True).add_to(map)
            MousePosition().add_to(map)
            MiniMap(toggle_display=True).add_to(map)
            map.add_child(MeasureControl())
            
            Fullscreen().add_to(map)
            LocateControl().add_to(map)
            Geocoder().add_to(map)
            js=gpd.read_file("DZA_adm2.geojson")  # Charger les données des limites administratives à partir du fichier GeoJSON
            style={'fillColor':'#FF0000',          # Définir les styles par défaut pour les limites
            'lineColor':'#c9d91e'
            }
            js=folium.GeoJson(    # Créez une couche GeoJSON avec des informations de style et d'info-bulle
                        js,
                        name="Limite administrative de Bouira ", # Définir le nom de la couche (« Limite administrative de Bouira »)
                        style_function=lambda x:get_zone_color(x), # Appliquer la fonction de couleur de remplissage aléatoire
                        tooltip=folium.GeoJsonTooltip(
                        fields=["ID_0", "ISO", "NAME_0","ID_1","NAME_1","ID_2","NAME_2", "TYPE_2","ENGTYPE_2","NL_NAME_2","VARNAME_2"],
                        aliases=["ID_0", "ISO", "NAME_0","ID_1","NAME_1","ID_2","NAME_2", "TYPE_2","ENGTYPE_2","NL_NAME_2","VARNAME_2"],
                        localize=True
                        )).add_to(map) 
            citysearch = Search(
            layer=js,
            geom_type="Point",
            placeholder="Search for a US City",
            collapsed=True,
            search_label="NAME_2",
            ).add_to(map)
            
            
            
# Ajoutez des fonctionnalités conviviales : position de la souris, mini-carte et contrôle des mesures,draw





##################################################################################################




 ##################################################################################################

 

        bordersStyle = {
        "color": "black",  # Use colon 🙂) after each key
        "weight": "2",
        "fillColor" : "red" ,
        "fillOpacity": "0.1",
    
        }
   

        folium.GeoJson(   
                        "DZA_adm0.geojson",
                        name="Pays_Algerie", 
                        style_function=lambda x:bordersStyle,
                        tooltip=folium.GeoJsonTooltip(
                        fields=["ID_0", "ISO", "NAME_0"],
                        aliases=["ID_0", "ISO", "NAME_0"],
                        localize=True
                        )).add_to(map)
        # Add a second TileLayer to the basemap
        folium.TileLayer('OpenStreetMap').add_to(map)
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='<a href="https://www.google.com/maps">Google Maps</a>',
            name='Google Satellite',
            overlay=True  # Mark Google Satellite as overlay by default
        ).add_to(map)
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='<a href="https://www.google.com/maps">Google Maps</a>',
            name='Google Maps',  # Change name to 'Google Maps'
            overlay=True  # Mark Google Maps as overlay by default
        ).add_to(map)
    ##################################################################################################
    ##################################################################################################
    ##################################################################################################
    #Add Service_Universel Data
        obj3=Service_Universel.objects.all()
        service_universal = folium.FeatureGroup(name='service_universal', show=False).add_to(map)
        circle_radius = 100  # Meters
        marker_cluster = MarkerCluster()
        for e in obj3:
            locations = [e.latitude, e.longitude]
            marker_cluster.add_child(
                folium.Circle(
                    location=locations,
                    radius=circle_radius,
                    color='#3388ff',
                    fill=True,
                    fill_color='#3388ff',
                    fill_opacity=0.4,
                    tooltip="localité:" +str(e.localité),
                    popup= folium.Popup(f"""
                    <img src="http://localhost:8000/static/images/.png" style="text-align:center;width:100px;" alt="My image">                    
                    <table>
                        <tbody>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LOCALITÉ:</td>
                                <td style="padding:1rem;">{str(e.localité)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Latitude:</td>
                                <td style="padding:1rem;">{str(e.latitude)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Longitude:</td>
                                <td style="padding:1rem;">{str(e.longitude)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Populations:</td>
                                <td style="padding:1rem;">{str(e.populations)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">البلدية:</td>
                                <td style="padding:1rem;">{str(e.municipality)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">المنطقة:</td>
                                <td style="padding:1rem;">{str(e.region)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">COMMUNE:</td>
                                <td style="padding:1rem;">{str(e.commune)}</td>
                            </tr>
                        </tbody>
                    </table>           
                    """)

                )
        
            ).add_to(service_universal)
    ##################################################################################################
    #Add Algerie_Telecom Data
        obj0=Algerie_Telecom.objects.all()
        algerie_Telecom = folium.FeatureGroup(name='algerie_Telecom', show=False).add_to(map)
        marker_cluster = MarkerCluster()
        for j in obj0:
            locations = [j.latitude, j.longitude]
            marker_cluster.add_child(
                folium.Marker(
                    locations,
                    icon=folium.features.CustomIcon("./img/at.png",icon_size=(40,40)),
                    tooltip="adresse_site:" +str(j.adresse_site),
                    popup= folium.Popup(f"""
                    <img src="http://localhost:8000/static/images/at.png" style="text-align:center;width:100px;" alt="My image">                    
                    <table>
                        <tbody>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">adresse site:</td>
                                <td style="padding:1rem;">{str(j.adresse_site)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LATITUDE:</td>
                                <td style="padding:1rem;">{str(j.latitude)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LONGITUDE:</td>
                                <td style="padding:1rem;">{str(j.longitude)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">commune:</td>
                                <td style="padding:1rem;">{str(j.commune)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">TYPE d'equipement d'acces (LTE):</td>
                                <td style="padding:1rem;">{str(j.type)}</td>
                            </tr>
                        </tbody>
                    </table>           
                    """)
                
                
                )
            ).add_to(algerie_Telecom)
    ##################################################################################################
    # Récupérer les données posta de la base de données
        libraries = Posta.objects.all()
        Les_Bureaux_de_Postes  = folium.FeatureGroup(name='Les Bureaux de Postes', show=False).add_to(map)
        marker_cluster = MarkerCluster()
        for library in libraries:
            locations = [library.latitude, library.longitude]
            marker_cluster.add_child(
                folium.Marker(

                    locations,
                # markers with apply function
                    
                    icon=folium.features.CustomIcon("./img/ap.png",icon_size=(40,40)),
                    tooltip="Library Name:" +str(library.commune),
                    popup= folium.Popup(f"""
                    <img src="http://localhost:8000/static/images/ap.png" style="text-align:center;width:100px;" alt="My image">                    
                    <table>
                        <tbody>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LONGITUDE:</td>
                                <td style="padding:1rem;">{str(library.longitude)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LATITUDE:</td>
                                <td style="padding:1rem;">{str(library.latitude)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">dénomination du bureau de poste:</td>
                                <td style="padding:1rem;">{str(library.dénomination)}</td>
                            </tr>
                        
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">COMMUNE:</td>
                                <td style="padding:1rem;">{str(library.commune)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Classe:</td>
                                <td style="padding:1rem;">{str(library.Classe)}</td>
                            </tr>
                            
                        </tbody>
                    </table>           
                    """)
                )
            ).add_to(Les_Bureaux_de_Postes )
    ##################################################################################################
     # Récupérer les données ooredoo de la base de données
        obj =Ooredoo2.objects.all()
        ooredoo = folium.FeatureGroup(name='ooredoo', show=False).add_to(map)
        marker_cluster = MarkerCluster()
        for i in obj:
            locations = [i.latitude, i.longitude]
            marker_cluster.add_child(
                folium.Marker(
                    locations,
                    #i.location.coords,
                    icon=folium.features.CustomIcon("./img/ooredoo.png",icon_size=(40,40)),
                    tooltip="Commune:" +str(i.commune),
                    popup= folium.Popup(f"""
                    <img src="http://localhost:8000/static/images/ooredoo.png" style="text-align:center;width:100px;" alt="My image">                    
                    <table>
                        <tbody>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Commune:</td>
                                <td style="padding:1rem;">{str(i.commune)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Code Site:</td>
                                <td style="padding:1rem;">{str(i.code_site)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Type:</td>
                                <td style="padding:1rem;">{str(i.type)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Adresse:</td>
                                <td style="padding:1rem;">{str(i.adresse)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Wilaya:</td>
                                <td style="padding:1rem;">{str(i.wilaya)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Mise en service:</td>
                                <td style="padding:1rem;">{str(i.mise_en_service)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LATITUDE:</td>
                                <td style="padding:1rem;">{str(i.latitude)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LONGITUDE:</td>
                                <td style="padding:1rem;">{str(i.longitude)}</td>
                            </tr>
    
                        </tbody>
                    </table>           
                    """)
                            #<tr>
                            #   <td style="background:red;color:white;padding:1rem;">Latitude:</td>
                            #  <td style="padding:1rem;">{str(i.latitude)}</td>
                        # </tr>
                )
            ).add_to(ooredoo)
    ##################################################################################################
     # Récupérer les données Mobilis de la base de données
        librarie = Mobilis.objects.all()
        mobilis = folium.FeatureGroup(name='mobilis', show=False).add_to(map)
        marker_cluster = MarkerCluster()
        for k in librarie:
            locations = [k.latitude, k.longitude]
            marker_cluster.add_child(
                folium.Marker(

                    locations,
                # markers with apply function
                    
                    icon=folium.features.CustomIcon("./img/mobilis.png",icon_size=(80, 80)),
                    tooltip="Library Name:" +str(k.Nom_du_Site),
                    popup= folium.Popup(f"""
                    <img src="http://localhost:8000/static/images/mobilis.png" style="text-align:center;width:100px;" alt="My image">
                    <table>
                        <tbody>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Nom du Site:</td>
                                <td style="padding:1rem;">{str(k.Nom_du_Site)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;"> Code Site:</td>
                                <td style="padding:1rem;">{str(k.Code_Site)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Type:</td>
                                <td style="padding:1rem;">{str(k.Type)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Typologie :</td>
                                <td style="padding:1rem;">{str(k.Typologie )}</td>
                            </tr>
        
                        
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Commune:</td>
                                <td style="padding:1rem;">{str(k.Commune)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Surface du Site (M²):</td>
                                <td style="padding:1rem;">{str(k.T_Salle_Equip)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Propriétaire:</td>
                                <td style="padding:1rem;">{str(k.Propriétaire)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Etat:</td>
                                <td style="padding:1rem;">{str(k.Etat)}</td>
                            </tr>
                        
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Type Gardiennage:</td>
                                <td style="padding:1rem;">{str(k.Type_Gardiennage)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">T_Salle_Equip:</td>
                                <td style="padding:1rem;">{str(k.T_Salle_Equip)}</td>
                            </tr>

                        </tbody>
                    </table>           
                    """)
                )
            ).add_to(mobilis)
    ##################################################################################################
    # Récupérer les données Djezzy de la base de données
        librarie = Djezzy.objects.all()
        djezzy = folium.FeatureGroup(name='djezzy', show=False).add_to(map)
        marker_cluster = MarkerCluster()
        for a in librarie:
            locations = [a.latitude, a.longitude]
            marker_cluster.add_child(
                folium.Marker(

                    locations,
                # markers with apply function
                    
                    icon=folium.features.CustomIcon("./img/djezzy.png",icon_size=(80, 80)),
                    tooltip="Adresse:" +str(a.Adresse),

                    popup= folium.Popup(f"""
                                        <img src="http://localhost:8000/static/images/djezzy.png" style="text-align:center;width:100px;" alt="My image">
                    <table>
                        <tbody>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Adresse:</td>
                                <td style="padding:1rem;">{str(a.Adresse)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LATITUDE:</td>
                                <td style="padding:1rem;">{str(a.latitude )}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">LONGITUDE:</td>
                                <td style="padding:1rem;">{str(a.longitude)}</td>
                            </tr>
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Commune:</td>
                                <td style="padding:1rem;">{str(a.commune)}</td>
                            </tr>
                        
                            <tr>
                                <td style="background:red;color:white;padding:1rem;">Technologie:</td>
                                <td style="padding:1rem;">{str(a.Technologie)}</td>
                            </tr>
                                        
                        </tbody>
                    </table>           
                    """)
                )
            ).add_to(djezzy)
    ##################################################################################################
        if start_point and end_point and data_route:
                folium.features.GeoJson(data=data_route).add_to(map)
                folium.Marker(location=start_point, popup=message_start_point, icon=folium.Icon(color="green")).add_to(map)
                folium.Marker(location=end_point, popup=message_end_point, icon=folium.Icon(color="red")).add_to(map)

        
        
        if print!=True:
            folium.LayerControl(position='topleft').add_to(map)
        folium.LatLngPopup().add_to(map)
        return map._repr_html_()
def get_less_rout(request):
    if request.method=='POST':
        _type=request.POST.get('location_option')
        if _type=='posta':
            query=Posta.objects.all()
        elif _type =='Mobilis':
            query=Mobilis.objects.all()
        elif _type == 'Algerie_Telecom':
             query=Algerie_Telecom.objects.all()  

        
        
        
        
        
        import requests
        distances = []
        current_latitude=request.POST.get('latitude')
        current_longitude=request.POST.get('longitude')
        posta=Posta.objects.all()
        for po in posta:
            direct_distance = geodesic((current_latitude,current_longitude), (po.latitude,po.longitude)).kilometers
            distances.append((po,direct_distance))
        Sorted_des=sorted(distances,key=lambda x: x[1])
        lest_3_direct_destanc=Sorted_des[3:]
        routs=[]
        for ro,des in lest_3_direct_destanc :
            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{current_longitude},{current_latitude};{ro.longitude},{ro.latitude}?steps=true&geometries=geojson"
            response = requests.get(osrm_url)
            end_point=(ro.latitude,ro.longitude)
            data = response.json()
            if 'routes' in data and len(data['routes']) > 0:
                route_distance = data['routes'][0]['distance']   
                routs.append((data,route_distance,end_point))
        less_ruot=min(routs, key=lambda x: x[1])
        data_route= less_ruot[0]['routes'][0]['geometry']
        start_point=(current_latitude,current_longitude)
        end_point=less_ruot[2]
        map=generate_map(print=False,start_point=start_point,end_point=end_point,data_route=data_route)
        

        context = {
        'map': map
        }
    
        return render(request, 'index.html', context)
    return HttpResponse('errore')
    
    return 


def index(request):

    map= generate_map(print=False)

    context = {
        'map': map
    }
    
    return render(request, 'index.html', context)

#def new_func(map):
 #   map.create_map(path='osm.html')