# The FreeCAD Airplane Design Workbench

A FreeCAD workbench dedicated to Airplane Design  

**Warning:** This is highly experimental code. Testers are welcome.

![AirPlaneDesign-UI-screen](resources/WingResult.png)

![WingProfile-screenshot](resources/AirplaneDesign001.png)

## Release Notes
**v0.3**: NACA Rib generator  
**v0.2**: New release with parametric objects based on a dedicated UI  
**v0.1**: Initial release based on sheet  deprecated!

**v0.001**: 11 July 2018: Initial version

## Prerequisites
* FreeCAD >= v0.17

## Installation
Use the FreeCAD [Addon Manager](https://github.com/FreeCAD/FreeCAD-addons#installing) to install AirPlaneDesign Workbench.

## Usage
After installation a new menu appears with to function :  
1. Create a rib : you can import DAT file or generate NACA Profil.
1.1 Import a DAT File
Simply copy the DAT File in the folde

![DAT folder](resources/Ribsfolder.png)
1.2 Create a Rib based on a DAT file
In the menu AiplaneDesign select create a RIB, the dialog below appears, clic on the tab "Import DAT File".

![DAT folder](resources/RIBSGUI1.png)

Select in the tree the dat file you want to use and define the choord of the rib and clic OK. That's all.
You can change directly in the GUI of the object the Dat File, the Choord (in mm). 

1.3 Use the NACA Generator
You can generate Naca profil 4 or 5 digits. In the menu AiplaneDesign select create a RIB, the dialog below appears, clic on the tab "NACA Generator". Simply fil the NACA Number, the number of points you want to generate and the choord in mm. A preview is automatically generate. 

![RibGUI](resources/RibGUI.png)


2.Create a wing


![WingGUI](resources/WingGUI.png)

The result

![WingGUI](resources/WingResult.png)



Ability to choose the:  
* Profiles you want to import in the UI (.dat format)  
 **Note:** 2 profiles are installed with the workbench ([eppler 205](wingribprofil/e205.dat) and [eppler 207](wingribprofil/e207.dat)). If you'd like to use different profile(s), simply include said .dat file(s) in to the [`wingribprofil`](wingribprofil/) directory.

## Roadmap

- [ ] Add NACA profil generator
- [ ] Improve RIB file selection 
- [ ] Add ability to translate workbench
- [ ] Tutorials

## Feedback
Feedback can be provided via the [discussion thread in english](https://forum.freecadweb.org/viewtopic.php?f=9&t=38917) or [discussion thread in french](https://forum.freecadweb.org/viewtopic.php?f=12&t=40376) on the FreeCAD forums  

## License
LGPLv2.1  
See [LICENSE](LICENSE) file
