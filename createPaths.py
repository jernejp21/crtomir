# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (c) 2020 Jernej Pangerc
## See LICENCE file for details [1].
##
#############################################################################

import numpy as np
import re

class CreatePaths:

    def getRectPath(self, element):
        path = {'x': [], 'y': []}
        x = float(element.x)
        y = float(element.y)
        rx = float(element.rx)
        ry = float(element.ry)
        width = float(element.width)
        height = float(element.height)

        # perform an absolute moveto operation to location (x+rx,y)
        path['x'].append(x + rx)
        path['y'].append(y)

        # perform an absolute horizontal lineto operation to location (x+width-rx,y)
        path['x'].append(x + width - rx)
        path['y'].append(y)

        # perform an absolute elliptical arc operation to coordinate (x+width,y+ry)
        if rx != 0:
            angle = np.linspace(np.pi*3/2, np.pi*2, 12)
            _x = x + width - rx + rx*np.cos(angle)
            _y = y + ry + ry*np.sin(angle)
            path['x'].extend(_x[1:-1].tolist())
            path['y'].extend(_y[1:-1].tolist())
        
        # perform an absolute vertical lineto to location (x+width,y+height-ry)
        path['x'].append(x + width)
        path['y'].append(y + height - ry)
        
        # perform an absolute elliptical arc operation to coordinate (x+width-rx,y+height)
        if rx != 0:
            angle = np.linspace(0, np.pi/2, 12)
            _x = x + width - rx + rx*np.cos(angle)
            _y = y + height - ry + ry*np.sin(angle)
            path['x'].extend(_x[1:-1].tolist())
            path['y'].extend(_y[1:-1].tolist())

        # perform an absolute horizontal lineto to location (x+rx,y+height)
        path['x'].append(x + rx)
        path['y'].append(y + height)

        # perform an absolute elliptical arc operation to coordinate (x,y+height-ry)
        if rx != 0:
            angle = np.linspace(np.pi/2, np.pi, 12)
            _x = x + rx + rx*np.cos(angle)
            _y = y + height - ry + ry*np.sin(angle)
            path['x'].extend(_x[1:-1].tolist())
            path['y'].extend(_y[1:-1].tolist())

        # perform an absolute absolute vertical lineto to location (x,y+ry)
        path['x'].append(x)
        path['y'].append(y + ry)
        
        # perform an absolute elliptical arc operation to coordinate (x+rx,y)
        if rx != 0:
            angle = np.linspace(np.pi, np.pi*3/2, 12)
            _x = x + rx + rx*np.cos(angle)
            _y = y + ry + ry*np.sin(angle)
            path['x'].extend(_x[1:-1].tolist())
            path['y'].extend(_y[1:-1].tolist())

        return path

    def getCircPath(self, element):
        path = {'x': [], 'y': []}
        r = float(element.r)
        cx = float(element.cx)
        cy = float(element.cy)

        angle = np.linspace(0, 2*np.pi, 50)
        x = cx + r*np.cos(angle)
        y = cy + r*np.sin(angle)

        path['x'] = x.tolist()
        path['y'] = y.tolist()

        return path

    def getEllipsePath(self, element):
        path = {'x': [], 'y': []}
        rx = float(element.rx)
        ry = float(element.ry)
        cx = float(element.cx)
        cy = float(element.cy)

        angle = np.linspace(0, 2*np.pi, 50)
        x = cx + rx*np.cos(angle)
        y = cy + ry*np.sin(angle)

        path['x'] = x.tolist()
        path['y'] = y.tolist()

        return path

    def getLinePath(self, element):
        path = {'x': [], 'y': []}
        x1 = float(element.x1)
        x2 = float(element.x2)
        y1 = float(element.y1)
        y2 = float(element.y2)

        path['x'].append(x1)
        path['x'].append(x2)
        path['y'].append(y1)
        path['y'].append(y2)

        return path

    def getPolylinePath(self, element):
        path = {'x': [], 'y': []}

        points = re.split('[, ]', element.points)

        for i in range(len(points)):
            if i%2 == 0:
                path['x'].append(float(points[i]))
            else:
                path['y'].append(float(points[i]))

        return path

    def getPolygonPath(self, element):
        path = {'x': [], 'y': []}

        points = re.split('[, ]', element.points)

        for i in range(len(points)):
            if i%2 == 0:
                path['x'].append(float(points[i]))
            else:
                path['y'].append(float(points[i]))

        path['x'].append(float(path[0]))
        path['y'].append(float(path[1]))

        return path
