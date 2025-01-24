# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by oyvinpet on Tue Aug 22 07:43:23 2023
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=307.999969482422, 
    height=173.0)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o2 = session.openOdb(name='simple_truss.odb')
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       3
#: Number of Node Sets:          4
#: Number of Steps:              2
session.viewports['Viewport: 1'].setValues(displayedObject=o2)
import sys
sys.path.insert(15, r'c:/Users/oyvinpet/abaqus_plugins/ModelViewPlugin')
import ModelView
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=139.057, 
    farPlane=259.422, width=101.604, height=32.8074, viewOffsetX=3.32791, 
    viewOffsetY=-4.9736)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    uniformScaleFactor=2)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=182.673, 
    farPlane=227.437, width=41.1927, height=13.3009, viewOffsetX=1.57544, 
    viewOffsetY=-15.3539)
session.odbs['C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb'].close(
    )
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       3
#: Number of Node Sets:          4
#: Number of Steps:              2
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
#* rom_Transporter::GetClassBagForRead - Table for class "res_Frame" is missing 
#* from the database: 
#* C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb. 
#* The database is corrupt.
#* File "c:/Users/oyvinpet/abaqus_plugins/ModelViewPlugin\ModelView.py", line 
#* 31, in ModelViewFunc
#*     viewport_obj.view.setValues(cameraPosition= (-2390, -2274, 976))
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
#* IndexError: Sequence index out of range
#* File "c:/Users/oyvinpet/abaqus_plugins/ModelViewPlugin\ModelView.py", line 
#* 52, in ModelViewFunc
#*     firstframe=this_step.frames[1]
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
#* rom_Transporter::GetClassBagForRead - Table for class "res_Frame" is missing 
#* from the database: 
#* C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb. 
#* The database is corrupt.
#* File "c:/Users/oyvinpet/abaqus_plugins/ModelViewPlugin\ModelView.py", line 
#* 31, in ModelViewFunc
#*     viewport_obj.view.setValues(cameraPosition= (-2390, -2274, 976))
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
#* rom_Transporter::GetClassBagForRead - Table for class "res_Frame" is missing 
#* from the database: 
#* C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb. 
#* The database is corrupt.
#* File "c:/Users/oyvinpet/abaqus_plugins/ModelViewPlugin\ModelView.py", line 
#* 52, in ModelViewFunc
#*     firstframe=this_step.frames[1]
session.odbs['C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb'].close(
    )
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/truss/simple_truss.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       3
#: Number of Node Sets:          4
#: Number of Steps:              2
