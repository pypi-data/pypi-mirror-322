# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by oyvinpet on Wed May 15 20:38:15 2024
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=307.999969482422, 
    height=168.925003051758)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o2 = session.openOdb(name='simple_trussjointc.odb')
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       26
#: Number of Node Sets:          11
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o2)
session.viewports['Viewport: 1'].view.setValues(nearPlane=36.1241, 
    farPlane=85.0409, width=49.09, height=16.9302, viewOffsetX=-3.12133, 
    viewOffsetY=-5.11314)
session.viewports['Viewport: 1'].view.setValues(width=49.1255, height=16.9424, 
    viewOffsetX=-3.4444, viewOffsetY=-5.53778)
session.viewports['Viewport: 1'].view.setValues(nearPlane=45.7028, 
    farPlane=91.1848, width=58.3805, height=20.1343, cameraPosition=(-22.9984, 
    -41.9951, 47.8317), cameraUpVector=(0.110518, 0.834672, 0.539546), 
    cameraTarget=(13.7049, -3.72261, 18.5346), viewOffsetX=-4.09331, 
    viewOffsetY=-6.58108)
session.viewports['Viewport: 1'].view.setValues(nearPlane=44.5023, 
    farPlane=93.0284, width=56.8471, height=19.6054, cameraPosition=(-19.3846, 
    -61.3409, 20.0437), cameraUpVector=(-0.30531, 0.602984, 0.737018), 
    cameraTarget=(10.2389, -8.60914, 16.5731), viewOffsetX=-3.98579, 
    viewOffsetY=-6.40822)
session.viewports['Viewport: 1'].view.setValues(nearPlane=44.4148, 
    farPlane=93.1159, width=56.7353, height=19.5669, cameraPosition=(-13.8146, 
    -64.5574, 18.7159), cameraUpVector=(0.134314, 0.36806, 0.92005), 
    cameraTarget=(15.8089, -11.8256, 15.2453), viewOffsetX=-3.97795, 
    viewOffsetY=-6.39562)
session.viewports['Viewport: 1'].view.setValues(nearPlane=41.4299, 
    farPlane=89.5571, width=52.9225, height=18.2519, cameraPosition=(-43.8609, 
    -40.234, 7.48827), cameraUpVector=(0.28946, -0.0137422, 0.957091), 
    cameraTarget=(10.1538, -13.2872, 12.6387), viewOffsetX=-3.71062, 
    viewOffsetY=-5.96581)
session.viewports['Viewport: 1'].view.setValues(nearPlane=41.9624, 
    farPlane=89.0247, width=53.6027, height=18.4865, cameraPosition=(-45.7067, 
    -36.937, 9.5969), cameraUpVector=(0.126921, 0.315241, 0.940486), 
    cameraTarget=(8.30796, -9.99025, 14.7473), viewOffsetX=-3.75831, 
    viewOffsetY=-6.04249)
session.viewports['Viewport: 1'].view.setValues(nearPlane=48.9274, 
    farPlane=91.2783, width=62.4998, height=21.555, cameraPosition=(11.1435, 
    -61.8415, 37.8709), cameraUpVector=(-0.0264566, 0.659405, 0.751323), 
    cameraTarget=(16.7552, -5.73864, 15.7075), viewOffsetX=-4.38213, 
    viewOffsetY=-7.04544)
session.viewports['Viewport: 1'].view.setValues(nearPlane=43.2745, 
    farPlane=94.4791, width=55.2789, height=19.0646, cameraPosition=(-31.2224, 
    -52.6412, 23.3937), cameraUpVector=(0.304416, 0.367156, 0.878935), 
    cameraTarget=(10.7141, -9.93925, 14.007), viewOffsetX=-3.87583, 
    viewOffsetY=-6.23143)
#: 
#: Element: PART_TRUSS.1012
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1012, 1013
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1014
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1014, 1015
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1120
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1120, 1121
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1213
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1213, 1214
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.202
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 12, 13
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1218
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1218, 1219
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1221
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1221, 1222
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1222
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1222, 1223
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1303
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1303, 1304
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1223
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1223, 1224
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1224
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1224, 1225
#:   S, Mises (Not averaged): NoValue
#: 
#: Element: PART_TRUSS.1225
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1225, 1226
#:   S, Mises (Not averaged): NoValue
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
session.viewports['Viewport: 1'].view.setValues(nearPlane=40.8953, 
    farPlane=96.8583, width=75.6067, height=26.0753, viewOffsetX=5.92808, 
    viewOffsetY=-2.82392)
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       46
#: Number of Node Sets:          18
#: Number of Steps:              1
import sys
sys.path.insert(15, r'c:/Users/oyvinpet/abaqus_plugins/ModelViewPlugin')
import ModelView
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=174.621, 
    farPlane=268.475, width=32.5802, height=13.3101, viewOffsetX=0.433724, 
    viewOffsetY=0.577306)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    uniformScaleFactor=1)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    uniformScaleFactor=10000)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    uniformScaleFactor=100000)
