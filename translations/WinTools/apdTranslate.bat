cd C:\Users\MINI PC\AppData\Roaming\FreeCAD\Mod\AirplaneDesign\translations
WinTools\pylupdate5 ..\InitGui.py -ts InitGui.ts
WinTools\pylupdate5 ..\apdPlane.py -ts apdPlane_py.ts
WinTools\pylupdate5 ..\apdWing.py -ts apdWing_py.ts
WinTools\pylupdate5 ..\apdNacelle.py -ts apdNacelle_py.ts
WinTools\pylupdate5 ..\apdRib.py -ts apdRib_py.ts

WinTools\lupdate ..\resources\apdPlane.ui -ts apdPlane_ui.ts
WinTools\lupdate ..\resources\apdWing.ui -ts apdWing_ui.ts
WinTools\lupdate ..\resources\apdNacelle.ui -ts apdNacelle_ui.ts
WinTools\lupdate ..\resources\apdRib.ui -ts apdRib_ui.ts

WinTools\lconvert -i apdPlane_ui.ts apdWing_ui.ts apdNacelle_ui.ts apdRib_ui.ts ^
   apdPlane_py.ts apdWing_py.ts apdNacelle_py.ts apdRib_py.ts ^
  -o apdWB.ts

:: après traduction
:: lrelease apdWB_fr.ts