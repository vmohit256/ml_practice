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
        penalty = self.alpha * np.eye(self.d+1)
        penalty[0, 0] = 0  # remove penalty on bias term
        shifted_gram_matrix = X.T @ X + penalty
        determinant = np.linalg.det(shifted_gram_matrix)
        
        """
        det(X^T X) = 0 iff some features are linearly dependent
        """
        assert determinant != 0, 'X^T X + alpha I is singular. Try increasing alpha. May be some features are redundant / linearly dependent?'

        self.W = np.linalg.inv(shifted_gram_matrix) @ X.T @ y
        self.coef_ = self.W[1:]
        self.intercept_ = self.W[0]

    def _fit_gd(self, X, y, lr=0.01, num_iters=1000):
        """
        For L2 penalty:
        Loss(w) = ||X w - y||^2 + alpha * ||w||^2
        del(Loss) / del(w) = 2 X^T X w - 2 X^T y + 2 alpha w
        Gradient descent step:
        w = w - lr * del(Loss) / del(w)

        For L1 penalty:
        Loss(w) = ||X w - y||^2 / (2 * num_samples) + alpha * ||w||_1
        subgradient, del(Loss) / del(w) = (X^T X w - X^T y)  / (2 * num_samples) + alpha * sign(w)  // sign(x) = 1 if x > 0, -1 if x < 0, 0 if x = 0
        """

        assert self.penalty_norm in ['l2', 'l1'], f'Invalid penalty_norm: {self.penalty_norm}. Must be in ["l2", "l1"]'
        self.N, self.d = X.shape
        self.W = np.zeros((self.d+1, 1))
        X = np.hstack([np.ones((self.N, 1)), X])

        xtx = 2 * X.T @ X
        xty = 2 * X.T @ y
        xty = xty.reshape(-1, 1)

        def get_gradient(W):
            gradient = xtx @ W - xty
            if self.penalty_norm == 'l2':
                # ridge prevents sparsity because gradient of l2 norm is small when w is close to 0. So it doesn't push w to 0
                penalty_gradient = self.alpha * W
                penalty_gradient[0] = 0  # remove penalty on bias term
            elif self.penalty_norm == 'l1':
                # lasso promotes sparsity becasue gradient of l1 norm is big when w is close to 0
                penalty_gradient = self.alpha * np.sign(W)
                penalty_gradient[0] = 0
                gradient = gradient / (2 * self.N)
            return gradient + penalty_gradient
        
        def get_loss(W):
            loss = np.linalg.norm(X @ W - y) ** 2 
            if self.penalty_norm == 'l2':
                norm = np.linalg.norm(W[1:]) ** 2
                penalty = self.alpha * norm
                loss += penalty
            elif self.penalty_norm == 'l1':
                norm = np.linalg.norm(W[1:], ord=1)
                penalty = self.alpha * norm
                loss = loss / (2 * self.N) + penalty
            return loss

        losses = []
        for iteration in range(num_iters):
            gradient = get_gradient(self.W)
            self.W -= lr * gradient
            if iteration % 100 == 0:
                loss = get_loss(self.W)
                losses.append(loss)
                print(f'Iteration: {iteration}, Loss: {loss}')
            if np.linalg.norm(gradient) < 1e-6:
                break
        self.coef_ = self.W[1:, 0]
        self.intercept_ = self.W[0, 0]
        return losses


    def fit(self, X, y):
        if self.solver == 'closed_form':
            return self._fit_closed_form(X, y)
        elif self.solver == 'gd':
            return self._fit_gd(X, y)
        else:
            raise NotImplementedError(f'Solver {self.solver} not implemented.')

    def predict(self, X):
        assert self.W is not None, 'Model not trained yet.'
        return X @ self.coef_ + self.intercept_