session.viewports['Viewport: 1'].view.setValues(nearPlane=211.066, 
    farPlane=232.031, width=15.5666, height=6.35945, viewOffsetX=-1.85424, 
    viewOffsetY=2.14304)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=195.842, 
    farPlane=247.254, width=64.8866, height=26.5083, viewOffsetX=6.30655, 
    viewOffsetY=-0.236822)
session.odbs['C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb'].close(
    )
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       46
#: Number of Node Sets:          18
#: Number of Steps:              1
session.viewports['Viewport: 1'].view.setValues(nearPlane=41.8029, 
    farPlane=79.1611, width=47.9562, height=19.5917, cameraPosition=(23.5738, 
    -28.7401, 53.9614), cameraUpVector=(0.617744, 0.777698, -0.116525), 
    cameraTarget=(10.5415, -0.185571, 2.14408))
session.viewports['Viewport: 1'].view.setValues(nearPlane=36.9437, 
    farPlane=83.344, width=42.3818, height=17.3144, cameraPosition=(-31.2012, 
    -38.3277, 23.7383), cameraUpVector=(0.401386, 0.516304, 0.756518), 
    cameraTarget=(10.6325, -0.169643, 2.19429))
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
session.viewports['Viewport: 1'].view.setValues(nearPlane=43.146, 
    farPlane=77.1417, width=14.0204, height=5.72778, viewOffsetX=-1.69752, 
    viewOffsetY=-0.461953)
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       46
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=6.98572e+007, 
    farPlane=1.17715e+008, width=8.44621e+006, height=3.45056e+006, 
    viewOffsetX=718118, viewOffsetY=-2.61473e+006)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    deformationScaling=AUTO)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       32
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=271.946, 
    farPlane=444.351, width=5.02473, height=2.05277, viewOffsetX=-1.63476, 
    viewOffsetY=18.2191)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    deformationScaling=AUTO)
session.viewports['Viewport: 1'].view.setValues(nearPlane=331.417, 
    farPlane=374.449, width=35.9763, height=14.6975, viewOffsetX=5.02897, 
    viewOffsetY=21.9011)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.659, 
    farPlane=368.636, width=36.6539, height=14.9743, viewOffsetX=2.49648, 
    viewOffsetY=21.3804)
session.viewports['Viewport: 1'].view.setValues(nearPlane=335.038, 
    farPlane=367.53, width=36.3693, height=14.8581, cameraPosition=(-268.498, 
    -153.954, 153.32), cameraUpVector=(0.605797, 0.466589, 0.644442), 
    cameraTarget=(5.298, -6.1302, -24.0334), viewOffsetX=2.4771, 
    viewOffsetY=21.2144)
session.viewports['Viewport: 1'].view.setValues(nearPlane=335.462, 
    farPlane=367.106, width=32.3083, height=13.199, viewOffsetX=4.17552, 
    viewOffsetY=23.0725)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=332.367, 
    farPlane=364.767, width=32.0103, height=13.0773, cameraPosition=(-326.164, 
    73.212, 65.2459), cameraUpVector=(0.560051, -0.0695338, 0.825535), 
    cameraTarget=(12.4183, -1.22758, -24.7029), viewOffsetX=4.13701, 
    viewOffsetY=22.8596)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=335.497, 
    farPlane=366.972, width=32.3119, height=13.2005, cameraPosition=(-288.654, 
    -181.09, 47.9571), cameraUpVector=(0.40492, 0.33458, 0.850939), 
    cameraTarget=(11.2566, 0.736631, -24.5883), viewOffsetX=4.17597, 
    viewOffsetY=23.0749)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=336.962, 
    farPlane=365.508, width=22.5719, height=9.22137, viewOffsetX=1.93792, 
    viewOffsetY=23.1242)
session.viewports['Viewport: 1'].view.setValues(nearPlane=336.477, 
    farPlane=365.596, width=22.5395, height=9.20811, cameraPosition=(-334.796, 
    38.2845, 62.085), cameraUpVector=(0.514655, -0.324219, 0.793733), 
    cameraTarget=(11.8522, 8.63645, -22.9225), viewOffsetX=1.93513, 
    viewOffsetY=23.0909)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=16 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=334.907, 
    farPlane=368.668, width=22.4343, height=9.16515, cameraPosition=(-332.761, 
    -73.4769, 37.0209), cameraUpVector=(0.442891, 0.278915, 0.852088), 
    cameraTarget=(12.8765, -2.52734, -24.3873), viewOffsetX=1.9261, 
    viewOffsetY=22.9831)
session.viewports['Viewport: 1'].view.setValues(nearPlane=332.551, 
    farPlane=370.603, width=22.2765, height=9.10066, cameraPosition=(-276.645, 
    -189.364, 79.724), cameraUpVector=(0.51672, 0.29894, 0.802269), 
    cameraTarget=(7.78059, 1.75046, -24.4269), viewOffsetX=1.91255, 
    viewOffsetY=22.8214)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=17 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=18 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=19 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=20 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=21 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=22 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=23 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=24 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=25 )
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=26 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=27 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=28 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=29 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=30 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=31 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=32 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=33 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=34 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=35 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=36 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=37 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=38 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=39 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=40 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=41 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=42 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=43 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=44 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=45 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=46 )
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=336.092, 
    farPlane=364.563, width=22.5137, height=9.1976, cameraPosition=(-296.808, 
    103.769, 138.546), cameraUpVector=(0.797169, 0.294439, 0.527094), 
    cameraTarget=(2.43695, -11.4741, -20.9583), viewOffsetX=1.93292, 
    viewOffsetY=23.0644)
