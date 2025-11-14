import maya.cmds as cmds
import random
import math
  
#Géneration de ville de temple aléatoire
RAYON_BASE = 30
RADIUS_MULTIPLIER = 0.6
SPACING_MARGIN = 1

# RAYON_BASE: distance de base entre les cercles de temples
# RADIUS_MULTIPLIER: multiplicateur appliqué à la somme des "rayons" des temples pour éviter le chevauchement
# SPACING_MARGIN: marge additionnelle minimale entre temples

# TEMPLES
def creer_temple_maya(nom, taille=5):
    niveaux = random.randint(3, 5)
    base = taille
    groupe = cmds.group(em=True, name=f"{nom}_temple_maya")

    # Étages pyramidaux
    for i in range(niveaux):
        largeur = base - (i * base / (niveaux + 1))
        hauteur = taille / niveaux
        cube = cmds.polyCube(w=largeur, h=hauteur, d=largeur, name=f"{nom}_etage_{i}")[0]
        cmds.move(0, i * hauteur + hauteur / 2, 0, cube)
        
        # Ajout de bordures décoratives
        cmds.select(cube + ".e[0:3]")
        cmds.polyBevel(offset=0.1, segments=2)
        
        cmds.parent(cube, groupe)


    # Temple au sommet
    hauteur_sommet = niveaux * (taille / niveaux)
    temple_sommet = cmds.polyCube(w=base * 0.3, h=taille * 0.3, d=base * 0.3)[0]
    cmds.move(0, hauteur_sommet + taille * 0.15, 0, temple_sommet)
    cmds.parent(temple_sommet, groupe)

    # Décoration aux coins de la base
    for x in [-base * 0.4, base * 0.4]:
        for z in [-base * 0.4, base * 0.4]:
            decoration = cmds.polyCube(w=0.3, h=taille * 0.4, d=0.3)[0]
            cmds.move(x, taille * 0.2, z, decoration)
            cmds.parent(decoration, groupe)

    return groupe


def creer_temple_grec(nom, taille=5):
    groupe = cmds.group(em=True, name=f"{nom}_temple_grec")

    base = cmds.polyCube(w=taille * 1.5, h=0.6, d=taille)[0]
    cmds.move(0, 0.3, 0, base)
    cmds.parent(base, groupe)

    corps = cmds.polyCube(w=taille, h=taille * 0.8, d=taille * 0.8)[0]
    cmds.move(0, taille * 0.4 + 0.3, 0, corps)
    cmds.parent(corps, groupe)

    colonnes = random.randint(6, 8)
    for i in range(colonnes):
        x = -taille * 0.6 + i * (taille * 1.2 / (colonnes - 1))
        for z in [-taille * 0.4, taille * 0.4]:
            colonne = cmds.polyCylinder(r=0.2, h=taille * 0.9, sa=16)[0]
            cmds.move(x, taille * 0.45, z, colonne)
            cmds.parent(colonne, groupe)

    toit = cmds.polyCube(w=taille * 1.6, h=0.3, d=taille * 1.1)[0]
    cmds.move(0, taille * 0.9 + 0.45, 0, toit)
    cmds.parent(toit, groupe)

    return groupe


