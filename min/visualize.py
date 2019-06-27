#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import lines

class Canvas(object):
    '''
        Class definition for canvas to draw components and rays
    '''
    def __init__(self, xlim, ylim, bbox=None, figsize=None):
        '''
            Function to initialize a blank canvas.

            Inputs:
                xlim: Tuple with limits for x-axis
                ylim: Tuple with limits for y-axis
                bbox: Parameters for bounding box. If None, it is automatically
                    assigned.
                figsize: 2-tuple of figure size in inches. If None, figure size
                    is set to 1ftx1ft

            Outputs:
                None
        '''
        # Create an empty matplotlib tool
        if figsize is not None:
            [self._canvas, self.axes] = plt.subplots(figsize=figsize)
        else:
            [self._canvas, self.axes] = plt.subplots()

        # Set x-coordinates and enable grid
        self.xlim = xlim
        self.ylim = ylim

        self.axes.axis('scaled')
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)
        self.axes.grid(True)

        if bbox is None:
            bbox = bbox={'facecolor':'yellow', 'alpha':0.5}

        self.bbox = bbox

    def draw_rays(self, ray_bundles, colors=None):
        '''
            Function to draw rays propagating through the system

            Inputs:
                ray_bundles: List of rays for the components
                colors: Color for each ray. If None, colors are randomly
                        generated
        '''
        if colors is None:
            colors = [np.random.rand(3,1) for i in range(len(ray_bundles))]

        # Make sure number of rays and number of colors are same
        if len(ray_bundles) != len(colors):
            raise ValueError("Need same number of colors as rays")

        for r_idx, ray_bundle in enumerate(ray_bundles):
            # First N-1 points are easy to cover
            for idx in range(ray_bundle.shape[1]-1):
                if ray_bundle[0, idx] == float('nan'):
                    break

                xmin = ray_bundle[0, idx]
                xmax = ray_bundle[0, idx+1]

                ymin = ray_bundle[1, idx]
                ymax = ray_bundle[1, idx+1]

                line = lines.Line2D([xmin, xmax],
                                    [ymin, ymax],
                                    color=colors[r_idx],
                                    linewidth=1.0)
                self.axes.add_line(line)

            # The last point has slope and starting point, so extend it till
            # end of canvas
            xmin = ray_bundle[0, -1]
            ymin = ray_bundle[1, -1]

            if xmin == float('nan'):
                return

            # Brute force by extending line by maximum distance
            dist = np.hypot(self.xlim[1]-self.xlim[0],
                            self.ylim[1]-self.ylim[0])
            xmax = xmin + dist*np.cos(ray_bundle[2, idx+1])
            ymax = ymin + dist*np.sin(ray_bundle[2, idx+1])

            line = lines.Line2D([xmin, xmax],
                                [ymin, ymax],
                                color=colors[r_idx],
                                linewidth=1.0)
            self.axes.add_line(line)
                

    def save(self, savename):
        '''
            Function to save the canvas
        '''
        self._canvas.savefig(savename,
                             bbox_inches='tight',
                             dpi=150)