session.viewports['Viewport: 1'].view.setValues(nearPlane=331.582, 
    farPlane=369.073, width=50.2618, height=20.5336, viewOffsetX=3.80402, 
    viewOffsetY=20.5312)
session.viewports['Viewport: 1'].view.setValues(nearPlane=334.991, 
    farPlane=372.093, width=50.7784, height=20.7446, cameraPosition=(-268.281, 
    -213.282, 54.1678), cameraUpVector=(0.499317, 0.21777, 0.838605), 
    cameraTarget=(5.65945, 4.57084, -21.7703), viewOffsetX=3.84312, 
    viewOffsetY=20.7423)
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.308, 
    farPlane=369.775, width=35.2728, height=14.4101, viewOffsetX=4.53881, 
    viewOffsetY=21.8492)
session.viewports['Viewport: 1'].view.setValues(nearPlane=342.833, 
    farPlane=364.852, width=35.8506, height=14.6461, cameraPosition=(-61.9844, 
    -303.022, 172.211), cameraUpVector=(0.596503, 0.61556, 0.515044), 
    cameraTarget=(-5.47146, -3.97957, -16.6002), viewOffsetX=4.61315, 
    viewOffsetY=22.2071)
session.viewports['Viewport: 1'].view.setValues(nearPlane=335.904, 
    farPlane=369.5, width=35.126, height=14.3501, cameraPosition=(-343.31, 
    -0.0258822, 17.5852), cameraUpVector=(0.43683, 0.437128, 0.786193), 
    cameraTarget=(12.5193, -8.1611, -22.2758), viewOffsetX=4.51991, 
    viewOffsetY=21.7582)
session.viewports['Viewport: 1'].view.setValues(nearPlane=336.875, 
    farPlane=369.563, width=35.2275, height=14.3916, cameraPosition=(-296.188, 
    -170.309, 53.7023), cameraUpVector=(0.573198, 0.0493439, 0.81793), 
    cameraTarget=(5.18965, 8.2308, -20.8963), viewOffsetX=4.53297, 
    viewOffsetY=21.8211)
session.viewports['Viewport: 1'].view.setValues(nearPlane=345.576, 
    farPlane=363.011, width=36.1374, height=14.7633, cameraPosition=(2.28179, 
    -355.04, -5.04708), cameraUpVector=(-0.106391, 0.384923, 0.916796), 
    cameraTarget=(8.28415, 2.60543, -23.0281), viewOffsetX=4.65005, 
    viewOffsetY=22.3847)
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.493, 
    farPlane=369.267, width=35.2922, height=14.418, cameraPosition=(-246.037, 
    -212.96, 123.361), cameraUpVector=(0.234912, 0.741632, 0.62833), 
    cameraTarget=(9.77245, -8.54349, -21.7088), viewOffsetX=4.54129, 
    viewOffsetY=21.8611)
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.642, 
    farPlane=369.12, width=35.3078, height=14.4244, cameraPosition=(-251.642, 
    -206.432, 122.675), cameraUpVector=(0.474417, 0.506808, 0.719774), 
    cameraTarget=(4.1672, -2.01557, -22.3944), viewOffsetX=4.54329, 
    viewOffsetY=21.8707)
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.055, 
    farPlane=369.964, width=35.2464, height=14.3993, cameraPosition=(-290.245, 
    -166.622, 90.2183), cameraUpVector=(0.434852, 0.473593, 0.765907), 
    cameraTarget=(7.21652, -2.3192, -22.8782), viewOffsetX=4.53539, 
    viewOffsetY=21.8327)
session.animationController.stop()
session.animationController.incrementFrame()
session.animationController.incrementFrame()
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=47 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=48 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=49 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=49 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=48 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=47 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=46 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=45 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=44 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=43 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=42 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=41 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=40 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=39 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=38 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=37 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=36 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=35 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=34 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=33 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=32 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=31 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=30 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=29 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=28 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=27 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=26 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=25 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=24 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=23 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=22 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=21 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=20 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=19 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=18 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=17 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=16 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=336.305, 
    farPlane=371.498, width=35.1679, height=14.3673, cameraPosition=(-14.3288, 
    -353.091, 27.1186), cameraUpVector=(-0.15393, 0.474024, 0.866952), 
    cameraTarget=(9.63402, 0.716444, -23.0363), viewOffsetX=4.52529, 
    viewOffsetY=21.7841)
