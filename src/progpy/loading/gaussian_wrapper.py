# Copyright © 2021 United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration.  All Rights Reserved.

from collections.abc import Callable
import numpy as np


class GaussianNoiseLoadWrapper():
    """
    .. versionadded:: 1.5.0
    
    This is a simple wrapper for future loading functions that adds gaussian noise to the inputs. It takes a future loading function and a standard deviation and returns a new future loading function that adds gaussian noise to the inputs.

    Arguments
    ----------
    fcn: Callable
        The future loading function to wrap
    std: float
        The standard deviation of the gaussian noise to add

    Keyword Arguments
    -------------------
    seed: {int, SeedSequence, BitGenerator, Generator}, optional
        The seed for random number generator. This can be set to make results repeatable.

    Example
    -------
    >>> from progpy.loading import GaussianNoiseLoadWrapper
    >>> m = SomeModel()
    >>> future_load = GaussianNoiseLoadWrapper(future_load, STANDARD_DEV)
    >>> m.simulate_to_threshold(future_load)
    """
    def __init__(self, fcn: Callable, std: float, seed: int = None):
        self.fcn = fcn
        self.std = std
        self.gen = np.random.default_rng(seed)

    def __call__(self, t: float, x=None):
        """
        Return the load with noise added

        Args:
            t (float): Time (s)
            x (StateContainer, optional): Current state. Defaults to None.

        Returns:
            InputContainer: The load with noise added
        """
        input = self.fcn(t, x)
        for key, value in input.items():
            input[key] = self.gen.normal(value, self.std)
        return input
