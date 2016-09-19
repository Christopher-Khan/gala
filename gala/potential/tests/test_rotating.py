# coding: utf-8
"""
    Test rotating potentials
"""

from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import time

# Third-party
import astropy.units as u
import pytest

# This project
from ..core import CompositePotential
from ..builtin import LogarithmicPotential, RotatingPotential
from ..ccompositepotential import CCompositePotential
from ...dynamics import CartesianPhaseSpacePosition
from ...units import solarsystem, galactic, DimensionlessUnitSystem
from ...integrate import DOPRI853Integrator
from .helpers import PotentialTestBase, CompositePotentialTestBase

# class RotatingPotentialTestBase(CompositePotentialTestBase):

#     def test_orbit_integration(self):
#         """
#         Make we can integrate an orbit in this potential
#         """
#         w0 = self.w0

#         t1 = time.time()
#         orbit = self.potential.integrate_orbit(w0, dt=1E-3, n_steps=10000,
#                                                Integrator=DOPRI853Integrator)
#         print("Integration time (10000 steps): {}".format(time.time() - t1))

#         us = self.potential.units
#         w0 = CartesianPhaseSpacePosition(pos=w0[:self.ndim]*us['length'],
#                                          vel=w0[self.ndim:]*us['length']/us['time'])
#         orbit = self.potential.integrate_orbit(w0, dt=1E-3, n_steps=10000,
#                                                Integrator=DOPRI853Integrator)

#         import matplotlib.pyplot as plt
#         orbit.plot()
#         plt.show()

#     @pytest.mark.skipif(True, "TODO: implement Hessian")
#     def test_hessian(self):
#         pass

# # class TestRestrictedThreeBody(RotatingPotentialTestBase):
#     # TODO: need to support coordinate transforms as well, then can offset
#     #       the point masses and to the restricted 3-body problem
#     # p1 = KeplerPotential(m=1., units=DimensionlessUnitSystem(),
#     #                      transform=XX)
#     # p2 = KeplerPotential(m=1., units=DimensionlessUnitSystem(),
#     #                      transform=XX)

# class TestLogBar(RotatingPotentialTestBase):
#     # See: Chapter 3, Pg. 184, Binney & Tremaine 2008
#     log_pot = LogarithmicPotential(units=DimensionlessUnitSystem(), v_c=1., r_h=0.03,
#                                    q1=1., q2=0.8, q3=1.)
#     potential = RotatingPotential(log_pot, Omega=[0,0,1])
#     w0 = [0.01,0,0,0,0.1,0]

def test_derp():
    import matplotlib.pyplot as plt

    log_pot = LogarithmicPotential(units=DimensionlessUnitSystem(), v_c=1., r_h=0.1,
                                   q1=1., q2=1., q3=1.)

    rot_pot = RotatingPotential(log_pot, Omega=[0,0,1])

    w0 = CartesianPhaseSpacePosition(pos=[0.5,0.,0],
                                     vel=[0.,0.025,0.])
    w = rot_pot.integrate_orbit(w0, dt=1E-2, n_steps=100,
                                Integrator=DOPRI853Integrator)

    w0_inertial = rot_pot.to_inertial_frame(w0, t=0.)
    w_inertial = log_pot.integrate_orbit(w0_inertial, dt=1E-2, n_steps=100,
                                         Integrator=DOPRI853Integrator)
    w_trans_inertial = rot_pot.to_inertial_frame(w)

    w.plot()
    plt.title("rotating")

    w_inertial.plot()
    plt.title("inertial")

    w_trans_inertial.plot()
    plt.title("rotating transform to inertial")

    plt.show()
    return



    from scipy.signal import argrelmin

    y_minima, = argrelmin(w.pos[1]**2)
    sos_idx = y_minima[w.vel[1][y_minima] > 0]


    w.plot()

    plt.figure()
    plt.scatter(w.pos[0][sos_idx], w.vel[0][sos_idx], marker='.', alpha=0.2, color='k')

    plt.show()