session.viewports['Viewport: 1'].view.setValues(nearPlane=336.247, 
    farPlane=371.555, width=35.162, height=14.3648, cameraPosition=(-18.9317, 
    -352.71, 27.604), cameraUpVector=(0.0316813, 0.464046, 0.885244), 
    cameraTarget=(5.03115, 1.09699, -22.5509), viewOffsetX=4.52451, 
    viewOffsetY=21.7804)
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.111, 
    farPlane=370.961, width=35.2523, height=14.4017, cameraPosition=(-1.40205, 
    -354.696, -3.14749), cameraUpVector=(0.177289, 0.381407, 0.907247), 
    cameraTarget=(0.80309, 2.99485, -21.0852), viewOffsetX=4.53613, 
    viewOffsetY=21.8364)
session.viewports['Viewport: 1'].view.setValues(nearPlane=334.802, 
    farPlane=372.006, width=35.0109, height=14.3031, cameraPosition=(349.959, 
    -79.926, 62.0314), cameraUpVector=(-0.495577, 0.28176, 0.821593), 
    cameraTarget=(8.92076, -9.04894, -21.2681), viewOffsetX=4.50506, 
    viewOffsetY=21.6868)
session.viewports['Viewport: 1'].view.setValues(nearPlane=336.18, 
    farPlane=369.229, width=35.155, height=14.362, cameraPosition=(16.7169, 
    -303.238, 184.108), cameraUpVector=(-0.194271, 0.801569, 0.565461), 
    cameraTarget=(10.1604, -9.73242, -21.028), viewOffsetX=4.5236, 
    viewOffsetY=21.776)
session.viewports['Viewport: 1'].view.setValues(nearPlane=335.347, 
    farPlane=372.243, width=35.068, height=14.3264, cameraPosition=(-43.7701, 
    -324.179, -130.913), cameraUpVector=(-0.143994, 0.0539958, 0.988104), 
    cameraTarget=(11.3492, 11.6178, -19.2376), viewOffsetX=4.51239, 
    viewOffsetY=21.722)
session.viewports['Viewport: 1'].view.setValues(nearPlane=332.786, 
    farPlane=374.083, width=34.8002, height=14.217, cameraPosition=(-287.891, 
    -171.743, -82.7445), cameraUpVector=(0.485395, -0.404679, 0.775002), 
    cameraTarget=(6.51346, 19.4549, -11.7601), viewOffsetX=4.47793, 
    viewOffsetY=21.5561)
session.viewports['Viewport: 1'].view.setValues(nearPlane=332.835, 
    farPlane=374.035, width=34.8053, height=14.2191, cameraPosition=(-282.693, 
    -177.464, -88.8918), cameraUpVector=(0.262847, -0.129252, 0.956141), 
    cameraTarget=(11.7114, 13.7335, -17.9074), viewOffsetX=4.47858, 
    viewOffsetY=21.5592)
session.viewports['Viewport: 1'].view.setValues(nearPlane=332.73, 
    farPlane=373.044, width=34.7944, height=14.2146, cameraPosition=(-251.497, 
    -192.122, 143.176), cameraUpVector=(0.550521, 0.483296, 0.680699), 
    cameraTarget=(3.036, -1.15416, -21.1819), viewOffsetX=4.47717, 
    viewOffsetY=21.5524)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=332.268, 
    farPlane=373.181, width=34.7461, height=14.1949, cameraPosition=(-250.581, 
    -166.899, 173.563), cameraUpVector=(0.229681, 0.889808, 0.394321), 
    cameraTarget=(10.7833, -14.102, -17.7768), viewOffsetX=4.47096, 
    viewOffsetY=21.5225)
session.viewports['Viewport: 1'].view.setValues(nearPlane=331.78, 
    farPlane=373.73, width=34.6951, height=14.1741, cameraPosition=(-225.118, 
    -205.276, 168.696), cameraUpVector=(0.680495, 0.402984, 0.611989), 
    cameraTarget=(-1.17798, 1.41632, -19.4484), viewOffsetX=4.4644, 
    viewOffsetY=21.4909)
session.viewports['Viewport: 1'].view.setValues(nearPlane=333.305, 
    farPlane=372.782, width=34.8546, height=14.2392, cameraPosition=(-322.041, 
    -119.463, 29.0277), cameraUpVector=(0.32751, 0.454523, 0.828339), 
    cameraTarget=(12.7462, -2.83736, -21.8138), viewOffsetX=4.48492, 
    viewOffsetY=21.5897)
session.viewports['Viewport: 1'].view.setValues(nearPlane=333.171, 
    farPlane=372.465, width=34.8405, height=14.2335, cameraPosition=(-307.07, 
    -97.1732, 125.389), cameraUpVector=(0.576975, 0.439086, 0.688697), 
    cameraTarget=(5.73914, -3.21486, -21.5508), viewOffsetX=4.48311, 
    viewOffsetY=21.581)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].view.setValues(nearPlane=331.642, 
    farPlane=373.677, width=34.6807, height=14.1682, cameraPosition=(-266.729, 
    -201.881, 90.9418), cameraUpVector=(0.346399, 0.554687, 0.756524), 
    cameraTarget=(8.70169, -2.6893, -21.8848), viewOffsetX=4.46254, 
    viewOffsetY=21.482)
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.466, 
    farPlane=367.854, width=3.11205, height=1.27137, viewOffsetX=1.87491, 
    viewOffsetY=20.0681)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
