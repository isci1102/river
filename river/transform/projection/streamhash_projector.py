import math

from river.base.transformer import BaseTransformer
from river.utils.math import dotvecmat


class StreamhashProjector(BaseTransformer):
    """Streamhash projection method  from Manzoor et. al.that is similar (or equivalent) to SparseRandomProjection. :cite:`xstream` The implementation is taken from the `cmuxstream-core repository <https://github.com/cmuxstream/cmuxstream-core>`_.

    Parameters
    ----------
    num_components
        Number of dimensions that the target will be projected into.
    density
        Density parameter of the streamhash projection.

    """

    def __init__(self, num_components, density=1 / 3.0):
        self.keys = list(range(0, num_components, 1))
        self.constant = math.sqrt(1.0 / density) / math.sqrt(num_components)
        self.density = density
        self.n_components = num_components

    def learn_one(self, X):
        """Learn particular (next) timestep's features to train the projector.

        Parameters
        ----------
        X
            Input feature vector.

        """

        return X

    def transform_one(self, X):
        """Projects particular (next) timestep's vector to (possibly) lower dimensional space.

        Parameters
        ----------
        X
            Input feature vector.

        Returns
        -------
        projected_X
            Projected feature vector.
        """

        ndim = len(X)

        feature_names = [str(i) for i in range(ndim)]

        R = {}
        for f in feature_names:
            for k in self.keys:
                R[(k, int(f))] = self._hash_string(k, f)

        R_T = {}
        for ind in R.keys():
            R_T[ind[1], ind[0]] = R[ind]
        R_T_ord = dict(sorted(R_T.items()))

        Y = dotvecmat(X, R_T_ord)
        return Y

    def _hash_string(self, k, s):
        import mmh3

        hash_value = int(mmh3.hash(s, signed=False, seed=k)) / (2.0**32 - 1)
        s = self.density
        if hash_value <= s / 2.0:
            return -1 * self.constant
        elif hash_value <= s:
            return self.constant
        else:
            return 0
