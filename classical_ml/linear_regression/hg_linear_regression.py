import numpy as np

class LinearRegression:
    def __init__(self, penalty_norm='l2', alpha=0.0, solver='closed_form'):
        self.W = None
        self.penalty_norm = penalty_norm
        self.alpha = alpha
        self.solver = solver

    def _fit_closed_form(self, X, y):
        """
        time complexity: O(d^3) for computing inverse of X^T X + alpha I and O(d^2 N) for computing X^T X
        """
        assert self.penalty_norm in ['l2'], f'Invalid penalty_norm: {self.penalty_norm}. Must be in ["l2"]'
        """
        X is N x d, y is N x 1
        Loss: (X w - y)^2 + alpha * w^2 = w^T X^T X w - 2 w^T X^T y + y^T y + alpha * w^T w
        del(Loss) / del(w) = 2 X^T X w - 2 X^T y + 2 alpha w = 0
        => w = (X^T X + alpha I)^-1 X^T y
        """
        self.N, self.d = X.shape
        X = np.hstack([np.ones((self.N, 1)), X])
        shifted_gram_matrix = X.T @ X + self.alpha * np.eye(self.d+1)
        determinant = np.linalg.det(shifted_gram_matrix)
        
        """
        det(X^T X) = 0 iff some features are linearly dependent
        """
        assert determinant != 0, 'X^T X + alpha I is singular. Try increasing alpha. May be some features are redundant / linearly dependent?'

        self.W = np.linalg.inv(shifted_gram_matrix) @ X.T @ y
        self.coef_ = self.W[1:]
        self.intercept_ = self.W[0]

    def fit(self, X, y):
        if self.solver == 'closed_form':
            self._fit_closed_form(X, y)
        else:
            raise NotImplementedError(f'Solver {self.solver} not implemented.')

    def predict(self, X):
        assert self.W is not None, 'Model not trained yet.'
        return X @ self.coef_ + self.intercept_