#: 
#: Element: PART_TRUSS.10014
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 10014, 10015
#:   Results: Integration Point values not available
#: 
#: Element: PART_TRUSS.10101
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 2, 10102
#:   Results: Integration Point values not available
#: 
#: Element: PART_TRUSS.10014
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 10014, 10015
#:   Results: Integration Point values not available
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.946, 
    farPlane=367.972, width=4.99404, height=2.04023, viewOffsetX=-0.436494, 
    viewOffsetY=20.0144)
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       33
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=219.413, 
    farPlane=369.886, width=30.2092, height=12.3414, viewOffsetX=-1.33435, 
    viewOffsetY=-12.8613)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    deformationScaling=AUTO)
session.viewports['Viewport: 1'].view.setValues(nearPlane=281.646, 
    farPlane=317.566, width=17.5716, height=7.17859, viewOffsetX=-2.82431, 
    viewOffsetY=-15.9466)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
#: 
#: Node: PART_TRUSS.2
#:                                         1             2             3        Magnitude
#: Base coordinates:                  6.00000e+000,  0.00000e+000,  0.00000e+000,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART_TRUSS.30301
#:                                         1             2             3        Magnitude
#: Base coordinates:                  6.02873e+000,  0.00000e+000,  9.57800e-002,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART_TRUSS.12
#:                                         1             2             3        Magnitude
#: Base coordinates:                  7.50000e+000,  0.00000e+000,  5.00000e+000,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART_TRUSS.11
#:                                         1             2             3        Magnitude
#: Base coordinates:                  2.00000e+000,  0.00000e+000,  5.00000e+000,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART_TRUSS.13
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.25000e+001,  0.00000e+000,  5.00000e+000,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART_TRUSS.2
#:                                         1             2             3        Magnitude
#: Base coordinates:                  6.00000e+000,  0.00000e+000,  0.00000e+000,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART_TRUSS.3
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.00000e+001,  0.00000e+000,  0.00000e+000,      -      
#: No deformed coordinates for current plot.
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
session.viewports['Viewport: 1'].view.setValues(nearPlane=284.806, 
    farPlane=314.466, width=1.68786, height=0.689547, viewOffsetX=-3.32375, 
    viewOffsetY=-15.827)
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       33
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=2, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=3427.94, 
    farPlane=3462.48, width=13.9811, height=5.71172, viewOffsetX=-37.3287, 
    viewOffsetY=-92.5665)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3430.41, 
    farPlane=3460.07, width=1.68322, height=0.687651, viewOffsetX=-36.1489, 
    viewOffsetY=-92.1509)
session.odbs['C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb'].close(
    )
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       34
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=2, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
#: 
#: Element: PART_TRUSS.10101
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 10101, 10102
#:   Results: Integration Point values not available
session.viewports['Viewport: 1'].view.setValues(nearPlane=3424.12, 
    farPlane=3466.36, width=41.1965, height=16.8301, viewOffsetX=-32.1119, 
    viewOffsetY=-94.2294)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3424.41, 
    farPlane=3466, width=32.1669, height=13.1412, viewOffsetX=-32.1088, 
    viewOffsetY=-93.2705)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=3426.96, 
    farPlane=3463.46, width=24.7386, height=10.1065, viewOffsetX=-32.6073, 
    viewOffsetY=-91.6196)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=3425.17, 
    farPlane=3465.41, width=32.114, height=13.1196, viewOffsetX=-28.6975, 
    viewOffsetY=-91.4572)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=16 )
#: 
#: Element: PART_TRUSS.10001
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1, 10002
#:   Results: Integration Point values not available
#: 
#: Element: PART_TRUSS.10003
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 10003, 10004
#:   Results: Integration Point values not available
#: 
#: Element: PART_TRUSS.10004
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 10004, 10005
#:   Results: Integration Point values not available
#: 
#: Element: PART_TRUSS.10014
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 10014, 10015
#:   Results: Integration Point values not available
#: 
#: Element: PART_TRUSS.10015
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 10015, 10016
#:   Results: Integration Point values not available
#: 
#: Element: PART_TRUSS.10001
#:   Type: B31
#:   Material: 
#:   Section: 
#:   Connect: 1, 10002
#:   Results: Integration Point values not available
session.viewports['Viewport: 1'].view.setValues(nearPlane=3428.43, 
    farPlane=3462.83, width=9.83964, height=4.01981, viewOffsetX=-36.4552, 
    viewOffsetY=-92.0088)
session.odbs['C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb'].close(
    )
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       44
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=2, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=3432.72, 
    farPlane=3457.76, width=20.2945, height=8.29097, viewOffsetX=-33.6332, 
    viewOffsetY=-91.3655)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3430.05, 
    farPlane=3460.43, width=3.53452, height=1.44397, viewOffsetX=-38.9722, 
    viewOffsetY=-93.014)
