from typing import Any, Dict, Tuple

import torch
from torch.utils.data import DataLoader

from diffusionlab.distributions.base import Distribution
from diffusionlab.samplers import Sampler
from diffusionlab.utils import pad_shape_back


class EmpiricalDistribution(Distribution):
    """
    An empirical distribution, i.e., the uniform distribution over a dataset.
    Formally, the distribution is defined as:

    mu(B) = (1/N) * sum_(i=1)^(N) delta(x_i in B)

    where x_i is the ith data point in the dataset, and N is the number of data points.
    """

    def __init__(self, sampler: Sampler, labeled_data: DataLoader):
        super().__init__(sampler, {"labeled_data": labeled_data})
        self.labeled_data: DataLoader = labeled_data

    @classmethod
    def validate_params(cls, dist_params: Dict[str, Any]) -> None:
        assert "labeled_data" in dist_params
        labeled_data = dist_params["labeled_data"]
        assert isinstance(labeled_data, DataLoader)
        assert len(labeled_data) > 0

    @classmethod
    def stateless_x0(
        cls,
        sampler: Sampler,
        dist_params: Dict[str, Any],
        xt: torch.Tensor,
        t: torch.Tensor,
    ) -> torch.Tensor:
        data = dist_params["labeled_data"]

        x_flattened = torch.flatten(xt, start_dim=1, end_dim=-1)  # (N, *D)

        alpha = sampler.alpha(t)  # (N, )
        sigma = sampler.sigma(t)  # (N, )

        softmax_denom = torch.zeros_like(t)  # (N, )
        x0_hat = torch.zeros_like(xt)  # (N, *D)
        for X_batch, y_batch in data:
            X_batch = X_batch.to(xt.device, non_blocking=True)  # (B, *D)
            X_batch_flattened = torch.flatten(X_batch, start_dim=1, end_dim=-1)[
                None, ...
            ]  # (1, B, D*)
            alpha_X_batch_flattened = (
                pad_shape_back(alpha, X_batch_flattened.shape) * X_batch_flattened
            )  # (N, B, D*)
            dists = (
                torch.cdist(x_flattened[:, None, ...], alpha_X_batch_flattened)[
                    :, 0, ...
                ]
                ** 2
            )  # (N, B)
            exp_dists = torch.exp(
                -dists / (2 * pad_shape_back(sigma, dists.shape) ** 2)
            )  # (N, B)
            softmax_denom += torch.sum(exp_dists, dim=1)  # (N, )
            X_batch_singleton = X_batch[None, ...]  # (1, B, *D)
            x0_hat += torch.sum(
                X_batch_singleton * pad_shape_back(exp_dists, X_batch_singleton.shape),
                dim=1,
            )  # (N, *D)

        softmax_denom = torch.maximum(
            softmax_denom,
            torch.tensor(
                torch.finfo(softmax_denom.dtype).eps, device=softmax_denom.device
            ),
        )
        x0_hat = x0_hat / pad_shape_back(softmax_denom, x0_hat.shape)  # (N, *D)
        return x0_hat

    def sample(self, N: int) -> Tuple[torch.Tensor, Any]:
        samples_X = []
        samples_y = []
        device = self.sampler.schedule.device
        while len(samples_X) < N:
            for X_batch, y_batch in self.labeled_data:
                samples_X.append(X_batch.to(device, non_blocking=True))
                samples_y.append(y_batch.to(device, non_blocking=True))
                if len(samples_X) >= N:
                    break
        X = torch.concatenate(samples_X)[:N]
        y = torch.concatenate(samples_y)[:N]
        return X, y
