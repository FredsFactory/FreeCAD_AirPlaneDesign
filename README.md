# FreeCAD_AirPlaneDesign
FreeCAD Air Plane Design WorkBench for FreeCAD v0.17 and v0.18.
Warning: This is highly experimental code.


![](https://github.com/FredsFactory/FreeCAD_AirPlaneDesign/blob/master/AirplaneDesign001.png)

![](https://github.com/FredsFactory/FreeCAD_AirPlaneDesign/blob/master/AirPlaneDesignWorkbench.png)

# Installation Instructions
Simply use AddOn Manager (from Tools menu).

# How to use it ?
After installation a new menu appears:  
1. Wizard: do not use this yet! (UI under heavy development!)  
2. Init New Plane: initialize a new document, with a sheet with many parameters  
3. Generate Wing: generate the wing based on the parameters in the sheet AirPlaneData  
4. Generate Wing Rib: before using the function make a clone of the wing and apply the function on this clone. The parameters are currently in the "generateWingRibs.py" program they are being outsourced to the sheet. Under development

Ability to choose the:  
* decomposition of the wing panel: cell B3  
* number of profil: cell B4  
* profiles you want to import: B6 (.dat format), two profiles are installed with the workbench (eppler 205 and eppler 207); If you want use another profile simply download it in to the `wingribprofil/` folder

# Release Notes
V0.001 11 July 2018: Initial version
