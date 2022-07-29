# if you are in production install waitress (pip install waitress) and put this code 
'''from waitress import server
    serve(app, host="0.0.0.0", port=8081) '''
# before to run the app

# IMPORTATION DES BIBLIOHEQUES
import os
import sys
import cv2  # pip install opencv-python ...................................................
import numpy as np  # pip install numpy ......................................................
import tensorflow as tf
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from pdf2image import convert_from_path
import prediction as pred # importion de notre module python de prediction

# INTIALISATION DE FLASK
app = Flask(__name__)
'''app.secret_key = "joelhhybghbgfgy"
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'''

# CONFIGURATION DES CHEMINS ET CHARGEMENT DU MODELE
'''app.config['UPLOAD_PATH'] = "UPLOAD_FOLDER"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024'''
courant = os.path.abspath(os.path.dirname(sys.argv[0]))

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# FONCTION POUR UNE ROUTE QUI N'EXISTE PAS
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

# FONCTION UPLOAD PLUS PREDICTION DE DOCUMENTS PDF COMME IMAGE
@app.route('/predict_files', methods=['POST'])  
def predict_files():

    # RECUPERATION DES DOC DANS UN FORMDATA AVEC 'files' COMME CLE DE CHAMP
    files = request.files.getlist('files')
    resultat = []
    Extraction_caractere = "Pas disponible"
    for file in files:

        # determination du type de document if pdf else si image
        name = file.filename
        name_type = name.split('.')[-1].lower()

        # si le document est un pdf
        if name_type == "pdf":

            # stocker le fichier dans le repertoire temporaire data
            file.save(os.path.join(courant + "/data/", file.filename))

            # convertir le fichier en image avec pdf2image
            pages = convert_from_path(os.path.join(courant + "/data/", file.filename), dpi=200)

            # suppression du pdf
            os.remove(os.path.join(courant + "/data/" + name))

            # stocker les images PIL de pages dans data
            for idx,page in enumerate(pages):
                page.save(os.path.join(courant + "/data/", str(file.filename)+str(idx)+'.jpg')) 

            # recuperation des images et prediction
            for idx,page in enumerate(pages):

                # lecture de l'image et premiere prediction
                npimg = np.fromfile(os.path.join(courant + "/data/"+ str(file.filename)+str(idx)+'.jpg'), np.uint8)
                output = pred.class_prediction(npimg)
                
                # plus de precision sur la nature des documents
                if output["CLASSE"] == "Justificatif d'identité":
                    Detail_output = pred.ID_prediction(npimg)
                    # si le justificatif est une piece d'identité alors on appelle la fonction d'extraction 
                    # de caractere de la cni
                    if Detail_output["CLASSE"] == "CARTE D'IDENTITE":
                        Extraction_caractere = pred.CNI_Extraction(pred.ImgRogne(npimg))

                elif output["CLASSE"] == "Justificatif d'adresse":
                    Detail_output = pred.ADR_prediction(npimg)

                else:
                    Detail_output = pred.REV_prediction(npimg)

                resultat.append([{
                    'FAMILLE': output,
                    'NATURE' : Detail_output,
                    'EXTRACTION' : Extraction_caractere
                }])
                output=""
            output=""

            # suppression des images
            for idx,page in enumerate(pages):
                os.remove(os.path.join(courant + "/data/", str(file.filename)+str(idx)+'.jpg'))

        else :  # si cest une image
            npimg = np.fromfile(file, np.uint8)  # lecture de l'image
            output = pred.class_prediction(npimg)

            # plus de precision sur la nature des documents
            if output["CLASSE"] == "Justificatif d'identité":
                Detail_output = pred.ID_prediction(npimg)
                # si le justificatif est une piece d'identité alors on appelLe la fonction d'extraction 
                # de caractere de la cni
                if Detail_output["CLASSE"] == "CARTE D'IDENTITE":
                    Extraction_caractere = pred.CNI_Extraction(pred.ImgRogne(npimg))

            elif output["CLASSE"] == "Justificatif d'adresse":
                Detail_output = pred.ADR_prediction(npimg)

            else:
                Detail_output = pred.REV_prediction(npimg)

            resultat.append([{
                    'FAMILLE': output,
                    'NATURE' : Detail_output,
                    'EXTRACTION' : Extraction_caractere
                }]) 

    return jsonify(resultat)

