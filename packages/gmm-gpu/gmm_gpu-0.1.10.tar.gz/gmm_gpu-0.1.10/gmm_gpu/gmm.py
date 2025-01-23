"""
Provides a GMM class for fitting multiple instances of `Gaussian Mixture Models <https://en.wikipedia.org/wiki/Mixture_model#Gaussian_mixture_model>`_.

This may be useful if you have a large number of independent small problems and you want to fit a GMM on each one.
You can create a single large 3D tensor (three dimensional matrix) with the data for all your instances (i.e. a batch) and then
send the tensor to the GPU and process the whole batch in parallel. This would work best if all the instances have roughly the same number of points.

If you have a single big problem (one GMM instance with many points) that you want to fit using the GPU, maybe `Pomegranate <https://github.com/jmschrei/pomegranate>`_ would be a better option.

### Example usage:
Import pytorch and the GMM class
>>> from gmm_gpu.gmm import GMM
>>> import pytorch

Generate some test data:
We create a batch of 1000 instances, each
with 200 random points. Half of the points
are sampled from distribution centered at
the origin (0, 0) and the other half from
a distribution centered at (1.5, 1.5).
>>> X1 = torch.randn(1000, 100, 2)
>>> X2 = torch.randn(1000, 100, 2) + torch.tensor([1.5, 1.5])
>>> X = torch.cat([X1, X2], dim=1)

Fit the model
>>> gmm = GMM(n_components=2, device='cuda')
>>> gmm.fit(X)

Predict the components:
This will return a matrix with shape (1000, 200) where
each value is the predicted component for the point.
>>> gmm.predict(X)
"""

from functools import reduce

import torch
import numpy as np


def _batch_pdf(X, means, covs, dtype):
    """
    Calculate the pdf for a batch of B sets of N D-dimensional points.

    Parameters
    ----------
    X : torch.tensor
        A tensor with shape (Batch, N-points, Dimensions)
    means : list<torch.tensor>
        Each element represents a component and
        the tensor inside has shape (Batch, Dimensions)
        and contains the mean vectors for the component
        for all instances in the batch.
    covs : list<torch.tensor>
        Each element represents a component and
        the tensor inside has shape (Batch, Dimensions, Dimensions)
        and contains the covariance matrices for the component
        for all instances in the batch.
    dtype : torch.dtype
        type for the data
    """
    B, N, D = X.shape
    diffs = X - means.unsqueeze(1)
    exp = torch.exp(-torch.sum(torch.linalg.solve(covs.float(),
                                                  diffs.float(),
                                                  left=False).to(dtype) * diffs,
                               dim=-1,
                               keepdim=True)/2)
    denom = (2*np.pi)**(-D/2) * covs.float().det().to(dtype)**(-1/2)
    return (denom.view(B, 1, 1) * exp).squeeze(-1)


