# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   libAeroShapes :                                                       *
#*   Routines pour la génération de formes fuselées,                       *
#*   https://fr.wikipedia.org/wiki/Corps_de_moindre_tra%C3%AEn%C3%A9e.     *
#*   Nota : les coordonnées et faces sont dans le plan xy.                 *
#*                                                                         *
#*   Auteur :  Claude GUTH                                                 *
#*   Date de création :      2021-07-28                                    *
#*   Dernière modification : 2021-07-28                                    *
#*                                                                         *
#*   Ce programme est libre de droits.                                     *
#*   Son utilisation est sous la responsablité de l'utilisateur            *
#*   sans aucune garantie de l'auteur.                                     *
#*                                                                         *
#***************************************************************************
# TODO: translate

__title__  = "airPlane Workbench - construction de formes fuselées"
__author__ = "Claude GUTH"

import FreeCAD
import Draft
import DraftTools
import Part
import math

def getLyonCoords(longueur, diametre, nbPoints=100):
  """
  :param longueur:          longueur (selon axe x) de la forme
  :param diametre:          diamètre de la forme
  :param nbPoints:          nb de points calculés
  :return: les coordonnées d'ordonnées positives d'une fome Lyon modèle A
  """
  # parametres intermédiaires de calcul
  ky = diametre*1.11326

  # points de la forme
  cLyon = [FreeCAD.Vector(0, 0, 0)]
  kx = 1 / float(nbPoints-1)
  for i in range(1, nbPoints):
    xRel= kx * float(i) 
    xRel2= xRel * xRel
    xRel3= xRel2 * xRel
    xRel4= xRel3 * xRel
    yPos = ky * math.sqrt(xRel - xRel2 - xRel3 + xRel4)
    cLyon.append(FreeCAD.Vector(xRel * longueur, yPos, 0))
  return cLyon

def getHoernerCoords(longueur, diametre, xRelEpaisseurMax, nbPoints=100):
  """
  :param longueur:          longueur (selon axe x) de la forme
  :param diametre:          diamètre de la forme
  :param xRelEpaisseurMax:  abscisse relative (0..1) pour l'épaisseur max
  :param nbPoints:          nb de points calculés
  :return: les coordonnées d'ordonnées positives d'une FEC
  """
  # parametres intermédiaires de calcul
  xeMax = xRelEpaisseurMax*longueur
  yeMax = 0.5*diametre
  pi_2 =  math.pi/2

  # points de la forme
  cFEC = [FreeCAD.Vector(0, 0, 0)]
  kl = longueur / float(nbPoints-1)
  for i in range(1, nbPoints):
    xPos = kl * float(i)
    if xPos < xeMax:
      yPos = yeMax * math.sqrt(2*xPos*xeMax - xPos*xPos) / xeMax
    else:
      yPos = yeMax * math.cos(pi_2*(xeMax-xPos)/(longueur-xeMax))
    cFEC.append(FreeCAD.Vector(xPos, yPos, 0))
  return cFEC

def getDuhamelCoords(longueur, diametre, nbPoints=100):
  """
  :param longueur:          longueur (selon axe x) de la forme
  :param diametre:          diamètre de la forme
  :param nbPoints:          nb de points calculés
  :return: les coordonnées d'ordonnées positives d'une fome Duhamel simplifiée
  """
  # parametres intermédiaires de calcul
  ky = diametre*1.3

  # points de la forme
  cLyon = [FreeCAD.Vector(0, 0, 0)]
  kx = 1 / float(nbPoints-1)
  for i in range(1, nbPoints):
    xRel= kx * float(i) 
    yPos = ky * (1 - xRel) * math.sqrt(xRel)
    cLyon.append(FreeCAD.Vector(xRel * longueur, yPos, 0))
  return cLyon

def getNACACoords(longueur, diametre, nbPoints=100):
  """
  :param longueur:          longueur (selon axe x) de la forme
  :param diametre:          diamètre de la forme
  :param nbPoints:          nb de points calculés
  :return: les coordonnées d'ordonnées positives d'une fome NACA 4 chiffres (non optimal)
  """
  # parametres intermédiaires de calcul
  ky = diametre

  # points de la forme
  cLyon = [FreeCAD.Vector(0, 0, 0)]
  kx = 1 / float(nbPoints-1)
  for i in range(1, nbPoints):
    xRel= kx * float(i) 
    xRel2= xRel * xRel
    xRel3= xRel2 * xRel
    xRel4= xRel3 * xRel
    yPos = ky * (1.4845*math.sqrt(xRel) -0.63*xRel - 1.758*xRel2 + 1.4215*xRel3 - 0.5075*xRel4)
    cLyon.append(FreeCAD.Vector(xRel * longueur, yPos, 0))
  return cLyon


