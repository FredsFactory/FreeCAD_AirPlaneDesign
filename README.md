# The FreeCAD Airplane Design Workbench

A FreeCAD workbench dedicated to Airplane Design  

**Warning:** This is highly experimental code. Testers are welcome.

![AirPlaneDesign-UI-screen](resources/AirPlaneDesignWorkbench-V0.3.png)

![WingProfile-screenshot](resources/AirplaneDesign001.png)

## Release Notes
**v0.3**: NACA Rib generator  
**v0.2**: New release with parametric objects based on a dedicated UI  
**v0.1**: Initial release based on sheet  

**v0.001**: 11 July 2018: Initial version

## Prerequisites
* FreeCAD >= v0.17

## Installation
Use the FreeCAD [Addon Manager](https://github.com/FreeCAD/FreeCAD-addons#installing) to install AirPlaneDesign Workbench.

## Usage
After installation a new menu appears:  
1. Create a rib
you can import DAT file or generate NACA Profil.

2.Create a wing

Ability to choose the:  
* Profiles you want to import in the UI (.dat format)  
 **Note:** 2 profiles are installed with the workbench ([eppler 205](wingribprofil/e205.dat) and [eppler 207](wingribprofil/e207.dat)). If you'd like to use different profile(s), simply include said .dat file(s) in to the [`wingribprofil`](wingribprofil/) directory.

## Roadmap

- [ ] Add NACA profil generator
- [ ] Add ability to translate workbench
- [ ] Tutorials

## Feedback
Feedback can be provided via the [discussion thread](https://forum.freecadweb.org/viewtopic.php?f=9&t=38917) on the FreeCAD forums

## License
LGPLv2.1  
See [LICENSE](LICENSE) file
