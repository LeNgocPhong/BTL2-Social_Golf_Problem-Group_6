from pysat.solvers import Glucose3
from pysat.formula import IDPool

def get_G_var(vpool, i, k, l):
    # biến chính, True nếu người chơi i ở trong nhóm k trong tuần l.
    return vpool.id(f"G_{i}_{k}_{l}")

def get_R_var(vpool, i, j, k, l):
    # biến phụ, True nếu có ít nhất j người chơi tính từ người chơi 1 đến người chơi i
    # ở trong nhóm k trong tuần l
    return vpool.id(f"R_{i}_{j}_{k}_{l}")

def encode_unique_group_assignment(solver, vpool, n, g, w):
    # Mỗi người chơi i trong tuần l chỉ được xếp vào duy nhất 1 nhóm k.
    for i in range(1, n+1):
        for l in range(1, w+1):
            # Ràng buộc At-Least-One (ALO): Người chơi i phải ở ít nhất 1 nhóm trong tuần l.
            alo_clause = [get_G_var(vpool, i, k, l) for k in range(1, g+1)]
            solver.add_clause(alo_clause)

    # Ràng buộc At_Most_One (AMO): Người chơi i ở tối đa 1 nhóm trong tuần l.
    for k1 in range(1,g):
        for k2 in range(k1+1, g+1):
            solver.add_clause([-get_G_var(vpool, i, k1, l), -get_G_var(vpool, i, k2, l)])