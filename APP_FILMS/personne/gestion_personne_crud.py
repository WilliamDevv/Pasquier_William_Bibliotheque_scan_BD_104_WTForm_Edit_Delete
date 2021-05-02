"""
    Fichier : gestion_personne_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les personne.
"""
import sys

import pymysql
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from APP_FILMS import obj_mon_application
from APP_FILMS.database.connect_db_context_manager import MaBaseDeDonnee
from APP_FILMS.erreurs.exceptions import *
from APP_FILMS.erreurs.msg_erreurs import *
from APP_FILMS.personne.gestion_personne_wtf_forms import FormWTFAjouterPersonne
from APP_FILMS.personne.gestion_personne_wtf_forms import FormWTFDeletePersonne
from APP_FILMS.personne.gestion_personne_wtf_forms import FormWTFUpdatePersonne

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /personne_afficher
    
    Test : ex : http://127.0.0.1:5005/personne_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_personne_sel = 0 >> tous les personnes.
                id_personne_sel = "n" affiche le genre dont l'id est "n"
"""


@obj_mon_application.route("/personne_afficher/<string:order_by>/<int:id_personne_sel>", methods=['GET', 'POST'])
def personne_afficher(order_by, id_personne_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion personne ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionPersonnes {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_personne_sel == 0:
                    strsql_personne_afficher = """SELECT id_personne, pers_nom, pers_prenom, pers_dateDeNaissance FROM t_personne ORDER BY id_personne ASC """
                    mc_afficher.execute(strsql_personne_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": id_personne_sel}
                    strsql_personne_afficher = """SELECT id_personne, pers_nom, pers_prenom, pers_dateDeNaissance 
                    FROM t_personne  WHERE id_personne = %(value_id_personne_selected)s"""

                    mc_afficher.execute(strsql_personne_afficher, valeur_id_personne_selected_dictionnaire)
                else:
                    strsql_personne_afficher = """SELECT id_personne, pers_nom, pers_prenom, pers_dateDeNaissance FROM t_personne ORDER BY id_personne DESC"""

                    mc_afficher.execute(strsql_personne_afficher)

                data_personne = mc_afficher.fetchall()

                print("data_personne ", data_personne, " Type : ", type(data_personne))

                # Différencier les messages si la table est vide.
                if not data_personne and id_personne_sel == 0:
                    flash("""La table "t_personne" est vide. !!""", "warning")
                elif not data_personne and id_personne_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"La personne demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données personne affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. personne_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} personne_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            #raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("personne/personne_afficher.html", data=data_personne)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5005/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/personnes_ajouter", methods=['GET', 'POST'])
def personne_ajouter_wtf():
    form = FormWTFAjouterPersonne()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion personnes ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionPersonnes {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                name_personne_wtf = form.nom_personne_wtf.data
                firstName_personne_wtf = form.prenom_personne_wtf.data
                birthDate_personne_wtf = form.dateDeNaissance_personne_wtf.data

                name_personne = name_personne_wtf.capitalize()
                firstName_personne = firstName_personne_wtf.capitalize()
                birthDate_personne = birthDate_personne_wtf
                valeurs_insertion_dictionnaire = {"value_name": name_personne,
                                                  "value_firstName": firstName_personne,
                                                  "value_birthDate": birthDate_personne}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_personne = """INSERT INTO t_personne (`id_personne`, `pers_nom`, `pers_prenom`, `pers_dateDeNaissance`) VALUES (NULL,%(value_name)s,%(value_firstName)s,%(value_birthDate)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_personne, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('personne_afficher', order_by='DESC', id_personne_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_personne_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_personne_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_pers_crud:
            code, msg = erreur_gest_pers_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion personne CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_pers_crud.args[0]} , "
                  f"{erreur_gest_pers_crud}", "danger")

    return render_template("personne/personne_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /personne_update

    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"

    Paramètres : sans

    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/personne_update", methods=['GET', 'POST'])
def personne_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_personne_update = request.values['id_personne_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatePersonne()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_personne_update_wtf = form_update.nom_personne_update_wtf.data
            firstName_personne_update_wtf = form_update.prenom_personne_update_wtf.data
            birthDate_personne_update_wtf = form_update.dateDeNaissance_personne_update_wtf.data
            name_personne_update = name_personne_update_wtf.capitalize()
            firstName_personne_update = firstName_personne_update_wtf.capitalize()
            birthDate_personne_update = birthDate_personne_update_wtf

            valeur_update_dictionnaire = {"value_id_update": id_personne_update,
                                          "value_name_update": name_personne_update,
                                          "value_firstName_update": firstName_personne_update,
                                          "value_birthDate_update": birthDate_personne_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_personne = """UPDATE `t_personne` SET `pers_nom` = %(value_name_update)s, `pers_prenom` = %(value_firstName_update)s, `pers_dateDeNaissance` = %(value_birthDate_update)s WHERE `t_personne`.`id_personne` = %(value_id_update)s;"""
            #str_sql_update_personne = """UPDATE `t_personne` SET `pers_nom` = 'Wead', `pers_prenom` = 'asd', `pers_dateDeNaissance` = '1990-04-13' WHERE `t_personne`.`id_personne` = 16;"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_personne, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('personne_afficher', order_by="ASC", id_personne_sel=id_personne_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_personne = """SELECT id_personne, pers_nom, pers_prenom, pers_dateDeNaissance FROM t_personne WHERE id_personne = %(value_id_personne)s"""
            valeur_select_dictionnaire = {"value_id_personne": id_personne_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_personne, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_personne = mybd_curseur.fetchone()
            print("data_personne ", data_personne, " type ", type(data_personne), " personne ",
                  data_personne["pers_nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_update_wtf.html"
            form_update.nom_personne_update_wtf.data = data_personne["pers_nom"]
            form_update.prenom_personne_update_wtf.data = data_personne["pers_prenom"]
            form_update.dateDeNaissance_personne_update_wtf.data = data_personne["pers_dateDeNaissance"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans prenom_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans prenom_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_pers_crud:
        code, msg = erreur_gest_pers_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_pers_crud} ", "danger")
        flash(f"Erreur dans personne_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_pers_crud.args[0]} , "
              f"{erreur_gest_pers_crud}", "danger")
        flash(f"__KeyError dans personne_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("personne/personne_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete

    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"

    Paramètres : sans

    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/personne_delete", methods=['GET', 'POST'])
def personne_delete_wtf():
    data_personne_avoir_pseudo_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_personne_delete = request.values['id_personne_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeletePersonne()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("personne_afficher", order_by="ASC", id_personne_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "personne/personne_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_personne_avoir_pseudo_delete = session['data_personne_avoir_pseudo_delete']
                print("data_personne_avoir_pseudo_delete ", data_personne_avoir_pseudo_delete)

                flash(f"Effacer la personne de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_personne": id_personne_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_avoir_pseudo = """DELETE FROM t_avoir_pseudo WHERE fk_personne = %(value_id_personne)s"""
                str_sql_delete_idpersonne = """DELETE FROM t_personne WHERE id_personne = %(value_id_personne)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_avoir_pseudo, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idpersonne, valeur_delete_dictionnaire)

                flash(f"Personne définitivement effacé !!", "success")
                print(f"Personne définitivement effacé !!")

                # afficher les données
                return redirect(url_for('personne_afficher', order_by="ASC", id_personne_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_personne": id_personne_delete}
            print(id_personne_delete, type(id_personne_delete))

            # Requête qui affiche tous les films qui ont le genre que l'utilisateur veut effacer
            str_sql_avoir_pseudo_delete = """SELECT id_avoir_pseudo, pseudo, id_personne, pers_nom FROM t_avoir_pseudo 
                                            INNER JOIN t_pseudo ON t_avoir_pseudo.fk_pseudo = t_pseudo.id_pseudo
                                            INNER JOIN t_personne ON t_avoir_pseudo.fk_personne = t_personne.id_personne
                                            WHERE fk_personne = %(value_id_personne)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_avoir_pseudo_delete, valeur_select_dictionnaire)
            data_personne_avoir_pseudo_delete = mybd_curseur.fetchall()
            print("data_personne_avoir_pseudo_delete...", data_personne_avoir_pseudo_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_personne_avoir_pseudo_delete'] = data_personne_avoir_pseudo_delete

            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_personne = """SELECT id_personne, pers_nom, pers_prenom, pers_dateDeNaissance FROM t_personne WHERE id_personne = %(value_id_personne)s"""

            mybd_curseur.execute(str_sql_id_personne, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
            data_personne = mybd_curseur.fetchone()
            print("data_personne", data_personne, " type ", type(data_personne),
                  "nom", data_personne["pers_nom"],
                  "prénom", data_personne["pers_prenom"],
                  "date de naissance", data_personne["pers_dateDeNaissance"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.nom_personne_delete_wtf.data = data_personne["pers_nom"]
            form_delete.prenom_personne_delete_wtf.data = data_personne["pers_prenom"]
            form_delete.dateDeNaissance_personne_delete_wtf.data = data_personne["pers_dateDeNaissance"]

            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans personne_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans personne_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_pers_crud:
        code, msg = erreur_gest_pers_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_pers_crud} ", "danger")

        flash(f"Erreur dans personne_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_pers_crud.args[0]} , "
              f"{erreur_gest_pers_crud}", "danger")

        flash(f"__KeyError dans personne_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("personne/personne_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_pseudo_associes=data_personne_avoir_pseudo_delete)
