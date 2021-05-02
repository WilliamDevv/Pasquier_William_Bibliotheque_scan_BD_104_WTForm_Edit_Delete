"""
    Fichier : gestion_personne_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import DateField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp


class FormWTFAjouterPersonne(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_personne_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_personne_wtf = StringField("Clavioter le nom de la personnne ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_personne_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])

    prenom_personne_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_personne_wtf = StringField("Clavioter le prénom de la personne ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                         Regexp(prenom_personne_regexp,
                                                                                message="Pas de chiffres, de caractères "
                                                                                        "spéciaux, "
                                                                                        "d'espace à double, de double "
                                                                                        "apostrophe, de double trait union")
                                                                         ])

    #dateDeNaissance_personne_regexp = "^(\d{4})-(\d{2})-(\d{2})"
    #dateDeNaissance_personne_wtf = DateField("Clavioter l'âge de la personne", format='%Y-%m-%d', validators=[Regexp(dateDeNaissance_personne_regexp,
                                                                                                                     #message="Pas de lettre, de caractères "
                                                                                                                             #"spéciaux, sous ce format "
                                                                                                                             #"YYYY-MM-DD ex. 2002-08-17")
                                                                                                              #])

    dateDeNaissance_personne_wtf = DateField("Clavioter l'âge de la personne", format='%Y-%m-%d')

    submit = SubmitField("Enregistrer personne")


class FormWTFUpdatePersonne(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_personne_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_personne_update_wtf = StringField("Clavioter le nom de la personnne ",
                                   validators=[Length(min=2, max=20, message="min 2 max 20"),
                                               Regexp(nom_personne_update_regexp,
                                                      message="Pas de chiffres, de caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait union")
                                               ])

    prenom_personne_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_personne_update_wtf = StringField("Clavioter le prénom de la personne ",
                                      validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                  Regexp(prenom_personne_update_regexp,
                                                         message="Pas de chiffres, de caractères "
                                                                 "spéciaux, "
                                                                 "d'espace à double, de double "
                                                                 "apostrophe, de double trait union")
                                                  ])

    # dateDeNaissance_personne_regexp = "^(\d{4})-(\d{2})-(\d{2})"
    # dateDeNaissance_personne_wtf = DateField("Clavioter l'âge de la personne", format='%Y-%m-%d', validators=[Regexp(dateDeNaissance_personne_regexp,
    # message="Pas de lettre, de caractères "
    # "spéciaux, sous ce format "
    # "YYYY-MM-DD ex. 2002-08-17")
    # ])

    dateDeNaissance_personne_update_wtf = DateField("Clavioter l'âge de la personne", format='%Y-%m-%d')

    submit = SubmitField("Update personne")


class FormWTFDeletePersonne(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_personne_delete_wtf = StringField("Effacer cette personne")
    prenom_personne_delete_wtf = StringField("Effacer cette personne")
    dateDeNaissance_personne_delete_wtf = StringField("Effacer cette personne")
    submit_btn_del = SubmitField("Effacer personne")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")