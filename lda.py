
"""
PCA finding the component axes that maximize the variance of our data
LDA additionaly intrested in the axes that maximizes the speration between multiple classes
LDA is suoervised learning (we have y), PCA is unsepurvised
"""

import numpy as np

class LDA:
    def __init__(self, n_components) -> None:
        self.n_components = n_components
        self.linear_descriminants = None
    
    def fit(self, X, y):
        n_features = X.shape[1]
        class_labels = np.unique(y)
        
        mean_overall = np.mean(X, axis=0)
        SW = np.zeros((n_features, n_features))
        SB = np.zeros((n_features, n_features))
        for c in class_labels:
            X_c = X[y==c]
            mean_c = np.mean(X_c, axis=0)
            SW += (X_c - mean_c).T.dot((X_c - mean_c))
            n_c = X_c.shape[0]
            mean_diff = (mean_c - mean_overall)
            
            SB += n_c * (mean_diff).dot(mean_diff.T)
        
        A = np.linalg.inv(SW).dot(SB)
        eigenvalues, eigenvectors = np.linalg.eig(A)
        eigenvectors = eigenvectors.T
        idxs = np.argsort(abs(eigenvalues))[::-1]
        eigenvalues = eigenvalues[idxs]
        eigenvectors = eigenvectors[idxs]
        
        self.linear_descriminants = eigenvectors[0 : self.n_components]
    
    def transform(self, X):
        return np.dot(X, self.linear_descriminants.T)


if __name__ == "__main__":
    # Imports
    import matplotlib.pyplot as plt
    from sklearn import datasets

    data = datasets.load_iris()
    X, y = data.data, data.target

    # Project the data onto the 2 primary linear discriminants
    lda = LDA(2)
    lda.fit(X, y)
    X_projected = lda.transform(X)

    print("Shape of X:", X.shape)
    print("Shape of transformed X:", X_projected.shape)

    x1, x2 = X_projected[:, 0], X_projected[:, 1]

    plt.scatter(
        x1, x2, c=y, edgecolor="none", alpha=0.8, cmap=plt.cm.get_cmap("viridis", 3)
    )

    plt.xlabel("Linear Discriminant 1")
    plt.ylabel("Linear Discriminant 2")
    plt.colorbar()
    plt.show()