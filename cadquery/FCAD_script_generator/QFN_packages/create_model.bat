taskkill -im freecad.exe /f
@echo OFF
echo cadquery-freecad-module required
@echo ON
cd %~p0
:: start "" "d:\FreeCAD_015\bin\freecad" main_generator.py QFN-28-1EP_6x6mm_Pitch0.65mm
start "" "d:\FreeCAD_015\bin\freecad" main_generator.py %1

::pause