import numpy as np
import pandas as pd
class XGBClass_Tree:
    def __init__(self, max_depth=3, reg_lambda=1.0, prune_gamma=0.1):
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.prune_gamma = prune_gamma

    def fit(self, x, residual, hessian):
        self.feature = np.array(x)
        self.residual = np.array(residual)
        self.hessian = np.array(hessian)
        self.tree = self._fit_tree(np.arange(x.shape[0]), depth=0)

    def _fit_tree(self, did, depth):
        if depth >= self.max_depth or len(did) <= 1:
            return {"value": self._leaf_value(did)}
        
        best_split = self._find_best_split(did)
        if best_split["gain"] < self.prune_gamma:
            return {"value": self._leaf_value(did)}

        left_idx = did[self.feature[did, best_split["feature"]] <= best_split["split_point"]]
        right_idx = did[self.feature[did, best_split["feature"]] > best_split["split_point"]]

        return {
            "feature": best_split["feature"],
            "split_point": best_split["split_point"],
            "gain": best_split["gain"],
            "left": self._fit_tree(left_idx, depth + 1),
            "right": self._fit_tree(right_idx, depth + 1),
        }

    def _find_best_split(self, did):
        G = self.residual[did].sum()
        H = self.hessian[did].sum()
        best_gain = -np.inf
        best_split = {}

        for feature in range(self.feature.shape[1]):
            values = self.feature[did, feature]
            sorted_idx = np.argsort(values)
            sorted_values = values[sorted_idx]
            sorted_residual = self.residual[did][sorted_idx]
            sorted_hessian = self.hessian[did][sorted_idx]

            G_left, H_left = 0, 0
            G_right, H_right = G, H

            for i in range(1, len(did)):
                G_left += sorted_residual[i - 1]
                H_left += sorted_hessian[i - 1]
                G_right -= sorted_residual[i - 1]
                H_right -= sorted_hessian[i - 1]

                if sorted_values[i] == sorted_values[i - 1]:
                    continue

                gain = (G_left**2 / (H_left + self.reg_lambda) +
                        G_right**2 / (H_right + self.reg_lambda) -
                        G**2 / (H + self.reg_lambda))

                if gain > best_gain:
                    best_gain = gain
                    best_split = {"feature": feature, "split_point": (sorted_values[i] + sorted_values[i - 1]) / 2, "gain": gain}

        return best_split

    def _leaf_value(self, did):
        G = self.residual[did].sum()
        H = self.hessian[did].sum()
        return -G / (H + self.reg_lambda)

    def predict(self, x):
        x = np.array(x,dtype=np.float64)
        def _predict_row(node, row):
            if "value" in node:
                return node["value"]
            if row[node["feature"]] <= node["split_point"]:
                return _predict_row(node["left"], row)
            else:
                return _predict_row(node["right"], row)

        return np.array([_predict_row(self.tree, row) for row in x])