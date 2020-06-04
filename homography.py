#!/usr/bin/env python

import numpy as np
import math

DEG2RAD = math.pi / 180

def fovX_to_focal_length(fovX, imageCenterX):
    focalLength = imageCenterX * (1 / math.tan(fovX * DEG2RAD / 2))
    return focalLength

# p is an array with the 7 parameters
def camera_parameters_to_homography(p, imageCenter):
    camera_parameters_to_homography(p[0], p[1], p[2], p[3], p[4], p[5], p[6], imageCenter)

def camera_parameters_to_homography(fovX, x, y, z, tilt, pan, roll, imageCenter):
    focalLength = fovX_to_focal_length(fovX, imageCenter[0])

    # Compute the rotation+translation matrix between the field frame and the camera frame
    # Using the right-hand rules, the rotation is -90� around the X axis
    rtWorldToCamera = np.zeros((4, 4))
    rtWorldToCamera[0, 0] = 1.0
    rtWorldToCamera[1, 2] = -1.0
    rtWorldToCamera[2, 1] = 1.0
    rtWorldToCamera[0, 3] = -x
    rtWorldToCamera[1, 3] = z
    rtWorldToCamera[2, 3] = -y
    rtWorldToCamera[3, 3] = 1.0

    # Camera rotation matrix
    cameraRotation = np.zeros((4, 4))
    xRotation = -tilt * DEG2RAD
    yRotation = -pan * DEG2RAD
    zRotation = -roll * DEG2RAD
    cx = math.cos(xRotation)
    sx = math.sin(xRotation)
    cy = math.cos(yRotation)
    sy = math.sin(yRotation)
    cz = math.cos(zRotation)
    sz = math.sin(zRotation)

    # Rotate pan - Ry, rotate tilt - Rx, rotate roll - Rz (R = Rz * Rx * Ry)
    cameraRotation[0, 0] = cz * cy - sz * sx * sy
    cameraRotation[0, 1] = -sz * cx
    cameraRotation[0, 2] = cz * sy + sz * sx * cy
    cameraRotation[1, 0] = sz * cy + cz * sx * sy
    cameraRotation[1, 1] = cz * cx
    cameraRotation[1, 2] = sz * sy - cz * sx * cy
    cameraRotation[2, 0] = -cx * sy
    cameraRotation[2, 1] = sx
    cameraRotation[2, 2] = cx * cy
    cameraRotation[3, 3] = 1

    # Camera intrinsic matrix
    intrinsic = np.zeros((4, 4))
    intrinsic[0, 0] = focalLength
    intrinsic[1, 1] = focalLength
    intrinsic[2, 2] = 1.0
    intrinsic[0, 2] = imageCenter[0]
    intrinsic[1, 2] = imageCenter[1]
    intrinsic[3, 3] = 1

    # Camera extrinsic matrix
    extrinsic = np.matmul(cameraRotation, rtWorldToCamera)

    # Camera matrix
    cameraMatrix = np.matmul(intrinsic, extrinsic)

    # Homography
    normalizationValue = cameraMatrix[2, 3]
    outHomography = np.zeros((3, 3))
    outHomography[0, 0] = cameraMatrix[0, 0] / normalizationValue
    outHomography[0, 1] = cameraMatrix[0, 1] / normalizationValue
    outHomography[0, 2] = cameraMatrix[0, 3] / normalizationValue
    outHomography[1, 0] = cameraMatrix[1, 0] / normalizationValue
    outHomography[1, 1] = cameraMatrix[1, 1] / normalizationValue
    outHomography[1, 2] = cameraMatrix[1, 3] / normalizationValue
    outHomography[2, 0] = cameraMatrix[2, 0] / normalizationValue
    outHomography[2, 1] = cameraMatrix[2, 1] / normalizationValue
    outHomography[2, 2] = 1

    return outHomography

def project_point(point, homography):
    pt_aux = np.ones((3,1), dtype=np.float64)
    pt_aux[0] = point[0]
    pt_aux[1] = point[1]

    aux = np.matmul(homography[2,0:], pt_aux)
    xp = np.matmul(homography[0,0:], pt_aux) / aux
    yp = np.matmul(homography[1,0:], pt_aux) / aux

    return [xp, yp]

def project_line(line, homography):
    point0 = project_point([line[0], line[1]], homography)
    point1 = project_point([line[2], line[3]], homography)
    line_out = [point0[0], point0[1], point1[0], point1[1]]

    return line_out