# FONCTION CLASSIFICATION DE DOCUMENTS PDF COMME IMAGE
@app.route('/classifications', methods=['POST'])
def classifications():
    files = request.files.getlist('files')

    # initialisation des listes
    resultat = [] 
    ADR_nature = []
    REV_nature = [] 
    ID_nature = []

    for file in files:

       # determination du type de document if pdf else si image
        name = file.filename
        name_type = name.split('.')[-1].lower()

        # si le document est un pdf
        if name_type == "pdf":
            # stocker le fichier dans le repertoire temporaire data
            file.save(os.path.join(courant + "/data/", file.filename))

            # convertir le fichier en image avec pdf2image
            pages = convert_from_path(os.path.join(courant + "/data/", file.filename), dpi=200)

            # suppression du pdf
            os.remove(os.path.join(courant + "/data/" + name))

            # stocker les images PIL de pages dans data
            for idx,page in enumerate(pages):
                page.save(os.path.join(courant + "/data/", str(file.filename)+str(idx)+'.jpg'))

            # recuperation des images et prediction
            for idx,page in enumerate(pages):

                # lecture de l'image
                npimg = np.fromfile(os.path.join(courant + "/data/"+ str(file.filename)+str(idx)+'.jpg'), np.uint8)
                output = pred.class_prediction(npimg)
                            
                # plus de precision sur la nature des documents pour une classification plus detaillée
                # pour les justificatifs d'identité
                if output["CLASSE"] == "Justificatif d'identité":
                    Detail_output = pred.ID_prediction(npimg)

                # ajout des information de prediction dans un json
                    ID_nature.append({
                        'NOM': str(file.filename)+str(idx)+'.jpg',
                        'FAMILLE': output,
                        'NATURE': Detail_output,
                    })
                # pour les justificatifs d'adresse
                elif output["CLASSE"] == "Justificatif d'adresse":
                    Detail_output = pred.ADR_prediction(npimg)

                    # ajout des information de pridiction dans un json
                    ADR_nature.append({
                        'NOM': str(file.filename)+str(idx)+'.jpg',
                        'FAMILLE': output,
                        'NATURE': Detail_output,
                    })

                # pour les justificatifs de revenu
                else:
                    Detail_output = pred.REV_prediction(npimg)
                    
                    # ajout des information de prEdiction dans un json
                    REV_nature.append({
                        'NOM': str(file.filename)+str(idx)+'.jpg',
                        'FAMILLE': output,
                        'NATURE': Detail_output,
                    })
                output=""
            output=""

            # suppression des images
            for idx,page in enumerate(pages):
                os.remove(os.path.join(courant + "/data/", str(file.filename)+str(idx)+'.jpg'))
        
        else : # si cest une image
            npimg = np.fromfile(file, np.uint8)
            output = pred.class_prediction(npimg)

            # pour les justificatifs d'identite
            if output["CLASSE"] == "Justificatif d'identité":
                Detail_output = pred.ID_prediction(npimg)

                # ajout des information de pridiction dans un json
                ID_nature.append({
                    'NOM': str(file.filename),
                    'FAMILLE': output,
                    'NATURE': Detail_output,
                })

            # pour les justificatifs d'adresse
            elif output["CLASSE"] == "Justificatif d'adresse":
                Detail_output = pred.ADR_prediction(npimg)

                # ajout des information de pridiction dans un json
                ADR_nature.append({
                    'NOM': str(file.filename),
                    'FAMILLE': output,
                    'NATURE': Detail_output,
                })

            # pour les justificatifs de revenu
            else:
                Detail_output = pred.REV_prediction(npimg)

                # ajout des information de pridiction dans un json
                REV_nature.append({
                    'NOM': str(file.filename),
                    'FAMILLE': output,
                    'NATURE': Detail_output,
                })
            output=""
    
        # le fichier json fichier regroupant toute les information
    resultat.append({
        'ID': ID_nature,
        'ADR': ADR_nature,
        'REV': REV_nature
    })

    return jsonify(resultat)

# FONCTION EXTRACTION VIVA DE DOCUMENTS PDF COMME IMAGE
@app.route('/visa_extraction', methods=['POST'])  
def visa_extraction():

    # RECUPERATION DES DOC DANS UN FORMDATA AVEC 'files' COMME CLE DE CHAMP
    files = request.files.getlist('files')
    resultat = []
    for file in files:

        # determination du type de document if pdf else si image
        name = file.filename
        name_type = name.split('.')[-1].lower()

        # si le document est un pdf
        if name_type == "pdf":

            # stocker le fichier dans le repertoire temporaire data
            file.save(os.path.join(courant + "/data/", file.filename))

            # convertir le fichier en image avec pdf2image
            pages = convert_from_path(os.path.join(courant + "/data/", file.filename), dpi=200)

            # suppression du pdf
            os.remove(os.path.join(courant + "/data/" + name))

            # stocker les images PIL de pages dans data
            for idx,page in enumerate(pages):
                page.save(os.path.join(courant + "/data/", str(file.filename)+str(idx)+'.jpg')) 

            # recuperation des images et prediction
            for idx,page in enumerate(pages):

                # lecture de l'image et premiere prediction
                npimg = np.fromfile(os.path.join(courant + "/data/"+ str(file.filename)+str(idx)+'.jpg'), np.uint8)
                output = pred.VISA_Extraction(pred.ImgRogne(npimg))
                                
                # ajout des information d'extraction dans un json
                resultat.append({
                    'NOM': output,
                })
                output=""
            output=""

            # suppression des images
            for idx,page in enumerate(pages):
                os.remove(os.path.join(courant + "/data/", str(file.filename)+str(idx)+'.jpg'))

        else :  # si cest une image
            npimg = np.fromfile(file, np.uint8)  # lecture de l'image
            output = pred.VISA_Extraction(pred.ImgRogne(npimg))

            resultat.append({
                    'NOM': output,
                }) 

    return jsonify(resultat)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
    # app.run(debug=True)