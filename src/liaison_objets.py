#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from src.obstacles import Obstacle


def liaison_objets( dico,list_bounds,tolerance,seuil ):
    """
    Fonction qui créé des objets de type Obstacle et retourne une liste de ces obstacles

    :param list_bounds: Liste de listes de format [angle début obstacle,angle fin obstacle]
    :return: list_obstacles: liste d'objets de type Obstacle
    """

    list_obstacles = []
    n = len(list_bounds)
    list_predicted_position = []
    distance_min = 12000
    distance_max = 0

    for obst in range(n):


        # Calcul milieu obstacles et largeur

        if len(list_bounds) >= 1:
            angle_min = list_bounds[obst][0]
            angle_max = list_bounds[obst][1]
            center = abs( angle_min+angle_max ) / 2

            if center not in dico.keys():
                for angle in dico.keys():
                    if angle_min<=angle<=angle_max:
                        distance = dico[angle]
                        if distance>distance_max:
                            distance_max = distance
                        if distance<distance_min:
                            distance_min = distance
                dico[center] = (distance_max+distance_min)/2
            width = max(abs(angle_max - angle_min),(distance_max-distance_min) )

        # Creation des objets de type Obstacle

        list_obstacles.append( Obstacle( width,center ) )
        obstacle_traite = list_obstacles[obst]


        # Calcul predicted_position: la position predite de l'obstacle a l'instant t+1

        predictedPosition = center # TODO
        list_predicted_position.append( predictedPosition )
        obstacle_traite.set_predictedPosition( predictedPosition )

        # Calcul predicted_plus_proche
        for predicted in list_predicted_position:
            predicted_plus_proche = abs( predictedPosition-center )

        # Update et categorisation des obstacles

        if abs( center-predictedPosition ) < tolerance:
            obstacle_traite.set_updated( True )
        else:
            if abs( predicted_plus_proche-center ) < seuil:
                obstacle_traite.set_isMoving( True ) #on a un objet mobile
                obstacle_traite.set_updated( True )
            else:
                obstacle_traite.set_updated( False )
                list_obstacles.remove( obst )

    return list_obstacles