session.odbs['C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb'].close(
    )
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       45
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=1, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=3430.69, 
    farPlane=3459.79, width=31.792, height=12.9881, viewOffsetX=-30.8695, 
    viewOffsetY=-91.835)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=1.29648e+006, 
    farPlane=2.13815e+006, width=66178.4, height=27036, viewOffsetX=7866.05, 
    viewOffsetY=102215)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    deformationScaling=AUTO)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=46.8521, 
    farPlane=74.6725, width=25.5747, height=10.4481, viewOffsetX=-1.06438, 
    viewOffsetY=0.236784)
session.viewports['Viewport: 1'].view.setValues(nearPlane=47.1535, 
    farPlane=74.1156, width=25.7392, height=10.5153, cameraPosition=(-30.6535, 
    -41.3502, 20.2797), cameraUpVector=(0.451508, 0.421011, 0.786696), 
    cameraTarget=(9.8071, -0.189654, 1.05727), viewOffsetX=-1.07123, 
    viewOffsetY=0.238307)
session.odbs['C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb'].close(
    )
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       45
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=50, scalefactor=0.1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=3426, 
    farPlane=3464.47, width=24.3862, height=9.96255, viewOffsetX=-34.109, 
    viewOffsetY=-91.745)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=3430.12, 
    farPlane=3460.36, width=43.1353, height=17.6222, viewOffsetX=-34.1175, 
    viewOffsetY=-91.3678)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    deformationScaling=AUTO)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3433.27, 
    farPlane=3458.52, width=21.8594, height=8.9303, viewOffsetX=-33.0562, 
    viewOffsetY=-91.1947)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
session.viewports['Viewport: 1'].view.setValues(nearPlane=3435.78, 
    farPlane=3454.7, width=2.1646, height=0.884309, viewOffsetX=-39.769, 
    viewOffsetY=-93.2672)
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       44
#: Number of Node Sets:          18
#: Number of Steps:              1
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=10, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=3419.71, 
    farPlane=3470.77, width=57.8836, height=23.6473, viewOffsetX=-22.8739, 
    viewOffsetY=-93.4017)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=22871.1, 
    farPlane=29894.3, width=23.9175, height=9.7711, viewOffsetX=2.085, 
    viewOffsetY=2000.3)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    deformationScaling=AUTO)
session.viewports['Viewport: 1'].view.setValues(nearPlane=42.4897, 
    farPlane=79.1237, width=19.2323, height=7.85703, viewOffsetX=0.269838, 
    viewOffsetY=-0.0340499)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=16 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=17 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=18 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=19 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=20 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=21 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=22 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=23 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=24 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=25 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=26 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=27 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=28 )
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=27 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=26 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=25 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=24 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=23 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=22 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=21 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=20 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=19 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=18 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=17 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=16 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=43.4934, 
    farPlane=78.2562, width=14.8897, height=6.08295, viewOffsetX=-1.06641, 
    viewOffsetY=-0.274795)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=50.5767, 
    farPlane=71.1729, width=6.5083, height=2.65885, viewOffsetX=-0.992396, 
    viewOffsetY=-1.30321)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=43.5374, 
    farPlane=78.2198, width=14.6003, height=5.96469, viewOffsetX=0.359024, 
    viewOffsetY=-2.42688)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=49 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=48 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=47 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=47.5392, 
    farPlane=74.2299, width=22.3652, height=9.13692, viewOffsetX=2.01244, 
    viewOffsetY=0.000788689)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=46 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=45 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=44 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=43 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=42 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=41 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=40 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=39 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=38 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=37 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=36 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=35 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=34 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=33 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=32 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=31 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=30 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=29 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=28 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=27 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=26 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=27 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=28 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=29 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=41.6002, 
    farPlane=80.0722, width=24.4913, height=10.0055, viewOffsetX=3.07151, 
    viewOffsetY=1.18101)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=50 )
