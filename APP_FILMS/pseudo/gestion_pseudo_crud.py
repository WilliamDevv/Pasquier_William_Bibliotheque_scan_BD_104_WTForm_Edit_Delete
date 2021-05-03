"""
    Fichier : gestion_genres_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les genres.
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
from APP_FILMS.pseudo.gestion_pseudo_wtf_forms import FormWTFAjouterPseudo
from APP_FILMS.pseudo.gestion_pseudo_wtf_forms import FormWTFUpdatePseudo
from APP_FILMS.pseudo.gestion_pseudo_wtf_forms import FormWTFDeletePseudo

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5005/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@obj_mon_application.route("/pseudo_afficher/<string:order_by>/<int:id_pseudo_sel>", methods=['GET', 'POST'])
def pseudo_afficher(order_by, id_pseudo_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion pseudo ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_pseudo_sel == 0:
                    strsql_pseudo_afficher = """SELECT id_pseudo, pseudo FROM t_pseudo ORDER BY id_pseudo ASC"""
                    mc_afficher.execute(strsql_pseudo_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_pseudo_selected_dictionnaire = {"value_id_pseudo_selected": id_pseudo_sel}
                    strsql_pseudo_afficher = """SELECT id_pseudo, pseudo FROM t_pseudo WHERE id_pseudo = %(value_id_pseudo_selected)s"""

                    mc_afficher.execute(strsql_pseudo_afficher, valeur_id_pseudo_selected_dictionnaire)
                else:
                    strsql_pseudo_afficher = """SELECT id_pseudo, pseudo FROM t_pseudo ORDER BY id_pseudo DESC"""

                    mc_afficher.execute(strsql_pseudo_afficher)

                data_pseudo = mc_afficher.fetchall()

                print("data_genres ", data_pseudo, " Type : ", type(data_pseudo))

                # Différencier les messages si la table est vide.
                if not data_pseudo and id_pseudo_sel == 0:
                    flash("""La table "t_pseudo" est vide. !!""", "warning")
                elif not data_pseudo and id_pseudo_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le pseudo demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données pseudo affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. genres_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} genres_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("pseudo/pseudo_afficher.html", data=data_pseudo)


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


@obj_mon_application.route("/pseudo_ajouter", methods=['GET', 'POST'])
def pseudo_ajouter_wtf():
    form = FormWTFAjouterPseudo()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion pseudo ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionPseudo {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                pseudo_wtf = form.pseudo_wtf.data

                pseudo = pseudo_wtf
                valeurs_insertion_dictionnaire = {"value_pseudo": pseudo}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_pseudo = """INSERT INTO t_pseudo (id_pseudo,pseudo) VALUES (NULL,%(value_pseudo)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_pseudo, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('pseudo_afficher', order_by='DESC', id_pseudo_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_pseudo_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_pseudo_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_pseudo_crud:
            code, msg = erreur_gest_pseudo_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion genres CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_pseudo_crud.args[0]} , "
                  f"{erreur_gest_pseudo_crud}", "danger")

    return render_template("pseudo/pseudo_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
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


@obj_mon_application.route("/pseudo_update", methods=['GET', 'POST'])
def pseudo_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_pseudo_update = request.values['id_pseudo_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatePseudo()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            pseudo_update = form_update.pseudo_update_wtf.data

            valeur_update_dictionnaire = {"value_id_pseudo": id_pseudo_update, "value_pseudo": pseudo_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_pseudo = """UPDATE t_pseudo SET pseudo = %(value_pseudo)s WHERE id_pseudo = %(value_id_pseudo)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_pseudo, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('pseudo_afficher', order_by="ASC", id_pseudo_sel=id_pseudo_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_pseudo = "SELECT id_pseudo, pseudo FROM t_pseudo WHERE id_pseudo = %(value_id_pseudo)s"
            valeur_select_dictionnaire = {"value_id_pseudo": id_pseudo_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_pseudo, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_pseudo = mybd_curseur.fetchone()
            print("data_pseudo ", data_pseudo, " type ", type(data_pseudo), " pseudo ",
                  data_pseudo["pseudo"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_update_wtf.html"
            form_update.pseudo_update_wtf.data = data_pseudo["pseudo"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans pseudo_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans pseudo_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_pseudo_crud:
        code, msg = erreur_gest_pseudo_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_pseudo_crud} ", "danger")
        flash(f"Erreur dans pseudo_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_pseudo_crud.args[0]} , "
              f"{erreur_gest_pseudo_crud}", "danger")
        flash(f"__KeyError dans pseudo_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("pseudo/pseudo_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_pseudo_delete_wtf" du formulaire "genres/pseudo_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/pseudo_delete", methods=['GET', 'POST'])
def pseudo_delete_wtf():
    data_pseudo_avoir_personne_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_pseudo_delete = request.values['id_pseudo_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeletePseudo()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("pseudo_afficher", order_by="ASC", id_pseudo_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/pseudo_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_pseudo_avoir_personne_delete = session['data_pseudo_avoir_personne_delete']
                print("data_pseudo_avoir_personne_delete ", data_pseudo_avoir_personne_delete)

                flash(f"Effacer le pseudo de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_pseudo": id_pseudo_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_avoir_pseudo = """DELETE FROM t_avoir_pseudo WHERE fk_pseudo = %(value_id_pseudo)s"""
                str_sql_delete_idpseudo = """DELETE FROM t_pseudo WHERE id_pseudo = %(value_id_pseudo)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_avoir_pseudo, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idpseudo, valeur_delete_dictionnaire)

                flash(f"Pseudo définitivement effacé !!", "success")
                print(f"Pseudo définitivement effacé !!")

                # afficher les données
                return redirect(url_for('pseudo_afficher', order_by="ASC", id_pseudo_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_pseudo": id_pseudo_delete}
            print(id_pseudo_delete, type(id_pseudo_delete))

            # Requête qui affiche tous les films qui ont le genre que l'utilisateur veut effacer
            str_sql_avoir_pseudo_delete = """SELECT id_avoir_pseudo, pseudo, id_personne, pers_nom, pers_prenom, pers_dateDeNaissance FROM t_avoir_pseudo 
                                            INNER JOIN t_pseudo ON t_avoir_pseudo.fk_pseudo = t_pseudo.id_pseudo
                                            INNER JOIN t_personne ON t_avoir_pseudo.fk_personne = t_personne.id_personne
                                            WHERE fk_pseudo = %(value_id_pseudo)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_avoir_pseudo_delete, valeur_select_dictionnaire)
            data_pseudo_avoir_personne_delete = mybd_curseur.fetchall()
            print("data_pseudo_avoir_personne_delete...", data_pseudo_avoir_personne_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "genres/pseudo_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_pseudo_avoir_personne_delete'] = data_pseudo_avoir_personne_delete

            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_pseudo = "SELECT id_pseudo, pseudo FROM t_pseudo WHERE id_pseudo = %(value_id_pseudo)s"

            mybd_curseur.execute(str_sql_id_pseudo, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
            data_pseudo = mybd_curseur.fetchone()
            print("data_pseudo ", data_pseudo, " type ", type(data_pseudo), " pseudo ",
                  data_pseudo["pseudo"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "pseudo_delete_wtf.html"
            form_delete.pseudo_delete_wtf.data = data_pseudo["pseudo"]

            # Le bouton pour l'action "DELETE" dans le form. "pseudo_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans pseudo_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans pseudo_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")

        flash(f"Erreur dans pseudo_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")

        flash(f"__KeyError dans pseudo_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("pseudo/pseudo_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_personne_associes=data_pseudo_avoir_personne_delete)
