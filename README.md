# calib
camera intrinsic calibration using known planar images (of banknotes) as patterns instead of calibration grids

#example comand:
python calib.py "meptest/*" dataset/EUR10REAR
#example result
Calibration images : 

	  meptest/1436032253627_MEP_IMAGE.jpg

	  meptest/1436032218662_MEP_IMAGE.jpg

	  meptest/1436032228650_MEP_IMAGE.jpg

	  meptest/1436032238648_MEP_IMAGE.jpg

	  meptest/1436032233625_MEP_IMAGE.jpg

	  meptest/1436032213634_MEP_IMAGE.jpg

	  meptest/1436032243618_MEP_IMAGE.jpg

	  meptest/1436032223625_MEP_IMAGE.jpg

	  meptest/1436032248589_MEP_IMAGE.jpg

RMS: 188.66049103

total error:  6.18043324432

camera matrix:

[[  20.19621475    0.          319.5       ]

 [   0.           17.14805632  239.5       ]

 [   0.            0.            1.        ]]

distortion coefficients:  [ -7.65652520e-14  -1.81677294e-09  -2.01062369e-15   6.62709259e-17  2.45107660e-14]

image size  (640, 480)

 focal X :  20.1962147461 pixel 

 focal Y :  17.1480563249 pixel 

 focal exif :  4.6  (mm)

 ccd width :  145.769889903

 X resolution= 4.39048146655 (pixel/mm)

 Y resolution= 3.72783833149

 width = image_width_pixel / X_resolution = 145.769889903  (mm)


#required python libraries
*numpy 
*opencv (with python bindings)
*PIL - Python Image Library
*glob

