#!/usr/bin/env python3
# coding: utf-8
import pylab as pl
import configparser
from math import pi, cos, sin

# Recuperation de la config
config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8")
distance_max_x_cartesien = int(config['DETECTION']['distance_max_x_cartesien'])
distance_max_y_cartesien = int(config['DETECTION']['distance_max_y_cartesien'])
distance_max = int(config['DETECTION']['distance_max'])


def init_affichage_cartesien():
    """
    Initialisation de l'affichage.

    """

    pl.ion()
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-distance_max_x_cartesien/2, distance_max_x_cartesien/2)
    ax.set_ylim(-distance_max_y_cartesien/2, distance_max_y_cartesien/2)
    ax.axhline(0, 0)
    ax.axvline(0, 0)
    r = []
    theta = []
    ax.scatter(theta, r)

    return ax, fig


def init_affichage_polaire():
    """
    Initialisation de l'affichage.

    """

    pl.ion()
    fig = pl.figure()
    ax = fig.add_subplot(111, polar=True)  # polaire !
    ax.set_ylim(0, distance_max)
    ax.set_ylim(0, 2 * pi)
    ax.axhline(0, 0)
    ax.axvline(0, 0)
    r = []
    theta = []
    ax.scatter(theta, r)

    return ax, fig


def affichage_cartesien(limits, ax, list_obstacles, dico, fig):
    """
        Affichage.

    """

    list_detected = []
    for detected in limits:
        for n in range(len(detected)):
            list_detected.append(detected[n])

    ax.clear()
    ax.set_xlim(-distance_max_x_cartesien / 2, distance_max_x_cartesien / 2)
    ax.set_ylim(-distance_max_y_cartesien / 2, distance_max_y_cartesien / 2)
    ax.axhline(0, 0)
    ax.axvline(0, 0)

    for o in list_obstacles:
        angle = o.center
        r = dico[angle]
        circle = pl.Circle((r * cos(angle), r * sin(angle)), radius=200, fc='orange')
        ax.add_artist(circle)

        if o.get_piste_obstacle() is not None:
            print("piste : ", o.get_piste_obstacle())
            for elt_piste in o.get_piste_obstacle():
                x_elt = elt_piste[0]
                y_elt = elt_piste[1]
                circle = pl.Circle((x_elt, y_elt), radius=20, fc='black')
                ax.add_artist(circle)

        if o.get_predicted_kalman() is not None:
            x_kalman = o.get_predicted_kalman()[0][0]
            y_kalman = o.get_predicted_kalman()[0][2]
            print("x_kalman : ", x_kalman)
            print("y_kalman : ", y_kalman)
            circle = pl.Circle((x_kalman, y_kalman), radius=200, fc='crimson')
            ax.add_artist(circle)

    # Listes des positions des obstacles à afficher
    detected_x = [dico[detected] * cos(detected) for detected in list_detected]
    detected_y = [dico[detected] * sin(detected) for detected in list_detected]

    # Listes des positions des points à afficher
    x = [distance * cos(angle) for distance, angle in zip(dico.values(), dico.keys())]
    y = [distance * sin(angle) for distance, angle in zip(dico.values(), dico.keys())]

    pl.plot(x, y, 'ro', markersize=0.6)
    pl.plot(detected_x, detected_y, 'bo', markersize=1.8)
    pl.grid()
    fig.canvas.draw()


def affichage_polaire(limits, ax, list_obstacles, dico, fig):
    """
        Affichage.

    """

    list_detected = []
    for detected in limits:
        for n in range(len(detected)):
            list_detected.append(detected[n])

    ax.clear()
    ax.set_xlim(0, 2 * pi)
    ax.set_ylim(0, +distance_max)
    ax.axhline(0, 0)
    ax.axvline(0, 0)

    for o in list_obstacles:
        angle = o.center
        r = dico[angle]
        print("nb_obstacles: ", len(list_obstacles))
        circle = pl.Circle((r * cos(angle), r * sin(angle)), o.width / 2, transform=ax.transData._b, color='g',
                          alpha=0.4)
        ax.add_artist(circle)

        if o.get_piste_obstacle() is not None:
            print("piste : ", o.get_piste_obstacle())
            for elt_piste in o.get_piste_obstacle():
                x_elt = elt_piste[0]
                y_elt = elt_piste[1]
                circle = pl.Circle((x_elt, y_elt), 8, transform=ax.transData._b,
                                  color='y',
                                  alpha=0.4)
                ax.add_artist(circle)

        if o.get_predicted_kalman() is not None:
            x_kalman = o.get_predicted_kalman()[0][0]
            y_kalman = o.get_predicted_kalman()[0][2]
            print("x_kalman : ", x_kalman)
            print("y_kalman : ", y_kalman)
            print("position kalman: ", x_kalman, " et ", y_kalman)
            circle = pl.Circle((x_kalman, y_kalman), o.width / 2, transform=ax.transData._b,
                              color='b',
                              alpha=0.4)
            ax.add_artist(circle)

    # Listes des positions des obstacles à afficher
    detected_r = [dico[detected] for detected in list_detected]
    detected_theta = [detected for detected in list_detected]

    # Listes des positions des points à afficher
    r = [distance for distance in dico.values()]
    theta = [angle for angle in dico.keys()]
    pl.plot(theta, r, 'ro', markersize=0.6)
    pl.plot(detected_theta, detected_r, 'bo', markersize=1.8)

    pl.grid()
    fig.canvas.draw()