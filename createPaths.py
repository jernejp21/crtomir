# -*- coding: utf-8 -*-

#############################################################################
#
# Copyright (c) 2020 Jernej Pangerc
# See LICENCE file for details [1].
#
#############################################################################

import numpy as np
import re


class CreateShapePaths:

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
            if i % 2 == 0:
                path['x'].append(float(points[i]))
            else:
                path['y'].append(float(points[i]))

        return path

    def getPolygonPath(self, element):
        path = {'x': [], 'y': []}

        points = re.split('[, ]', element.points)

        for i in range(len(points)):
            if i % 2 == 0:
                path['x'].append(float(points[i]))
            else:
                path['y'].append(float(points[i]))

        path['x'].append(float(path[0]))
        path['y'].append(float(path[1]))

        return path


class CreatePathPaths:

    def getPathPath(self, element):
        d = element.d
        dString = d.split()

        self.paths = []
        self.path = {'x': [], 'y': []}
        self.currentPosition = {'x': 0, 'y': 0}
        self.startPosition = {'x': 0, 'y': 0}
        isExecute = False
        pathCommand_current = 'm'
        pathCommand_next = None
        array = []
        parameters = []

        for i in range(1, len(dString)):
            if len(dString[i]) == 1 and dString[i] > 'a':
                pathCommand_next = dString[i]
                isExecute = True

            if isExecute:
                isExecute = False

                self.function(pathCommand_current, parameters)
                pathCommand_current = pathCommand_next
                parameters = []
            else:
                array = dString[i].split(',')

                for j in range(len(array)):
                    array[j] = float(array[j])

                parameters.append(array)

        self.function(pathCommand_current, parameters)
        self.paths.append(self.path)

        return self.paths

    def function(self, pathCommand, param):
        if pathCommand == 'm':
            if len(self.path['x']):
                self.paths.append(self.path)
            
            self.path = {'x': [], 'y': []}
            for x, y in param:
                self.currentPosition['x'] += x
                self.currentPosition['y'] += y
                self.startPosition['x'] = self.currentPosition['x']
                self.startPosition['y'] = self.currentPosition['y']
            self.path['x'].append(self.currentPosition['x'])
            self.path['y'].append(self.currentPosition['y'])

        if pathCommand == 'z':
            self.currentPosition['x'] = self.startPosition['x']
            self.currentPosition['y'] = self.startPosition['y']
            self.path['x'].append(self.startPosition['x'])
            self.path['y'].append(self.startPosition['y'])

        if pathCommand == 'l':
            for x, y in param:
                self.currentPosition['x'] += x
                self.currentPosition['y'] += y
                self.path['x'].append(self.currentPosition['x'])
                self.path['y'].append(self.currentPosition['y'])

        if pathCommand == 'h':
            for x in param:
                self.currentPosition['x'] += x[0]
            self.path['x'].append(self.currentPosition['x'])
            self.path['y'].append(self.currentPosition['y'])

        if pathCommand == 'v':
            for y in param:
                self.currentPosition['y'] += y[0]
            self.path['x'].append(self.currentPosition['x'])
            self.path['y'].append(self.currentPosition['y'])

        if pathCommand == 'c':
            # Cubic curve:
            # B(t) = (1-t)^3 * P0 + 3(1-t)^2 * t * P1 + 3(1-t) * t^2 * P2 + t^3 * P3

            counter = 1
            P0 = [self.currentPosition['x'], self.currentPosition['y']]
            for x, y in param:
                if counter % 3 == 1:
                    P1 = [P0[0] + x, P0[1] + y]
                if counter % 3 == 2:
                    P2 = [P0[0] + x, P0[1] + y]
                if counter % 3 == 0:
                    P3 = [P0[0] + x, P0[1] + y]

                if counter == 3:
                    t = np.linspace(0, 1, 11)

                    B_x = (1-t)**3 * P0[0] + 3*(1-t)**2 * t * \
                        P1[0] + 3*(1-t)*t ** 2*P2[0] + t**3 * P3[0]
                    B_y = (1-t)**3 * P0[1] + 3*(1-t)**2 * t * \
                        P1[1] + 3*(1-t)*t ** 2*P2[1] + t**3 * P3[1]

                    self.path['x'].extend(B_x.tolist())
                    self.path['y'].extend(B_y.tolist())

                    P0 = P3
                    counter = 0

                counter += 1

            self.currentPosition['x'] = P0[0]
            self.currentPosition['y'] = P0[1]

        if pathCommand == 'q':
            # Quadratic curve:
            # B(t) = (1-t)^2 * P0 + 2(1-t) * t * P1 + t^2 * P2

            counter = 1
            P0 = [self.currentPosition['x'], self.currentPosition['y']]
            for x, y in param:
                if counter % 2 == 1:
                    P1 = [P0[0] + x, P0[1] + y]
                if counter % 2 == 0:
                    P2 = [P0[0] + x, P0[1] + y]

                if counter == 2:
                    t = np.linspace(0, 1, 11)

                    B_x = (1-t)**2 * P0[0] + 2*(1-t)*t*P1[0] + t**2 * P2[0]
                    B_y = (1-t)**2 * P0[1] + 2*(1-t)*t*P1[1] + t**2 * P2[1]

                    self.path['x'].extend(B_x.tolist())
                    self.path['y'].extend(B_y.tolist())

                    P0 = P2
                    counter = 0

                counter += 1

            self.currentPosition['x'] = P0[0]
            self.currentPosition['y'] = P0[1]
