#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.analyze_dic import analyze_dic
from src.data_cleaner import data_cleaner
from src.liaison_objets import liaison_objets
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8")
nombre_tours = float(config['MESURES']['nombre_tours'])
resolution_degre = float(config['MESURES']['resolution_degre'])
distance_max = int(config['DETECTION']['distance_max'])
distance_infini = int(config['DETECTION']['distance_infini'])
ecart_min_inter_objet = int(config['DETECTION']['ecart_min_inter_objet'])
seuil_association = int(config['OBSTACLES FIXES OU MOBILES']['seuil_association'])


def mesures(Te, list_obstacles_precedente, threadData):
    """
    Récupération et traitements de données.

    """

    # Copie de la liste des mesures du thread
    lidarDataList = list(threadData.readyData)
    # Mise en forme des donnees, avec un dictionnaire liant angles a la distance associee, et moyennant les distances si il y a plusieurs tours effectues
    dico = data_cleaner(lidarDataList, nombre_tours, resolution_degre, distance_infini)

    # Detection des bords d'obstacles
    limits = analyze_dic(dico, distance_max, ecart_min_inter_objet)
    print("Ostacles détectés aux angles:", limits)

    # Mise a jour des obstacles detectes, incluant le filtre de kalman
    list_obstacles, list_obstacles_precedente = liaison_objets(dico, limits, seuil_association,
                                                               Te, list_obstacles_precedente)

    return dico, limits, list_obstacles, list_obstacles_precedente