def creer_temple_bouddhiste(nom, taille=5):
    # Reprise du temple TP1
    groupe = cmds.group(em=True, name=f"{nom}_temple_bouddhiste")

    # Socle
    socle = cmds.polyCube(w=20, d=15, h=1, n=f"{nom}_socle")[0]
    cmds.move(0, 0.5, 0, socle)
    cmds.parent(socle, groupe)

    # Colonnes
    positions_colonnes = [
        (-6, -4.5, 0.5), (6, -4.5, 0.5), (-6, 4.5, 0.5), (6, 4.5, 0.5),
        (-6, 0, 0.5), (6, 0, 0.5),
        (0, -4.5, 0.5), (0, 4.5, 0.5)
    ]
    for x, z, rayon in positions_colonnes:
        col = cmds.polyCylinder(r=rayon, h=6, n=f"{nom}_colonne")[0]
        cmds.move(x, 3.5, z, col)
        cmds.parent(col, groupe)

    # Corps principal avec trois portes
    corps = cmds.polyCube(w=12, d=8, h=6, n=f"{nom}_corps")[0]
    cmds.move(0, 3.5, 0, corps)
    for px in [-3.5, 0, 3.5]:
        porte = cmds.polyCube(w=3, d=4, h=5)[0]
        cmds.move(px, 4, 3.5, porte)
        corps = cmds.polyBoolOp(corps, porte, op=2)[0]
    cmds.parent(corps, groupe)

    # Toit principal
    toit = cmds.polyCube(w=14, d=10, h=0.5, n=f"{nom}_toit")[0]
    cmds.move(0, 7, 0, toit)
    cmds.select(toit + ".f[1]")
    cmds.polyExtrudeFacet(ltz=1, ls=(1.3, 1.5, 1))
    cmds.parent(toit, groupe)

    # Pagode supérieure
    hauteur = 11.2
    largeur_base = 1.2
    objets_pagode = []
    for i in range(6):
        largeur = largeur_base - i * 0.15
        toit_etage = cmds.polyCube(w=largeur, d=largeur, h=0.08)[0]
        cmds.move(0, hauteur, 0, toit_etage)
        cmds.select(toit_etage + ".f[1]")
        cmds.polyExtrudeFacet(ltz=0.12, ls=(1.3, 1.3, 1))
        objets_pagode.append(toit_etage)
        hauteur += 0.24
        cyl = cmds.polyCylinder(r=largeur * 0.25, h=0.32)[0]
        cmds.move(0, hauteur, 0, cyl)
        objets_pagode.append(cyl)
        hauteur += 0.24

    fleche = cmds.polyCone(r=0.16, h=0.48)[0]
    cmds.move(0, hauteur, 0, fleche)
    objets_pagode.append(fleche)
    pagode = cmds.polyUnite(objets_pagode, n=f"{nom}_pagode")[0]
    cmds.delete(pagode, ch=True)
    cmds.parent(pagode, groupe)

    # Escalier avant
    escalier = cmds.polyCube(w=20, d=15, h=1, n=f"{nom}_escalier")[0]
    cmds.move(0, 0.5, 8, escalier)
    cmds.scale(0.7, 0.8, 0.16, escalier)
    cmds.parent(escalier, groupe)

    # Toit arrondi
    cyl = cmds.polyCylinder(n=f"{nom}_toit_cyl", r=3.5, h=15, sa=3)[0]
    cmds.move(0, 10.5, 0, cyl)
    cmds.rotate(0, 0, 90, cyl)
    sph = cmds.polySphere(r=17, n=f"{nom}_toit_sph")[0]
    cmds.move(0, 28, 0, sph)
    toit_arrondi = cmds.polyBoolOp(cyl, sph, op=2, n=f"{nom}_toit_arrondi")[0]
    cmds.parent(toit_arrondi, groupe)

    cmds.move(0, 0, 0, groupe)
    return groupe


def creer_tour_simple(nom, taille=3):
    groupe = cmds.group(em=True, name=f"{nom}_tour_simple")
    
    # Base carrée
    base = cmds.polyCube(w=taille * 1.2, h=taille * 0.2, d=taille * 1.2)[0]
    cmds.move(0, taille * 0.1, 0, base)
    cmds.parent(base, groupe)
    
    # Corps principal
    hauteur_tour = taille * random.uniform(1.8, 2.8)
    rayon_tour = taille * 0.4
    corps = cmds.polyCylinder(r=rayon_tour, h=hauteur_tour, sa=12)[0]
    cmds.move(0, taille * 0.2 + hauteur_tour/2, 0, corps)
    cmds.parent(corps, groupe)
    
    # Fenêtres
    nb_niveaux = random.randint(2, 4)
    for niveau in range(nb_niveaux):
        hauteur_fenetre = taille * 0.2 + (niveau + 1) * hauteur_tour / (nb_niveaux + 1)
        
        # fenêtres par niveau
        nb_fenetres = random.randint(2, 4)
        for i in range(nb_fenetres):
            angle = (2 * math.pi / nb_fenetres) * i
            x_fenetre = rayon_tour * 0.9 * math.cos(angle)
            z_fenetre = rayon_tour * 0.9 * math.sin(angle)
            
            fenetre = cmds.polyCube(w=taille * 0.15, h=taille * 0.3, d=taille * 0.1)[0]
            cmds.move(x_fenetre, hauteur_fenetre, z_fenetre, fenetre)
            cmds.parent(fenetre, groupe)
    
    # Toit conique
    toit = cmds.polyCone(r=rayon_tour * 1.3, h=taille * 0.8)[0]
    cmds.move(0, taille * 0.2 + hauteur_tour + taille * 0.4, 0, toit)
    cmds.parent(toit, groupe)
    
    # Porte d'entrée
    porte = cmds.polyCube(w=taille * 0.3, h=taille * 0.6, d=taille * 0.1)[0]
    cmds.move(0, taille * 0.2 + taille * 0.3, rayon_tour, porte)
    cmds.parent(porte, groupe)
    
    return groupe


