# The FreeCAD Airplane Design Workbench

A FreeCAD workbench dedicated to Airplane Design  

**Warning:** This is highly experimental code. Testers are welcome.

![WingProfile-screenshot](resources/AirplaneDesign001.png)

![AirPlaneDesign-UI-screen](resources/AirPlaneDesignWorkbench-V0.3.png)

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
1. Wizard: do not use this yet! (**Note:** UI under heavy development!)  
2. Init New Plane: initializes a new document which includes a spreadsheet with many parameters  
3. Generate Wing: generate the wing based on the parameters in the spreadsheet AirPlaneData  
4. Generate Wing Rib: (**Note:** before using this function make a clone of the wing and apply the function on this clone) The parameters are currently in [`generateWingRibs.py`](generateWingRibs.py) and are currently being outsourced to the spreadsheet. **Note:** Under development

Ability to choose the:  
* Decomposition of the wing panel: cell B3  
* Number of profile: cell B4  
* Profiles you want to import: B6 (.dat format)  
 **Note:** 2 profiles are installed with the workbench ([eppler 205](wingribprofil/e205.dat) and [eppler 207](wingribprofil/e207.dat)). If you'd like to use different profile(s), simply include said .dat file(s) in to the [`wingribprofil`](wingribprofil/) directory.

## Roadmap

- [ ] Add ability to translate workbench
- [ ] Tutorials

## Feedback
Feedback can be provided via the [discussion thread](https://forum.freecadweb.org/viewtopic.php?f=9&t=38917) on the FreeCAD forums

## License
LGPLv2.1  
See [LICENSE](LICENSE) file
