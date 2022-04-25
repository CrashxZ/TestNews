import numpy as np
rng = np.random.RandomState(1)
X = rng.randint(5, size=(6, 100))
print(X[2:3])