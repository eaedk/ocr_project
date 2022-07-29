# IMPORTATION DES BIBLIOHEQUES
import os
import sys
import cv2  # pip install opencv-python ....................................................
import numpy as np  # pip install numpy ....................................................
import tensorflow as tf #pip install tensorfflow ...........................................
import pytesseract # pip install pytesseract ...............................................
from resizeimage import resizeimage #pip install python-resize-image .......................
import traitementText as pretext

# CHARGEMENT DES MODELES IA
courant = os.path.abspath(os.path.dirname(sys.argv[0]))
class_modele = tf.keras.models.load_model(courant + "/modeles/C4_BUILDER_1.h5")
ID_modele = tf.keras.models.load_model(courant + "/modeles/C4_IDT_1.h5")
ADR_modele = tf.keras.models.load_model(courant + "/modeles/C4_ADR_1.h5")
REV_modele = tf.keras.models.load_model(courant + "/modeles/C4_REV3_1.h5")

# FONCTION GENERALE DE PREDICTION 
def class_prediction(npimg):
    resultat = []

    # lecture et pretraitement de l'image fonction du pretraitement lors de la conception du modele
    img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (500, 500))
    data = img.reshape(-1, 500 * 500)
    data = data / 255.
    data = data.reshape(-1, 500, 500, 1)
    # determination du type
    model_out = class_modele.predict([data])
    if np.argmax(model_out) == 0:
        str_label = "Justificatif d'identité"
    elif np.argmax(model_out) == 1:
        str_label = "Justificatif d'adresse"
    elif np.argmax(model_out) == 2:
        str_label = "Justificatif de revenu"
    resultat = {
        'CLASSE': str(str_label),
        'PROBABILITE': str(np.amax(model_out)),
        'SUMMARY': model_out.tolist()
    }
    return resultat 

# FONCTION DE PREDICTION DES JUSTIFICATIFS D'IDENTITES 
def ID_prediction(npimg):
    resultat = []

    # lecture et pretraitement de l'image fonction du pretraitement lors de la conception du modele
    img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (500, 500))
    data = img.reshape(-1, 500 * 500)
    data = data / 255.
    data = data.reshape(-1, 500, 500, 1)

    # determination du type
    model_out = ID_modele.predict([data])
    if np.argmax(model_out) == 0:
        str_label = "CARTE D'IDENTITE"
    elif np.argmax(model_out) == 1:
        str_label = "EXTRAIT"
    elif np.argmax(model_out) == 2:
        str_label = "CERTIFICAT"
    elif np.argmax(model_out) == 3:
        str_label = "PASSEPORT"
    resultat = {
        'CLASSE': str(str_label),
        'PROBABILITE': str(np.amax(model_out)),
        'SUMMARY': model_out.tolist()
    }
    return resultat 

# FONCTION DE PREDICTION DES JUSTIFICATIFS D'ADRESSES
def ADR_prediction(npimg):
    resultat = []

    # lecture et pretraitement de l'image fonction du pretraitement lors de la conception du modele
    img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (500, 500))
    data = img.reshape(-1, 500 * 500)
    data = data / 255.
    data = data.reshape(-1, 500, 500, 1)

    # determination du type
    model_out = ADR_modele.predict([data])
    if np.argmax(model_out) == 0:
        str_label = "CERTIFICAT"
    elif np.argmax(model_out) == 1:
        str_label = "DOCUMENT SGCI"
    elif np.argmax(model_out) == 2:
        str_label = "FACTURE"
    resultat = {
        'CLASSE': str(str_label),
        'PROBABILITE': str(np.amax(model_out)),
        'SUMMARY': model_out.tolist()
    }
    return resultat 

# FONCTION DE PREDICTION DES JUSTIFICATIFS DE REVENU  
def REV_prediction(npimg):
    resultat = []

    # lecture et pretraitement de l'image fonction du pretraitement lors de la conception du modele
    img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (500, 500))
    data = img.reshape(-1, 500 * 500)
    data = data / 255.
    data = data.reshape(-1, 500, 500, 1)

    # determination du type
    model_out = REV_modele.predict([data])
    if np.argmax(model_out) == 0:
        str_label = "BULLETN"
    elif np.argmax(model_out) == 1:
        str_label = "FICHE ENTREPRISE"
    elif np.argmax(model_out) == 2:
        str_label = "DOCUMENT SGCI"
    resultat = {
        'CLASSE': str(str_label),
        'PROBABILITE': str(np.amax(model_out)),
        'SUMMARY': model_out.tolist()
    }
    return resultat

#FONCTION D'EXTRACTION DE CARRACTERES
#FONCTION DE PRETRAITEMENT

#NIVEAU GRAY
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#ECROSION
def erode(image):
    kernel = np.ones((1,1),np.uint8)
    #return cv2.dilate(image, kernel, iterations=1)
    return cv2.erode(image, kernel, iterations = 1)