class GMM:
    def __init__(self,
                 n_components,
                 max_iter=100,
                 device='cuda',
                 tol=0.001,
                 reg_covar=1e-6,
                 dtype=torch.float32,
                 random_seed=None):
        """
        Initialize a Gaussian Mixture Models instance to fit.

        Parameters
        ----------
        n_components : int
            Number of components (gaussians) in the model.
        max_iter : int
            Maximum number of EM iterations to perform.
        device : torch.device
            Which device to be used for the computations
            during the fitting (e.g `'cpu'`, `'cuda'`, `'cuda:0'`).
        tol : float
            The convergence threshold.
        reg_covar : float
            Non-negative regularization added to the diagonal of covariance.
            Allows to assure that the covariance matrices are all positive.
        dtype : torch.dtype
            Data type that will be used in the GMM instance.
        random_seed : int
            Controls the random seed that will be used
            when initializing the model parameters.
        """
        self._n_components = n_components
        self._max_iter = max_iter
        self._device = device
        self._tol = tol
        self._reg_covar = reg_covar
        self._dtype = dtype
        self._rand_generator = torch.Generator(device=device)
        if random_seed:
            self._rand_seed = random_seed
            self._rand_generator.manual_seed(random_seed)
        else:
            self._rand_seed = None


    def fit(self, X):
        """
        Fit the GMM on the given tensor data.

        Parameters
        ----------
        X : torch.tensor
            A tensor with shape (Batch, N-points, Dimensions)
        """
        X = X.to(self._dtype)
        if X.device.type != self._device:
            X = X.to(self._device)

        B, N, D = X.shape

        component_mask = self._init_clusters(X)

        r = torch.full((B, N, self._n_components), np.nan, device=X.device, dtype=self._dtype)
        for k in range(self._n_components):
            r[:, :, k][component_mask == k] = 1

        # This gives us the amount of points per component
        # for each instance in the batch. It's necessary
        # in order to handle missing points (with nan values).
        N_actual = r.nansum(1)
        N_actual_total = N_actual.sum(1)

        converged = torch.full((B,), False)

        self.means = [self._component_means(X, component_mask, k)
                      for k in range(self._n_components)]
        self.covs = [self._get_covs(X, self.means[k], r[:, :, k], N_actual[:, k])
                     for k in range(self._n_components)]
        self._precisions_cholesky = [self._get_precisions_cholesky(covs)
                                    for covs in self.covs]
        # pi list contains the fraction of the dataset for every cluster
        self._pi = [N_actual[:, k]/N_actual_total for k in range(self._n_components)]

        iteration = 0
        while iteration < self._max_iter and not converged.all():

            # === E-STEP ===

            new_r = r.clone()
            for k in range(self._n_components):
                new_r[~converged, :, k] = _estimate_gaussian_prob(
                    X[~converged],
                    self.means[k][~converged],
                    self._precisions_cholesky[k][~converged],
                    self._dtype
                ).mul(self._pi[k][~converged].unsqueeze(1))
            total = new_r.sum(2)
            new_r.div_(total.unsqueeze(2).repeat(1, 1, self._n_components))
            diffs = new_r - r
            r = new_r
            N_actual = r.nansum(1)

            # If all the points are assigned to a single component
            # the components can't change anymore.
            single_component = (N_actual == N_actual_total.unsqueeze(1)).any(1)
            converged[single_component] = True

            # If the change for some instances in the batch
            # are small enough, we mark those instances as
            # converged and do not process them anymore.
            small_change = diffs.nanmean([1, 2]).abs() < self._tol
            converged[small_change] = True

            # === M-STEP ===

            # We update the means, covariances and weights
            # for all instances in the batch that still
            # have not converged.
            for k in range(self._n_components):
                self.means[k][~converged] = torch.div(
                        # the nominator is sum(r*X)
                        (r[~converged, :, k].unsqueeze(2) * X[~converged]).nansum(1),
                        # the denominator is normalizing by the number of valid points
                        N_actual[~converged, k].unsqueeze(1))
                self.covs[k][~converged] = self._get_covs(X[~converged],
                                                          self.means[k][~converged],
                                                          r[~converged, :, k],
                                                          N_actual[~converged, k])
                self._precisions_cholesky[k][~converged] = self._get_precisions_cholesky(self.covs[k][~converged])
                self._pi[k] = N_actual[:, k]/N_actual_total


            iteration += 1


    def predict(self, X):
        """
        Predict the component assignment for the given tensor data.

        Parameters
        ----------
        X : torch.tensor
            A tensor with shape (Batch, N-points, Dimensions)

        Returns
        ----------
        torch.tensor
            tensor of shape (B, N) with component ids as values.
        """
        if X.dtype == self._dtype:
            X = X.to(self._dtype)
        if X.device.type != self._device:
            X = X.to(self._device)
        B, N, D = X.shape
        probs = torch.zeros(B, N, self._n_components, device=X.device)
        for k in range(self._n_components):
            probs[:, :, k] = _estimate_gaussian_prob(X,
                                                     self.means[k],
                                                     self._precisions_cholesky[k],
                                                     self._dtype)
        return probs.argmax(2).cpu()


    def score_samples(self, X):
        """
        Compute the log-likelihood of each point across all instances in the batch.

        Parameters
        ----------
        X : torch.tensor
            A tensor with shape (Batch, N-points, Dimensions)

        Returns
        ----------
        torch.tensor
            tensor of shape (B, N) with the score for each point in the batch.
        """
        if X.device.type != self._device:
            X = X.to(self._device)
        X = X.to(self._dtype)
        B, N, D = X.shape
        log_probs = torch.zeros(B, N, self._n_components, device=X.device)
        for k in range(self._n_components):
            # Calculate weighted log probabilities
            log_probs[:, :, k] = torch.add(
                    self._pi[k].log().unsqueeze(1),
                    _estimate_gaussian_prob(X,
                                            self.means[k],
                                            self._precisions_cholesky[k],
                                            self._dtype).log()
                )
        return log_probs.logsumexp(2).cpu()


    def score(self, X):
        """
        Compute the per-sample average log-likelihood of each instance in the batch.

        Parameters
        ----------
        X : torch.tensor
            A tensor with shape (Batch, N-points, Dimensions)

        Returns
        ----------
        torch.tensor
            tensor of shape (B,) with the log-likelihood for each instance in the batch.
        """
        return self.score_samples(X).nanmean(1).cpu()


    def bic(self, X):
        """
        Calculates the BIC (Bayesian Information Criterion) for the model on the dataset X.

        Parameters
        ----------
        X : torch.tensor
            A tensor with shape (Batch, N-points, Dimensions)

        Returns
        ----------
        torch.tensor
            tensor of shape (B,) with the BIC value for each instance in the Batch.
        """
        scores = self.score(X)
        valid_points = (~X.isnan()).all(2).sum(1)
        return -2 * scores * valid_points + self.n_parameters() * np.log(valid_points)


    def n_parameters(self):
        """
        Returns the number of free parameters in the model for a single instance of the batch.

        Returns
        ----------
        int
            number of parameters in the model
        """
        n_features = self.means[0].shape[1]
        cov_params = self._n_components * n_features * (n_features + 1) / 2.0
        mean_params = n_features * self._n_components
        return int(cov_params + mean_params + self._n_components - 1)


    def _init_clusters(self, X):
        """
        Init the assignment component (cluster) assignment for B sets of N D-dimensional points.

        Parameters
        ----------
        X : torch.tensor
            A tensor with shape (Batch, N-points, Dimensions)
        """
        _, assignment = self._kmeans(X, self._n_components)
        return assignment


    def _component_means(self, X, component_mask, k):
        """
        Get the centers of the gaussian components for B sets of N D-dimensional points.

        Parameters
        ----------
        X : torch.tensor
            A tensor with shape (Batch, N-points, Dimensions)
        component_mask : torch.tensor
            mask of shape (B, N) that assigns each point to a component.
        k : int
            component id
        """
        mask = (component_mask == k).to(self._dtype).unsqueeze(-1)
        sum_masked = (X * mask).nansum(1)
        count_masked = mask.nansum(dim=1)
        count_masked[count_masked == 0] = 1
        return sum_masked / count_masked


    def _kmeans(self, X, n_clusters=2, max_iter=20, tol=0.001):
        """
        Clusters the points in each instance of the batch using k-means.
        Points with nan values are assigned with value -1.

        Parameters
        ----------
        X : torch.tensor
            A tensor with shape (Batch, N-points, Dimensions)
        n_clusters : int
            Number of clusters to find.
        max_iter : int
            Maximum number of iterations to perform.
        tol : float
            The convergence threshold.
        """
        B, N, D = X.shape
        C = n_clusters
        valid_points = ~X.isnan().any(2)
        centers = self._kmeans_pp(X, C, valid_points)
        distances = torch.empty(B, N, C, device=self._device)
        i = 0
        diff = np.inf
        while i < max_iter and diff > tol:
            # Calculate the distance between each point and cluster centers
            for c in range(C):
                distances[:, :, c] = ((X - centers[:, c, :].unsqueeze(1)) ** 2).sum(2) ** 0.5
            # Assign each point to the cluster with closest center
            assignment = distances.argmin(2)
            # Recalculate cluster centers
            new_centers = torch.empty(B, C, D, device=self._device)
            for c in range(C):
                cluster_mask = (assignment == c).unsqueeze(2).repeat(1, 1, D)
                new_centers[:, c, :] = torch.where(cluster_mask, X, np.nan).nanmedian(1).values
            # Estimate how much change we get in the centers
            diff = (new_centers - centers).mean(1).max()
            centers = new_centers
            i += 1
        for c in range(C):
            distances[:, :, c] = ((X - centers[:, c, :].unsqueeze(1)) ** 2).sum(2) ** 0.5
        # Assign each point to the cluster with closest center.
        # Invalid points are assigned -1.
        assignment = torch.where(valid_points, distances.argmin(2), -1)
        return centers, assignment


    def _kmeans_pp(self, X, C, valid_points):
        valid_mask = valid_points.clone()
        B, N, D = X.shape
        centers = torch.empty(B, C, D, device=self._device)
        indices = torch.arange(0, N, device=self._device)
        rand = np.random.default_rng(self._rand_seed)
        std = self._nanstd(X)
        for b in range(B):
            point_index = rand.choice(indices[valid_mask[b]].cpu().numpy())
            point = X[b, point_index, :]
            point_len = (X[b, point_index, :].pow(2).sum(-1) ** 0.5)
            centers[b, 0, :] = std[b]*point/point_len
            valid_mask[b, point_index] = False
            for k in range(1, C):
                prev_center = centers[b, k-1, :]
                distances = ((X[b, valid_mask[b], :] - prev_center) ** 2).sum(-1) ** 0.5
                max_dist_index = distances.argmax()

                # The distances are calculated on a subset of the points
                # so we need to convert the index of the furthest point
                # to the index of the point in the whole dataset.
                point_index = indices[valid_mask[b]][max_dist_index]

                # The standard kmeans++ algorithm selects an initial
                # point at random for the first centroid and then for
                # each cluster selects the point that is furthest away
                # from the previous one. This is prone to selecting
                # outliers that are very far away from all other points,
                # leading to clusters with a single point. In the GMM
                # fitting these clusters are problematic, because variance
                # covariance metrics do not make sense anymore.
                # To ameliorate this, I position the centroid at a point
                # that pointing in the direction of the furthest point,
                # but the length of the vector is equal to the standard
                # deviation in the dataset.
                centers[b, k, :] = std[b] * X[b, point_index, :] / distances[max_dist_index]
        return centers


    def _get_covs(self, X, means, r, nums):
        B, N, D = X.shape
        # C_k = (1/N_k) * sum(r_nk * (x - mu_k)(x - mu_k)^T)
        diffs = X - means.unsqueeze(1)
        summands = r.view(B, N, 1, 1) * torch.matmul(diffs.unsqueeze(3), diffs.unsqueeze(2))
        covs = summands.nansum(1) / nums.view(B, 1, 1)
        # We use the EGV decomposition to substitute
        # covariance matrices that are not positive
        # definite (due to numerical instability)
        # with the closest positive-definite matrix.
        eigvals, eigvecs = torch.linalg.eigh(covs.float())
        eigvals = torch.clamp(eigvals, min=self._reg_covar)
        return eigvecs @ torch.diag_embed(eigvals) @ eigvecs.transpose(-1, -2)


    def _get_precisions_cholesky(self, covs):
        B, D, D = covs.shape
        covs_cholesky = torch.linalg.cholesky(covs)
        precisions_cholesky = torch.linalg.solve_triangular(
                covs_cholesky,
                torch.eye(D, device=self._device).unsqueeze(0).repeat(B, 1, 1),
                upper=False,
                left=True).permute(0, 2, 1)
        return precisions_cholesky.to(self._dtype)


    def _nanstd(self, X):
        valid = torch.sum(~X.isnan().any(2), 1)
        return (((X - X.nanmean(1).unsqueeze(1)) ** 2).nansum(1) / valid.unsqueeze(1)) ** 0.5


def _estimate_gaussian_prob(X, mean, precisions_chol, dtype):
    """
    Compute the probability of a batch of points X under
    a batch of multivariate normal distributions.

    Parameters
    ----------
    X : torch.tensor
        A tensor with shape (Batch, N-points, Dimensions).
        Represents a batch of points.
    mean : torch.tensor
        The means of the distributions. Shape (B, D)
    chol_cov : torch.tensor
        Cholesky decompositions of the covariance matrices. Shape: (B, D, D)
    dtype : torch.dtype
        Data type of the result

    Returns
    ----------
    torch.tensor
        tensor of shape (B, N) with probabilities
    """
    B, N, D = X.shape
    y = torch.bmm(X, precisions_chol) - torch.bmm(mean.unsqueeze(1), precisions_chol)
    log_prob = y.pow(2).sum(2)
    log_det = torch.diagonal(precisions_chol, dim1=1, dim2=2).log().sum(1)
    return torch.exp(
            -0.5 * (D * np.log(2 * np.pi) + log_prob) + log_det.unsqueeze(1))

