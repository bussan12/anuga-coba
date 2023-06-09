#
# earthquake_tsunami function
#
#import okada
"""This function returns a callable object representing an initial water
   displacement generated by a submarine earthqauke.
   
Using input parameters:

Required
 length  along-stike length of rupture area
 width   down-dip width of rupture area
 strike  azimuth (degrees, measured from north) of fault axis
 dip     angle of fault dip in degrees w.r.t. horizontal
 depth   depth to base of rupture area
 
Optional
 x0      x origin (0)
 y0      y origin (0)
 slip    metres of fault slip (1)
 rake    angle of slip (w.r.t. horizontal) in fault plane (90 degrees)

The returned object is a callable okada function that represents
the initial water displacement generated by a submarine earthuake.

"""



from builtins import object
def earthquake_tsunami(length, width, strike, depth, \
                       dip, x0=0.0, y0=0.0, slip=1.0, rake=90.,\
                       domain=None, verbose=False):

    from math import sin, radians

    if domain is not None:
        xllcorner = domain.geo_reference.get_xllcorner()
        yllcorner = domain.geo_reference.get_yllcorner()
        x0 = x0 - xllcorner  # fault origin (relative)
        y0 = y0 - yllcorner
    
    #a few temporary print statements
    if verbose is True:
        print('\nThe Earthquake ...')
        print('\tLength: ', length)
        print('\tDepth: ', depth)
        print('\tStrike: ', strike)
        print('\tWidth: ', width)
        print('\tDip: ', dip)
        print('\tSlip: ', slip)
        print('\tx0: ', x0)
        print('\ty0: ', y0)

    # warning test
    test = width*1000.0*sin(radians(dip)) - depth

    if verbose is True:
        if test > 0.0:
            print('Earthquake source not located below seafloor')
            print('Please check depth')

    return Okada_func(length=length, width=width, dip=dip, \
                      x0=x0, y0=y0, strike=strike, depth=depth, \
                      slip=slip, rake=rake, test=test)


#
# Okada class
#

"""This is a callable class representing the initial water displacment 
   generated by an earthquake.

Using input parameters:

Required
 length  along-stike length of rupture area
 width   down-dip width of rupture area
 strike  azimuth (degrees, measured from north) of fault axis
 dip     angle of fault dip in degrees w.r.t. horizontal
 depth   depth to base of rupture area
 
Optional
 x0      x origin (0)
 y0      y origin (0)
 slip    metres of fault slip (1)
 rake    angle of slip (w.r.t. horizontal) in fault plane (90 degrees)

"""

class Okada_func(object):

    def __init__(self, length, width, dip, x0, y0, strike, \
                 depth, slip, rake, test):
        self.dip = dip
        self.length = length
        self.width = width
        self.x0 = x0
        self.y0 = y0
        self.strike = strike
        self.depth = depth
        self.slip = slip
        self.rake = rake
        self.test = test


    def __call__(self, x, y):
        """Make Okada_func a callable object.

        If called as a function, this object returns z values representing
        the initial 3D distribution of water heights at the points (x,y)
        produced by a submarine mass failure.
        """

        from math import sin, cos, radians, exp, cosh
        from okada import okadatest

        #ensure vectors x and y have the same length
        N = len(x)
        assert N == len(y)

        depth = self.depth
        dip = self.dip
        length = self.length
        width = self.width
        x0 = self.x0
        y0 = self.y0
        strike = self.strike
        dip = self.dip
        rake = self.rake
        slip = self.slip
        
        #double Gaussian calculation assumes water displacement is oriented
        #E-W, so, for displacement at some angle alpha clockwise from the E-W
        #direction, rotate (x,y) coordinates anti-clockwise by alpha

        cosa = cos(radians(strike))
        sina = sin(radians(strike))

        xr = ( (x-x0) * sina + (y-y0) * cosa)
        yr = (-(x-x0) * cosa + (y-y0) * sina) 

        z = okada(xr,yr,depth,length,width,dip,rake,slip)
    
                
        return z

    
