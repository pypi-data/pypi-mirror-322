from abc import ABC, abstractmethod
from typing import List, Optional, Union

import numpy as np

from vopy.datasets import Dataset
from vopy.utils import get_closest_indices_from_points, get_noisy_evaluations_chol


# TODO: Revise evaluate abstract method.
# It should both accomodate evaluations that are noisy in themselves and synthetically noisy ones.
# Maybe distinguish real problems from test problems.
class Problem(ABC):
    """
    Abstract base class for defining optimization problems. Provides a template
    for evaluating solutions in a given problem space.

    .. note::
        Classes derived from :class:`Problem` must implement the :meth:`evaluate` method.

    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def evaluate(self, x: np.ndarray) -> np.ndarray:
        """
        Evaluates the problem at a given point (or array of points) :obj:`x`.

        :param x: The input for where to evaluate the problem.
        :type x: np.ndarray
        :return: The evaluation result as an array, representing the objective values at :obj:`x`.
        :rtype: np.ndarray
        """
        pass


class ProblemFromDataset(Problem):
    """
    Define an evaluatable optimization problem using data from a given dataset.

    This class enables the evaluation of points based on nearest neighbor lookup
    from an offline dataset, with optional Gaussian noise.

    :param dataset: The dataset containing input and output data for the problem.
    :type dataset: Dataset
    :param noise_var: The variance of the noise to add to the outputs.
    :type noise_var: float
    """

    def __init__(self, dataset: Dataset, noise_var: float) -> None:
        super().__init__()

        self.dataset = dataset
        self.noise_var = noise_var

        noise_covar = np.eye(self.dataset.out_dim) * noise_var
        self.noise_cholesky = np.linalg.cholesky(noise_covar)

    def evaluate(self, x: np.ndarray, noisy: bool = True) -> np.ndarray:
        """
        Evaluates the problem at given points by finding the nearest points
        in the dataset and optionally adding Gaussian noise.

        :param x: The input points to evaluate, given as an array of shape (N, in_dim).
        :type x: np.ndarray
        :param noisy: If `True`, adds Gaussian noise to the output based on the specified
            noise variance. Defaults to `True`.
        :type noisy: bool
        :return: An array of shape (N, out_dim) representing the evaluated output.
        :rtype: np.ndarray
        """
        if x.ndim <= 1:
            x = x.reshape(1, -1)

        indices = get_closest_indices_from_points(x, self.dataset.in_data, squared=True)
        f = self.dataset.out_data[indices].reshape(len(x), -1)

        if not noisy:
            return f

        y = get_noisy_evaluations_chol(f, self.noise_cholesky)
        return y


class ContinuousProblem(Problem):
    """
    Abstract base class for continuous optimization problems. It includes noise handling for
    outputs based on a specified noise variance. It should have the following attribute defined:

    - :obj:`out_dim`: :type:`int`

    :param noise_var: The variance of the noise to be added to the outputs.
    :type noise_var: float
    """

    out_dim: int

    def __init__(self, noise_var: float) -> None:
        super().__init__()

        self.noise_var = noise_var

        noise_covar = np.eye(self.out_dim) * noise_var
        self.noise_cholesky = np.linalg.cholesky(noise_covar)

    @abstractmethod
    def evaluate_true(self, x: np.ndarray) -> np.ndarray:
        pass

    def evaluate(self, x: np.ndarray, noisy: bool = True) -> np.ndarray:
        """
        Evaluates the problem at given points with optional Gaussian noise.

        :param x: Input points to evaluate, given as an array of shape (N, 2).
        :type x: np.ndarray
        :param noisy: If `True`, adds Gaussian noise to the output based on the specified
            noise variance. Defaults to `True`.
        :type noisy: bool
        :return: A 2D array with evaluated Branin and Currin values for each input,
            with optional noise.
        :rtype: np.ndarray
        """
        if x.ndim == 1:
            x = x.reshape(1, -1)

        f = self.evaluate_true(x)

        if not noisy:
            return f

        y = get_noisy_evaluations_chol(f, self.noise_cholesky)
        return y


def get_continuous_problem(name: str, noise_var: float) -> ContinuousProblem:
    """
    Retrieves an instance of a continuous problem by name. If the
    problem name is not recognized, a ValueError is raised.

    :param name: The name of the continuous problem class to instantiate.
    :type name: str
    :param noise_var: The variance of the noise to apply in the problem.
    :type noise_var: float
    :return: An instance of the specified continuous problem.
    :rtype: ContinuousProblem

    :raises ValueError: If the specified problem name does not exist in the global scope.
    """
    if name in globals():
        return globals()[name](noise_var)

    raise ValueError(f"Unknown continuous problem: {name}")


class BraninCurrin(ContinuousProblem):
    """
    A continuous optimization problem combining the Branin and Currin functions.
    This problem was first utilized by [Belakaria2019]_ for multi-objective
    optimization tasks, where both objectives are evaluated over the same input domain.

    :param noise_var: The variance of the noise added to the output evaluations.
    :type noise_var: float

    References:
        .. [Belakaria2019]
            Belakaria, Deshwal, Doppa.
            Max-value Entropy Search for Multi-Objective Bayesian Optimization.
            Neural Information Processing Systems (NeurIPS), 2019.
    """

    bounds = [(0.0, 1.0), (0.0, 1.0)]
    in_dim = len(bounds)
    out_dim = 2
    domain_discretization_each_dim = 33
    depth_max = 5

    def __init__(self, noise_var: float) -> None:
        super().__init__(noise_var)

    def _branin(self, X):
        """
        Computes the Branin function.

        :param X: The input array of shape (N, 2).
        :type X: np.ndarray
        :return: The evaluated Branin function values.
        :rtype: np.ndarray
        """
        x_0 = 15 * X[..., 0] - 5
        x_1 = 15 * X[..., 1]
        X = np.stack([x_0, x_1], axis=1)

        t1 = X[..., 1] - 5.1 / (4 * np.pi**2) * X[..., 0] ** 2 + 5 / np.pi * X[..., 0] - 6
        t2 = 10 * (1 - 1 / (8 * np.pi)) * np.cos(X[..., 0])
        return t1**2 + t2 + 10

    def _currin(self, X):
        """
        Computes the Currin function.

        :param X: The input array of shape (N, 2).
        :type X: np.ndarray
        :return: The evaluated Currin function values.
        :rtype: np.ndarray
        """
        x_0 = X[..., 0]
        x_1 = X[..., 1]
        x_1[x_1 == 0] += 1e-9
        factor1 = 1 - np.exp(-1 / (2 * x_1))
        numer = 2300 * np.power(x_0, 3) + 1900 * np.power(x_0, 2) + 2092 * x_0 + 60
        denom = 100 * np.power(x_0, 3) + 500 * np.power(x_0, 2) + 4 * x_0 + 20
        return factor1 * numer / denom

    def evaluate_true(self, x: np.ndarray) -> np.ndarray:
        """
        Evaluates the true (noiseless) outputs of the Branin and Currin functions,
        normalized for each output dimension.

        :param x: Input points to evaluate, with shape (N, 2).
        :type x: np.ndarray
        :return: A 2D array with normalized Branin and Currin function values for each input.
        :rtype: np.ndarray
        """
        branin = self._branin(x)
        currin = self._currin(x)

        # Normalize the results
        branin = (branin - 54.3669) / 51.3086
        currin = (currin - 7.5926) / 2.6496

        Y = np.stack([-branin, -currin], axis=1)
        return Y


class DecoupledEvaluationProblem(Problem):
    """
    Wrapper around a :class:`Problem` instance that allows for decoupled evaluations of
    objective functions. This class enables selective evaluation of specific objectives
    by indexing into the output of the underlying problem.

    :param problem: An instance of :class:`Problem` to wrap and decouple evaluations.
    :type problem: Problem
    """

    def __init__(self, problem: Problem) -> None:
        super().__init__()
        self.problem = problem

    def evaluate(
        self,
        x: np.ndarray,
        evaluation_index: Optional[Union[int, List[int]]] = None,
        **evaluate_kwargs: dict,
    ) -> np.ndarray:
        """
        Evaluates the underlying problem at the given points and returns either the full
        output or specific objectives as specified by `evaluation_index`.

        :param x: The input points to evaluate, given as an array of shape (N, in_dim).
        :type x: np.ndarray
        :param evaluation_index: Specifies which objectives to return. Can be:
            - `None` (default) to return all objectives,
            - an `int` to return a specific objective across all points,
            - a list of indices to return specific objectives for each point.
        :type evaluation_index: Optional[Union[int, List[int]]]
        :param evaluate_kwargs: Additional keyword arguments to pass to the evaluation function of
            the underlying problem.
        :type evaluate_kwargs: dict
        :return: An array of evaluated values, either the full output or specific objectives.
        :rtype: np.ndarray
        :raises ValueError: If :obj:`evaluation_index` has an invalid format or length.
        """
        if (
            evaluation_index is not None
            and not isinstance(evaluation_index, int)
            and len(x) != len(evaluation_index)
        ):
            raise ValueError(
                "evaluation_index must; be None, have type int or have the same length as x."
            )

        values = self.problem.evaluate(x, **evaluate_kwargs)

        if evaluation_index is None:
            return values

        if isinstance(evaluation_index, int):
            return values[:, evaluation_index]

        evaluation_index = np.array(evaluation_index, dtype=np.int32)
        return values[np.arange(len(evaluation_index)), evaluation_index]