# FONCTION DE RONGNAGE D'IMAGE
def ImgRogne(npimg):
    img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v= cv2.split(hsv)
    ret_h, th_h = cv2.threshold(h,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret_s, th_s = cv2.threshold(s,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #Fusion th_h et th_s
    th=cv2.bitwise_or(th_h,th_s)
    #Ajouts de bord à l'image
    bordersize=10
    th=cv2.copyMakeBorder(th, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )

    #Remplissage des contours
    im_floodfill = th.copy()
    h, w = th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    th = th | im_floodfill_inv

    #Enlèvement des bord de l'image
    th=th[bordersize: len(th)-bordersize,bordersize: len(th[0])-bordersize]


    contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for i in range (0, len(contours)) :
        mask_BB_i = np.zeros((len(th),len(th[0])), np.uint8)
        x,y,w,h = cv2.boundingRect(contours[i])
        cv2.drawContours(mask_BB_i, contours, i, (255,255,255), -1)
        BB_i=cv2.bitwise_and(img,img,mask=mask_BB_i)
        if h >90 and w>90 :
            BB_i=BB_i[y:y+h,x:x+w]
            return BB_i

#FONCTION D'EXTRACTION DE CARACTERES
# 
# CAS D'UNE PIÉCE D'IDENTITÉ

def CNI_Extraction(image):
    resultat = []
    # LECTURE ET REDIMENSSIONEMENT DE L'IMAGE ISSU DU ROGNAGE
    width = 500
    height = 300
    dim = (width, height)
    img = get_grayscale(image)

    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    img = cv2.GaussianBlur(img, (1,1), 1)
    img1= img.copy()
    img2= img.copy()
    img3= img.copy()

    # CONFIGURATION DE L'ATTRIBUT CONFIG DE TESSERACT
    custom_config = r'--psm 7 --oem 1 -c tessedit_char_whitelist= azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN'

    # CIBLAGE DE L'IMMATRICULATION DE LA PIECE
    x,w = 240, 480
    y,h= 60 , 90
    Immatriculation = cv2.rectangle(img, (x, y), (w, h), (0, 255, 0), 1)
    Immatriculation = cv2.resize(img[y:h, x:w], (300,50), interpolation = cv2.INTER_AREA)
    Immatriculation_extrait = pytesseract.image_to_string(Immatriculation , config=custom_config)

    # CIBLAGE DU NOM DE LA PIECE
    x1,w1 = 140, 350
    y1,h1 = 80, 120
    Nom = cv2.rectangle(img1, (x1, y1), (w1, h1), (0, 255, 0), 1)
    Nom = cv2.resize(img1[y1:h1, x1:w1], (400,70), interpolation = cv2.INTER_AREA)
    Nom_extrait = pytesseract.image_to_string(Nom , config=custom_config)

    # CIBLAGE DU PRENOM DE LA PIECE
    x2,w2 = 140, 450
    y2,h2 = 109 , 150
    Prenom = cv2.rectangle(img2, (x2, y2), (w2, h2), (0, 255, 0), 1)
    Prenom = cv2.resize(img2[y2:h2, x2:w2], (500,70), interpolation = cv2.INTER_AREA)
    Prenom_extrait = pytesseract.image_to_string(Prenom , config=custom_config)

    # CIBLAGE DE LA DATE D'EXPIRATION DE LA PIECE
    x3,w3 = 350, 480
    y3,h3 = 240, 500
    Date_fin = cv2.rectangle(img3, (x3, y3), (w3, h3), (0, 255, 0), 1)
    Date_fin = cv2.resize(img3[y3:h3, x3:w3], (550,100), interpolation = cv2.INTER_AREA) 
    Date_fin_extrait = pytesseract.image_to_string(Date_fin , config=custom_config)
    
    # CIBLAGE DU LIEU D'ETABLISSEMENT DE LA PIECE
    x4,w4 = 150, 350
    y4,h4 = 250, 300
    Lieu = cv2.rectangle(img, (x4, y4), (w4, h4), (0, 255, 0), 1)
    Lieu = cv2.resize(img[y4:h4, x4:w4], (300,50), interpolation = cv2.INTER_AREA)  
    Lieu_extrait = pytesseract.image_to_string(Lieu , config=custom_config)
 
    

    resultat = {
            'IMMATRICULATION': pretext.modif_chiffre(pretext.sup_espace(pretext.sup_saut(Immatriculation_extrait.upper()))),
            'NOM': pretext.modif_lettre(pretext.sup_saut(Nom_extrait.upper())),
            'PRENOM': pretext.modif_lettre(pretext.sup_saut(Prenom_extrait.upper())),
            #'DATE_EXPIRATION' : Date_fin_extrait,
            #'LIEU_ETABLISSEMENT' : Lieu_extrait.upper()
        }
    return resultat
    
#FONCTION D'EXTRACTION DE CARACTERES
# 
# CAS D'UNE CARTE VISA

def VISA_Extraction(image):

    custom_config = r'--psm 6'

    # LECTURE ET REDIMENSSIONEMENT DE L'IMAGE ISSU DU ROGNAGE
    width = 1500
    height = 700
    dim = (width, height)
    img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    img = cv2.GaussianBlur(img, (1,1), 3)
    img = get_grayscale(img)


    #DELIMITATION DE LA ZONE D'INFORMATION ET EXTRACTION 
    x1,w1 = 95, 1000
    y1,h1 = 530, 700
    Nom = cv2.rectangle(img, (x1, y1), (w1, h1), (0, 255, 0), 1)
    Nom_VISA = pytesseract.image_to_string(img[y1:h1, x1:w1], config=custom_config)
        
    resultat = pretext.modif_visa(Nom_VISA.upper()) 

    return resultat