#!/usr/bin/env python

import cv2
import numpy as np
import math
import json

from homography import project_line

class SportsField:

    def __init__(self, fieldPath):
        self.lines = {}
        self.type = ""
        self.size = [0,0]

        self.load(fieldPath)
    
    # just used for debug
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def load(self, fieldPath):
        with open(fieldPath) as f:
            data = json.load(f)

        self.type = data['type']
        self.size = data['size']
        self.lines = data['lines']

    def project_to_image(self, homography, image_size, color = (255, 255, 255), thickness = 2, image_background = None):
        if image_background is None:
            image = np.zeros((image_size[1], image_size[0], 3))
        else:
            image = image_background

        for line in self.lines.values():
            for line_segment in line:
                pline = project_line(line_segment, homography)
                cv2.line(image, (int(pline[0]), int(pline[1])), (int(pline[2]), int(pline[3])), color, thickness)

        return image

if __name__ == "__main__":
    field = SportsField("footballFieldModel.json")
    
    image_size = [960, 540]

    homography = np.zeros((3,3), dtype=np.float64)
    homography[0] = [ 1.85073162e+01,  7.40476941e+00,  4.80000000e+02]
    homography[1] = [ 0.00000000e+00, -6.24863124e-01,  3.04377750e+02]
    homography[2] = [ 0.00000000e+00,  1.54266029e-02,  1.00000000e+00]
                
    img = field.project_to_image(homography, image_size)

    print("field: ", field)

    cv2.imshow('image', img)
    cv2.waitKey(0)
