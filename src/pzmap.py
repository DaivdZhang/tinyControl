from .transferfunction import SISO
from .lti import LinearTimeInvariant as LTI
from matplotlib import pyplot as plt
import numpy as np

__all__ = ["pzmap"]


def pzmap(sys_, title='pole-zero map', plot=True):
    if isinstance(sys_, LTI):
        if not isinstance(sys_, SISO):
            raise NotImplementedError('pzmap currently only for SISO')
    else:
        raise TypeError('sys_ should be LTI or sub class of LTI')

    zero = sys_.zero()
    pole = sys_.pole()

    if plot:
        l1 = None
        l2 = None
        if zero.shape[0]:
            l1 = plt.scatter(np.real(zero), np.imag(zero), s=30, marker='o', color='#069af3')
        if pole.shape[0]:
            l2 = plt.scatter(np.real(pole), np.imag(pole), s=30, marker='x', color='#fdaa48')

        plt.legend([l1, l2], ["zero", "pole"])
        plt.grid()
        plt.axvline(x=0, color='black')
        plt.axhline(y=0, color='black')
        plt.xlabel('Real Axis')
        plt.ylabel('Imag Axis')
        plt.title(title)
        plt.show()

    return pole, zero