# POSITIONNEMENT ET GÉNÉRATION
def position_valide(x, z, taille, temples_existants, distance_min=10):
    # Vérifie qu'un nouveau temple ne chevauche pas les précédents.
    for tx, tz, ttaille in temples_existants:
        # Utiliser le multiplicateur et la marge pour définir la distance requise
        distance_requise = (taille + ttaille) * RADIUS_MULTIPLIER + distance_min + SPACING_MARGIN
        dist = math.sqrt((x - tx)**2 + (z - tz)**2)
        if dist < distance_requise:
            return False
    return True


def generer_ville_temple():
    # Génère plusieurs temples autour du centre du monde.

    #cmds.select(all=True) -> # Sélectionne TOUS les objets de la scène Maya
    #cmds.delete() -> # Supprime tout ce qui est sélectionné

    groupe_ville = cmds.group(em=True, name="ville_de_temples")

    types_temples = [
        creer_temple_maya,
        creer_temple_grec,
        creer_temple_bouddhiste,
        creer_tour_simple
    ]

    temples_existants = []

    cercles = 3
    rayon_base = RAYON_BASE
    # Variation aléatoire du nombre de temples par cercle
    temples_par_cercle = [
        random.randint(6, 10),
        random.randint(10, 15),
        random.randint(14, 20)
    ]

    # Temple central
    taille_centrale = 15

    # Probabilités pour le temple central plus variées
    type_central = random.choice(types_temples)
    nom_central = "temple_central"
    
    # Ajuster le nom selon le type choisi
    if type_central == creer_temple_maya:
        nom_central = "temple_central_maya"
    elif type_central == creer_temple_grec:
        nom_central = "temple_central_grec"
    elif type_central == creer_temple_bouddhiste:
        nom_central = "temple_central_bouddhiste"
    elif type_central == creer_tour_simple:
        nom_central = "temple_central_tour"
    
    temple_central = type_central(nom_central, taille_centrale)
    cmds.move(0, 0, 0, temple_central)
    cmds.parent(temple_central, groupe_ville)
    temples_existants.append((0, 0, taille_centrale))

    # Cercles de temples
    for c in range(cercles):
        rayon = rayon_base * (c + 1)
        nb = temples_par_cercle[c]
        angle_step = 2 * math.pi / nb

        for i in range(nb):
            # Probabilité aléatoire d'apparition de chaque temple (70-90% de chance)
            if random.random() > random.uniform(0.1, 0.3):
                # éviter des trous importants
                angle = i * angle_step + random.uniform(-0.04, 0.04)
                x = rayon * math.cos(angle)
                z = rayon * math.sin(angle)

                taille = 12
                # distance_min pour rapprocher les temples sans les faire toucher
                if position_valide(x, z, taille, temples_existants, distance_min=3):
                    creer = random.choice(types_temples)
                    temple = creer(f"temple_{c}_{i}", taille)
                    cmds.move(x, 0, z, temple)

                    # Orientation vers le centre
                    rot = math.degrees(math.atan2(-z, -x))
                    cmds.rotate(0, rot, 0, temple)

                    cmds.parent(temple, groupe_ville)
                    temples_existants.append((x, z, taille))

    cmds.xform(groupe_ville, centerPivots=True)
    
    # Fusionne tous les temples en un seul objet
    # Sélectionne tous les enfants du groupe ville
    enfants = cmds.listRelatives(groupe_ville, children=True, fullPath=True)
    if enfants and len(enfants) > 1:
        # Duplique tous les objets pour les fusionner
        objets_a_fusionner = []
        for enfant in enfants:
            # Obtiens tous les meshes de chaque temple
            meshes = cmds.listRelatives(enfant, allDescendents=True, type='mesh', fullPath=True)
            if meshes:
                for mesh in meshes:
                    transform = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
                    objets_a_fusionner.append(transform)
        
        if len(objets_a_fusionner) > 1:
            # Fusionne tous les objets
            ville_fusionnee = cmds.polyUnite(objets_a_fusionner, name="ville_de_temples_fusionnee")[0]
            cmds.delete(ville_fusionnee, constructionHistory=True)
            
            # Supprime le groupe original
            cmds.delete(groupe_ville)
            return ville_fusionnee
    
    return groupe_ville


# EXÉCUTION
generer_ville_temple()

