import numpy as np
def get_cnn_input():
    return {"input":np.random.randn(16, 3, 32, 32).astype(np.float32).tolist()}
