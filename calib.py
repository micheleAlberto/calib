import numpy as np
import cv2
import re
import sys
from cv2 import calibrateCamera
#cv2.calibrateCamera
#(objectPoints, imagePoints, imageSize[, cameraMatrix[, distCoeffs[, rvecs[, tvecs[, flags[, criteria]]]]]]) 
#retval, cameraMatrix, distCoeffs, rvecs, tvecs
from knnwrap.knn import KnnIndex
from PIL import Image, ExifTags
import glob
import os
detector=cv2.ORB(1600)

class referenceImage:
    @staticmethod
    def build(image,width=None,height=None):
        if not width and not height:
            name,x,y,_discard=re.split('x|y|\.',image)
            width=int(x)
            height=int(y)
            print name
            print 'width ',width,' mm'
            print 'height ',height,' mm'
        if not name:
            name=image.split('.')[0]+'.reference'
        IMG=cv2.imread(image,0)
        img_heigh,img_width=IMG.shape[:2]
        x_scale=img_width/width
        y_scale=img_heigh/height
        kps_cv2, features=detector.detectAndCompute(IMG ,None)
        obj_points=[]
        for kp in kps_cv2:
            _x,_y=kp.pt
            _x=_x/x_scale
            _y=_y/y_scale
            _z=0.
            _o=kp.angle
            _s=kp.octave
            _v=[_x,_y,_z,_s,_o]
            obj_points.append(_v)
        obj_points=np.array(obj_points,np.float32)
        Index=KnnIndex()
        Index.train(features)
        Index.set_dataset_key_map(obj_points)
        Index.save(name)
        return name
    @staticmethod
    def query_image(image,refName,show=False):
        if True:
            IMG=cv2.imread(image,0)
            exif_focal=getFocal(image)
            img_heigh,img_width=IMG.shape[:2]
            query_kps_cv2, query_features=detector.detectAndCompute(IMG,None )
            ref=KnnIndex()
            ref.load(refName)
            dstPoints=[]
            srcPoints=[]
            obj_points=ref.query(query_features,K=8,mapped=True)
            for it,kp in enumerate(query_kps_cv2):
                L=obj_points[it]
                for o_pt in L:
                    dstPoints.append(o_pt[0:3])
                    srcPoints.append(kp.pt)
            dstPoints2d=np.array(dstPoints,np.float32)[:,0:2].copy()
            srcPoints=np.array(srcPoints,np.float32)
            H,mask = cv2.findHomography(srcPoints, dstPoints2d,cv2.RANSAC,5.0)
            obj_pt=[]
            img_pt=[]
            for it,m in enumerate(mask):
                if m:
                    obj_pt.append(dstPoints[it])
                    img_pt.append(srcPoints[it])
            if True:
                obj_pt=np.array(obj_pt)
                img_pt=np.array(img_pt)
                return obj_pt,img_pt
    @staticmethod
    def queryCalibration(images,refName):
        calibration_object_points=[]
        calibration_image_points=[]
        exif_focals=[getFocal(image) for image in images]
        exif_focal=np.average( exif_focals)
        imageSize=cv2.imread(images[0],0).shape[::-1]
        for image in images:
            obj_pt,img_pt=referenceImage.query_image(image,refName)
            if len (img_pt) > 10:
                calibration_object_points.append(obj_pt)
                calibration_image_points.append(img_pt)
        ret, mtx, dist, rvecs, tvecs = (
            cv2.calibrateCamera(
                calibration_object_points, 
                calibration_image_points, 
                imageSize)
            )   
        mean_error = 0
        for i in xrange(len(calibration_object_points)):
            imgpoints2, _ = cv2.projectPoints(calibration_object_points[i], rvecs[i], tvecs[i], mtx, dist)
            imgpoints2.shape=calibration_image_points[i].shape
            error = cv2.norm(calibration_image_points[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            mean_error += error
        print "RMS:", ret   
        print "total error: ", mean_error/len(calibration_object_points)
        print "camera matrix:\n", mtx
        print "distortion coefficients: ", dist.ravel()
        print "image size ",imageSize
        print " focal X : ",mtx[0,0],"pixel "
        print " focal Y : ",mtx[1,1],"pixel "
        print " focal exif : ", exif_focal ," (mm)"
        print " ccd width : ",float(imageSize[0])*exif_focal/mtx[0,0]
        X_res = mtx[0,0]/exif_focal
        print " X resolution=",X_res , "(pixel/mm)"
        print " Y resolution=",mtx[1,1]/exif_focal
        print " width = image_width_pixel / X_resolution =",imageSize[0]/X_res , " (mm)"
            
        
def getFocal(image_file_name):
    tags = {}
    with open(image_file_name, 'rb') as fp:
        img = Image.open(fp)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo is not None:
                for tag, value in exifinfo.items():
                    tags[ExifTags.TAGS.get(tag, tag)] = value
        # Extract Focal Length
    focalN, focalD = tags.get('FocalLength', (0, 1))
    focal_length = float(focalN)/float(focalD)
    return focal_length

def help_and_exit():
    print """
    uses:
    1)python calib.py "PATTERN" REFERENCE
    2)python calib.py "PATTERN" image_namex123y456.jpg

    PATTERN : a glob pattern to specify the calibration images
        es: meptest/*.jpg
    REFERENCE: a reference file
        es: dataset/EUR10REAR
    in the second case a new reference file is built from a given image
    the image name should follow the format
        image_namex{width}y{height}.(jpg|JPG|png|PNG)

    """
    sys.exit(0)
    return 

def main():
    image_pattern=sys.argv[1]
    images=glob.glob(image_pattern)
    print "Calibration images : "
    for im in images:
        print "\t ",im
    reference_name=sys.argv[2]
    _rs=reference_name.split('.')
    if len(_rs)==2 and _rs[1] in ['jpg','JPG','png','PNG']:
        print "Building reference for ",reference_name 
        reference_name = referenceImage.build(reference_name)
    if not os.path.isfile(reference_name):
        print 'invalid reference: ',reference_name
        help_and_exit()
    referenceImage.queryCalibration(images,reference_name)
    
    
    


if __name__ == "__main__":
    main()
