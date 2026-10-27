from pysat.solvers import Glucose3
from pysat.formula import IDPool

def get_G_var(vpool, i, k, l):
    # biến chính, True nếu người chơi i ở trong nhóm k trong tuần l.
    return vpool.id(f"G_{i}_{k}_{l}")

def get_R_var(vpool, i, j, k, l):
    # biến phụ, True nếu có ít nhất j người chơi tính từ người chơi 1 đến người chơi i
    # ở trong nhóm k trong tuần l
    return vpool.id(f"R_{i}_{j}_{k}_{l}")

