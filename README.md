# The FreeCAD Air Plane Design Workbench
FreeCAD Air Plane Design WorkBench for FreeCAD >=v0.17
**Warning:** This is highly experimental code.


![](https://github.com/FredsFactory/FreeCAD_AirPlaneDesign/blob/master/AirplaneDesign001.png)

![](https://github.com/FredsFactory/FreeCAD_AirPlaneDesign/blob/master/AirPlaneDesign002.png)

![](https://github.com/FredsFactory/FreeCAD_AirPlaneDesign/blob/master/AirPlaneDesignWorkbench.png)

# Installation
Simply use the FreeCAD [Addon Manager](https://github.com/FreeCAD/FreeCAD-addons#installing).

# How to use it ?
After installation a new menu appears:  
1. Wizard: do not use this yet! (**Note:** UI under heavy development!)  
2. Init New Plane: initialize a new document, with a sheet with many parameters  
3. Generate Wing: generate the wing based on the parameters in the sheet AirPlaneData  
4. Generate Wing Rib: before using the function make a clone of the wing and apply the function on this clone. The parameters are currently in the "generateWingRibs.py" program they are being outsourced to the sheet. **Note:** Under development

Ability to choose the:  
* Decomposition of the wing panel: cell B3  
* Number of profile: cell B4  
* Profiles you want to import: B6 (.dat format), two profiles are installed with the workbench (eppler 205 and eppler 207); If you want use another profile simply download it in to the `wingribprofil/` folder

# Feedback
Feedback can be provided via the https://forum.freecadweb.org/viewtopic.php?f=12&t=38215 on the FreeCAD forums

# Release Notes
V0.002 29 July 2019: 
* compatible with V0.18 tested on PC windows 10 & MacOS, 
* split the inital sheet in 3 sheet
* ribs is now managed as a parameter : the list of ribs is now managed as a parameter in the table :"AirPlaneRibs" : position, length & rotation.
* new picture in readme fil to explain some parameters.

V0.001 11 July 2018: Initial version