#: 
#: Node: PART_TRUSS.10016
#:                                         1             2             3        Magnitude
#: Base coordinates:                  5.90000e+000,  0.00000e+000,  0.00000e+000,      -      
#: Scale:                             2.11664e+002,  2.11664e+002,  2.11664e+002,      -      
#: Deformed coordinates (unscaled):   5.90000e+000,  3.92564e-010,  1.01111e-014,      -      
#: Deformed coordinates (scaled):     5.90000e+000,  8.30917e-008,  2.14015e-012,      -      
#: Displacement (unscaled):           1.12779e-014,  3.92564e-010,  1.01111e-014,  3.92564e-010
#: 
#: Node: PART_TRUSS.1
#:                                         1             2             3        Magnitude
#: Base coordinates:                  0.00000e+000,  0.00000e+000,  0.00000e+000,      -      
#: Scale:                             2.11664e+002,  2.11664e+002,  2.11664e+002,      -      
#: Deformed coordinates (unscaled):   0.00000e+000,  0.00000e+000,  0.00000e+000,      -      
#: Deformed coordinates (scaled):     0.00000e+000,  0.00000e+000,  0.00000e+000,      -      
#: Displacement (unscaled):           0.00000e+000,  0.00000e+000,  0.00000e+000,  0.00000e+000
#: 
#: Nodes for distance: PART_TRUSS.10016, PART_TRUSS.1
#:                                        1             2             3        Magnitude
#: Base distance:                    -5.90000e+000,  0.00000e+000,  0.00000e+000,  5.90000e+000
#: Scale:                             2.11664e+002,  2.11664e+002,  2.11664e+002,      -      
#: Deformed distance (unscaled):     -5.90000e+000, -3.92564e-010, -1.01111e-014,  5.90000e+000
#: Deformed distance (scaled):       -5.90000e+000, -8.30917e-008, -2.14015e-012,  5.90000e+000
#: Relative displacement (unscaled): -1.12779e-014, -3.92564e-010, -1.01111e-014,  3.92564e-010
session.viewports['Viewport: 1'].view.setValues(nearPlane=47.1314, 
    farPlane=74.6182, width=27.32, height=11.1611, viewOffsetX=-0.57748, 
    viewOffsetY=0.75579)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=49 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=48 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=47 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=46 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=47 )
#: 
#: Node: PART_TRUSS.30612
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.39713e+001,  0.00000e+000,  9.57800e-002,      -      
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed coordinates (unscaled):   1.39713e+001,  4.54763e-006,  9.57800e-002,      -      
#: Deformed coordinates (scaled):     1.39713e+001,  9.09526e-006,  9.57800e-002,      -      
#: Displacement (unscaled):           2.62518e-015,  4.54763e-006,  6.63315e-016,  4.54763e-006
#: 
#: Node: PART_TRUSS.30601
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.25287e+001,  0.00000e+000,  4.90422e+000,      -      
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed coordinates (unscaled):   1.25287e+001,  4.54763e-006,  4.90422e+000,      -      
#: Deformed coordinates (scaled):     1.25287e+001,  9.09526e-006,  4.90422e+000,      -      
#: Displacement (unscaled):           1.10941e-015,  4.54763e-006, -3.62969e-015,  4.54763e-006
#: 
#: Nodes for distance: PART_TRUSS.30612, PART_TRUSS.30601
#:                                        1             2             3        Magnitude
#: Base distance:                    -1.44254e+000,  0.00000e+000,  4.80844e+000,  5.02016e+000
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed distance (unscaled):     -1.44254e+000,  0.00000e+000,  4.80844e+000,  5.02016e+000
#: Deformed distance (scaled):       -1.44254e+000,  0.00000e+000,  4.80844e+000,  5.02016e+000
#: Relative displacement (unscaled): -1.51578e-015,  0.00000e+000, -4.29301e-015,  4.55274e-015
session.viewports['Viewport: 1'].view.setValues(nearPlane=49.2477, 
    farPlane=72.5213, width=15.1703, height=6.19757, viewOffsetX=2.00574, 
    viewOffsetY=0.364098)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=46 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=45 )
session.viewports['Viewport: 1'].view.setValues(nearPlane=47.1144, 
    farPlane=74.6351, width=27.4048, height=11.1958, viewOffsetX=0.40614, 
    viewOffsetY=1.41508)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=44 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=43 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=42 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=41 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=40 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=39 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=38 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=37 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=36 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=35 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=36 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=37 )
#: 
#: Node: PART_TRUSS.30601
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.25287e+001,  0.00000e+000,  4.90422e+000,      -      
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed coordinates (unscaled):   1.25287e+001,  1.64980e-019,  4.90422e+000,      -      
#: Deformed coordinates (scaled):     1.25287e+001,  3.29960e-019,  4.90422e+000,      -      
#: Displacement (unscaled):           9.25040e-016,  1.64980e-019, -2.50728e-015,  2.67248e-015
#: 
#: Node: PART_TRUSS.30412
#:                                         1             2             3        Magnitude
#: Base coordinates:                  9.75440e+000,  0.00000e+000,  4.91200e-001,      -      
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed coordinates (unscaled):   9.75440e+000, -3.81656e-004,  4.91200e-001,      -      
#: Deformed coordinates (scaled):     9.75440e+000, -7.63311e-004,  4.91200e-001,      -      
#: Displacement (unscaled):          -2.07925e-015, -3.81656e-004,  2.82967e-016,  3.81656e-004
#: 
#: Nodes for distance: PART_TRUSS.30601, PART_TRUSS.30412
#:                                        1             2             3        Magnitude
#: Base distance:                    -2.77433e+000,  0.00000e+000, -4.41302e+000,  5.21264e+000
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed distance (unscaled):     -2.77433e+000, -3.81656e-004, -4.41302e+000,  5.21264e+000
#: Deformed distance (scaled):       -2.77433e+000, -7.63311e-004, -4.41302e+000,  5.21264e+000
#: Relative displacement (unscaled): -3.00429e-015, -3.81656e-004,  2.79025e-015,  3.81656e-004
session.viewports['Viewport: 1'].view.setValues(nearPlane=49.1548, 
    farPlane=74.5176, width=28.5916, height=11.6806, cameraPosition=(-25.1463, 
    -41.9762, 29.7758), cameraUpVector=(0.378052, 0.632574, 0.675963), 
    cameraTarget=(9.7975, -0.739921, 1.91992), viewOffsetX=0.423729, 
    viewOffsetY=1.47637)
