#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy.optimize as sp

"""
This code is based on the formalism from Murray & Correia (2011), available
freely at http://arxiv.org/abs/1009.1738. The equation numbers are from this
article, unless otherwise noted.
"""

# Calculates the orbital parameter K (Eq. 66)
def K(m1, m2, n, a, I, e):
    """This is an orbital parameter. Currently not in use by the code."""
    return m2/(m1+m2)*n*a*np.sin(I)/np.sqrt(1.-e**2)

# Calculates Eq. 65
def vr(vz, K, w, f, e):
    """The radial velocities equation."""
    w *= np.pi/180.
    return vz + K*(np.cos(w+f) + e*np.cos(w))

# Calculates the Kepler equation (Eq. 41)
def kepler(E, e, M):
    """The Kepler equation."""
    return E - e*np.sin(E) - M

# Calculates the radial velocities for given orbital parameters
def get_RVs(K, T, t0, w, e, a, VZ, NT, ts):
    """
    Function that produces the radial velocities arrays given the following 
    parameters.

    K = orbit parameter [km/s]
    T = period [d]
    t0 = Time of periastron passage [d]
    w = Argument of periapse [degrees]
    e = eccentricity
    a = semi-major axis
    VZ = proper motion [km/s]
    NT = number of points for one period
    ts = array of times [d]
    """

    # Calculating RVs for one period
    t = np.linspace(t0, t0+T, NT)                    # Time (days)
    M = 2*np.pi/T*(t-t0)                             # Mean anomaly
    E = np.array([sp.newton(func = kepler, x0 = Mk, args = (e, Mk)) \
                 for Mk in M])                       # Eccentric anomaly
    f = 2*np.arctan2(np.sqrt(1.+e)*np.sin(E/2),
                     np.sqrt(1.-e)*np.cos(E/2))      # True anomaly
    RV = np.array([vr(VZ, K, w, fk, e) for fk in f]) # Radial velocities (km/s)

    # Calculating RVs in the specified time interval
    RVs = np.interp(ts, t, RV, period = T)
    return RVs

# Works the same as get_RVs, but the parameters that can't be negative are set
# in log-scale
def log_RVs(lnK, lnT, t0, w, lne, lna, VZ, NT, ts):
    """
    Function that produces the radial velocities arrays given the following
    parameters.

    lnK = ln of the orbit parameter K [km/s]
    lnT = ln of the period [d]
    t0 = Time of periastron passage [d]
    w = Argument of periapse [degrees]
    lne = ln of the eccentricity
    lna = ln of the semi-major axis
    VZ = proper motion [km/s]
    NT = number of points for one period
    ts = array of times [d]
    """
    K = np.exp(lnK)
    T = np.exp(lnT)
    e = np.exp(lne)
    a = np.exp(lna)
    return get_RVs(K, T, t0, w, e, a, VZ, NT, ts)
