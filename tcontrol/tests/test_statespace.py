from unittest import TestCase
import numpy as np
from tcontrol.statespace import *
from tcontrol.transferfunction import tf, ss2tf


class TestStateSpace(TestCase):
    def setUp(self):
        self.A = np.matrix([[0, 1], [-4, -0.5]])
        self.B = np.matrix([[0.], [1.]])
        self.C = np.matrix([[4., 0.]])
        self.D = np.matrix([0.])
        self.tf_ = tf([4], [1, 0.5, 4])
        self.ss_ = StateSpace(self.A, self.B, self.C, self.D)

    def test___init__(self):
        ss_ = StateSpace(self.A, self.B, self.C, self.D)
        self.assertTrue(ss_.A is self.A)
        self.assertEqual(StateSpace(self.A, self.B, self.C, 0),
                         StateSpace(self.A, self.B, self.C, self.D))
        self.assertRaises(ValueError, StateSpace, self.A, self.C, self.B, 0)
        self.assertRaises(ValueError, StateSpace, self.A, self.C, 0, self.B)

    def test___str__(self):
        pass

    def test___add__(self):
        ss_1 = self.ss_ + self.ss_
        A = [[0, 1, 0, 0], [-4, -.5, 0, 0], [0, 0, 0, 1], [0, 0, -4, -.5]]
        B = [[0], [1], [0], [1]]
        C = [4, 0, 4, 0]
        ss_2 = StateSpace(A, B, C, 0)
        self.assertEqual(ss_1, ss_2)

    def test___mul__(self):
        pass

    def test_pole(self):
        self.assertTrue(np.array_equal(self.ss_.pole(), ss2tf(self.ss_).pole()))

    def test_controllability(self):
        pass

    def test_is_controllable(self):
        self.assertTrue(self.ss_.is_controllable())

    def test_observability(self):
        pass

    def test_is_observable(self):
        self.assertTrue(self.ss_.is_observable())

    def test_dual_system(self):
        _ = StateSpace.dual_system(self.ss_)
        self.assertTrue(np.all(np.equal(_.A.T, self.ss_.A)))
        self.assertTrue(np.all(np.equal(_.C.T, self.ss_.B)))
        self.assertTrue(np.all(np.equal(_.B.T, self.ss_.C)))

    def test_to_controllable_form(self):
        T = self.ss_.to_controllable_form()
        A = T.I*self.A*T
        B = T.I*self.B
        C = self.C*T
        ss_1 = StateSpace(A, B, C, 0)
        ss_2 = StateSpace([[0, 1], [-4, -.5]], [[0], [1]], [4, 0], 0)
        self.assertEqual(ss_1, ss_2)

    def test_ss(self):
        self.assertEqual(ss(self.A, self.B, self.C, self.D), self.ss_)
        self.assertRaises(ValueError, ss, self.A, self.B, self.C, self.D, self.B)
        self.assertEqual(ss(self.tf_), self.ss_)

    def test_tf2ss(self):
        ss_ = tf2ss(self.tf_)
        self.assertTrue(np.all(ss_.A == self.A))
        self.assertTrue(np.all(ss_.B == self.B))
        self.assertTrue(np.all(ss_.C == self.C))
        self.assertRaises(TypeError, tf2ss, ss_)

    def test_ss2tf(self):
        self.assertEqual(ss2tf(self.ss_), self.tf_)

    def test_continuous_to_discrete(self):
        A = np.array([[0, 1], [0, -2]])
        B = np.array([[0], [1]])
        sys_ = StateSpace(A, B, self.C, self.D)
        d_sys_ = continuous_to_discrete(sys_, 0.05)
        continuous_to_discrete(d_sys_, 0.01)
        self.assertWarns(UserWarning, continuous_to_discrete, d_sys_, 0.01)