session.viewports['Viewport: 1'].view.setValues(nearPlane=50.1522, 
    farPlane=73.684, width=29.1718, height=11.9176, cameraPosition=(-19.942, 
    -49.7733, 21.5286), cameraUpVector=(0.230666, 0.589723, 0.773964), 
    cameraTarget=(10.0792, -0.761175, 1.67955), viewOffsetX=0.432327, 
    viewOffsetY=1.50633)
session.viewports['Viewport: 1'].view.setValues(nearPlane=54.3173, 
    farPlane=69.5189, width=5.36627, height=2.1923, viewOffsetX=1.18333, 
    viewOffsetY=1.95049)
session.viewports['Viewport: 1'].view.setValues(nearPlane=54.3774, 
    farPlane=69.4588, width=5.37221, height=2.19472, viewOffsetX=1.31506, 
    viewOffsetY=2.38164)
#: 
#: Node: PART_TRUSS.30501
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.00447e+001,  0.00000e+000,  8.94400e-002,      -      
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed coordinates (unscaled):   1.00447e+001,  3.69798e-006,  8.94400e-002,      -      
#: Deformed coordinates (scaled):     1.00447e+001,  7.39595e-006,  8.94400e-002,      -      
#: Displacement (unscaled):          -8.81156e-016,  3.69798e-006,  4.72568e-016,  3.69798e-006
#: 
#: Node: PART_TRUSS.30513
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.24553e+001,  0.00000e+000,  4.91056e+000,      -      
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed coordinates (unscaled):   1.24553e+001,  3.69798e-006,  4.91056e+000,      -      
#: Deformed coordinates (scaled):     1.24553e+001,  7.39595e-006,  4.91056e+000,      -      
#: Displacement (unscaled):           9.62626e-016,  3.69798e-006, -2.47067e-015,  3.69798e-006
#: 
#: Nodes for distance: PART_TRUSS.30501, PART_TRUSS.30513
#:                                        1             2             3        Magnitude
#: Base distance:                     2.41056e+000,  0.00000e+000,  4.82112e+000,  5.39018e+000
#: Scale:                             2.00000e+000,  2.00000e+000,  2.00000e+000,      -      
#: Deformed distance (unscaled):      2.41056e+000,  0.00000e+000,  4.82112e+000,  5.39018e+000
#: Deformed distance (scaled):        2.41056e+000,  0.00000e+000,  4.82112e+000,  5.39018e+000
#: Relative displacement (unscaled):  1.84378e-015,  0.00000e+000, -2.94324e-015,  3.47306e-015
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
session.viewports['Viewport: 1'].view.setValues(nearPlane=49.2851, 
    farPlane=74.5511, width=35.1984, height=14.3797, viewOffsetX=3.17856, 
    viewOffsetY=0.106009)
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       44
#: Number of Node Sets:          18
#: Number of Steps:              1
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=2, scalefactor=-1, 
    step=-1, x_in_or_out='In')
#* IndexError: Sequence index out of range
#* File "c:/Users/oyvinpet/abaqus_plugins/ModelViewPlugin\ModelView.py", line 
#* 52, in ModelViewFunc
#*     firstframe=this_step.frames[1]
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
session.viewports['Viewport: 1'].view.setValues(nearPlane=2875.29, 
    farPlane=4015.19, width=2889.41, height=1180.42, viewOffsetX=-132.563, 
    viewOffsetY=-2.38726)
o1 = session.openOdb(
    name='C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       44
#: Number of Node Sets:          18
#: Number of Steps:              1
session.viewports['Viewport: 1'].view.setValues(nearPlane=42.3671, 
    farPlane=78.7978, width=26.1786, height=10.6948, viewOffsetX=0.842555, 
    viewOffsetY=-0.973228)
import ModelView
ModelView.ModelViewFunc(render_beams='Off', deflection=2, scalefactor=-1, 
    step=-1, x_in_or_out='In')
session.viewports['Viewport: 1'].view.setValues(nearPlane=3429.24, 
    farPlane=3461.24, width=35.8746, height=14.656, viewOffsetX=-31.4062, 
    viewOffsetY=-90.0474)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    deformationScaling=AUTO)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=16 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=17 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=18 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=19 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=20 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=21 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=22 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=23 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=24 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=25 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=26 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=27 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=28 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=29 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=30 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=31 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=32 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=33 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=34 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=35 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=36 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=37 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=36 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=37 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=38 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=37 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=38 )
#: Warning: The output database 'C:/Cloud/OD_OWP/Work/Python/Github/abaqustools/example/trussjointc/simple_trussjointc.odb' disk file has changed.
#: 
#: The current plot operation has been canceled, re-open the file to view the results
