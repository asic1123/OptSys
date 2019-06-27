#!/usr/bin/env python

'''
    Module for rendering simple optical outputs using raytracing.
'''

# System imports
#import os
#import sys
#import pdb

# Scipy and related imports
import numpy as np
import scipy.linalg as lin

def propagate_rays(components, rays, lmb=525e-9):
    '''
        Function to propagate rays through a set of components

        Inputs:
            components: List of optical components
            rays: List of 3-tuple of rays with x-coord, y-coord and angle
            lmb: Wavelength of rays in m. Default if 525nm

        Outputs:
            ray_bundles: For N components, this is a list of 3x(N+1) coordinates
                of rays propagated through the components.
    '''
    # Create output ray first
    ncomponents = len(components)
    nrays = len(rays)
    ray_bundles = []

    for idx in range(nrays):
        ray_bundles.append(np.zeros((3, ncomponents+1)))
        ray_bundles[idx][:, 0] = rays[idx]

    # Now propagate each ray through each component
    for r_idx in range(nrays):
        for c_idx in range(1, ncomponents+1):
            ray_bundles[r_idx][:, c_idx] = components[c_idx-1].propagate(
                                            ray_bundles[r_idx][:, c_idx-1],
                                            lmb).reshape(3,)

    # Done, return
    return ray_bundles

def angle_wrap(angle):
    '''
        Wrap angle between -180 to 180

        Inputs:
            angle: In radians

        Outputs:
            wrapped_angle: In radians
    '''
    if angle > np.pi:
        angle -= 2*np.pi
    elif angle < -np.pi:
        angle += 2*np.pi

    return angle

class OpticalObject(object):
    '''
        Generic class definition for optical object. This object is inherited
        to create optical objects such as lenses, mirrors and gratings

        Common properties:
            1. Position of the object
            2. Orientation of the object w.r.t global Y axis
            3. Aperture: Diameter of the object

        Specific properties:
            Lens/mirror: Focal length
            Grating (Transmissive only): Number of groves per mm
            DMD: Deflection angle

        Note: Unless you definitely know what you are doing, do not create
              any object with this class. Look at the objects which inherit
              this class.
    '''
    def __init__(self, aperture, pos, theta, name=None):
        '''
            Generic constructor for optical objects.

            Inputs:
                aperture: Aperture size
                pos: Position of lens in 2D cartesian grid
                theta: Inclination of lens w.r.t Y axis
                name: Name (string) of the optical component. Name will be
                    used for labelling the ocmponents in drawing

            Outputs:
                None.
        '''
        self.theta = theta
        self.pos = pos
        self.aperture = aperture
        self.name = name

        # Create coordinate transformation matrix
        self.H = self.create_xform()
        self.Hinv = lin.inv(self.H)

    def get_intersection(self, orig, theta):
        '''
            Method to get interesection of optical object plane and ray

            Inputs:
                orig: Origin of ray
                theta: Orientation of ray w.r.t x-axis

            Outputs:
                dest: Destination of ray
        '''

        # If theta is nan, it means the ray terminated
        if np.isnan(theta):
            return np.ones((3,1))*float('nan')

        # Transform ray origin to new coordinates
        p = np.array([[orig[0]], [orig[1]], [1]], dtype=np.float64)

        p_new = self.H.dot(p)

        # Similarly find the angle in new coordinate system
        theta_new = theta + self.theta

        # Now compute the intersection
        x_new_tf = 0
        y_new_tf = p_new[1][0] - p_new[0][0]*np.tan(theta_new)

        # Sanity check to see if the interesection lies within the aperture
        if y_new_tf > self.aperture/2.0 or y_new_tf < -self.aperture/2.0:
            flag = float('nan')
        else:
            flag = 1.0

        p_tf = np.array([[x_new_tf], [y_new_tf], [1]])

        # Go back to original system and return result
        p_final = self.Hinv.dot(p_tf)
        p_final[2] = flag

        return p_final

    def propagate(self, point, lmb=None):
        '''
            Function to propagate a ray through the object. Requires an extra
            definition for computing angles

            Inputs:
                point: 3x1 vector with x-coordinate, y-coordinate and angle (rad)
                lmb: Wavelength. Only required for grating
            Outputs:
                dest: 3x1 vector with x-coordinate, y-coordinate and angle (rad)
        '''
        # First get intersection of the point with object plane
        dest = self.get_intersection(point[:2], point[2])

        # Then compute angle
        if np.isnan(dest[2]):
            return dest

        dest[2] = self._get_angle(point, lmb, dest)

        return dest

    def create_xform(self):
        '''
            Function to create transformation matrix for coordinate change

            Inputs:
                None

            Outputs:
                H: 3D transformation matrix
        '''
        R = np.zeros((3, 3))
        T = np.zeros((3, 3))

        # Rotation
        R[0, 0] = np.cos(self.theta)
        R[0, 1] = -np.sin(self.theta)
        R[1, 0] = np.sin(self.theta)
        R[1, 1] = np.cos(self.theta)
        R[2, 2] = 1

        # Translation
        T[0, 0] = 1
        T[0, 2] = -self.pos[0]
        T[1, 1] = 1
        T[1, 2] = -self.pos[1]
        T[2, 2] = 1

        return R.dot(T)

class Mirror(OpticalObject):
    ''' Class definition for Mirror object'''
    def __init__(self, aperture, pos, theta, name='Mirror'):
        '''
            Constructor for Mirror object.

            Inputs:
                aperture: Size of diffraction grating
                pos: Position of diffraction grating
                theta: Inclination of theta w.r.t Y axis
                name: Name of the optical component. If Empty string, generic
                    name is assigned. If None, no name is printed.

            Outputs:
                None.
        '''

        # Initialize parent optical object parameters
        OpticalObject.__init__(self, aperture, pos, theta, name)

        # Extra parameters
        self.type = 'mirror'

    def _get_angle(self, point, lmb, dest):
        '''
            Function to compute angle after propagation through mirror.

            Inputs:
                point: 3-tuple of x-coordinate, y-coordinate and angle (radians)
                lmb: Wavelength of ray, only needed for grating

            Outputs:
                theta: Angle after propagation
        '''

        # Next compute deflection angle
        theta_dest = np.pi - point[2] - 2*self.theta

        return angle_wrap(theta_dest)


