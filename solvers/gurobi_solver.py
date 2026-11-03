import time
import gurobipy as gp
from gurobipy import GRB


def solve_sgp_gurobi(g, p, w, time_limit=300.0):
    t_start = time.perf_counter()
    n = g * p

    # Khởi tạo môi trường Gurobi tắt log ra màn hình
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()
    model = gp.Model("SGP_ILP", env=env)

    # 1. Tạo biến G_{i,k,l}
    G = model.addVars(
        range(1, n + 1), range(1, g + 1), range(1, w + 1),
        vtype=GRB.BINARY, name="G"
    )

    # 2. Unique Group Assignment
    for i in range(1, n + 1):
        for l in range(1, w + 1):
            model.addConstr(gp.quicksum(G[i, k, l] for k in range(1, g + 1)) == 1)

    # 3. Group Size
    for k in range(1, g + 1):
        for l in range(1, w + 1):
            model.addConstr(gp.quicksum(G[i, k, l] for i in range(1, n + 1)) == p)

    # 4. Unique Pairings (Tuyến tính hóa bằng biến phụ M)
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            m_l = []
            for l in range(1, w + 1):
                # m biểu thị cặp (i, j) gặp nhau ở tuần l (chỉ phụ thuộc i, j, l)
                m = model.addVar(vtype=GRB.BINARY, name=f"M_{i}_{j}_{l}")
                for k in range(1, g + 1):
                    # Nếu cả i và j đều ở nhóm k tuần l thì m bắt buộc phải bằng 1
                    model.addConstr(m >= G[i, k, l] + G[j, k, l] - 1)
                m_l.append(m)
            # Tổng số tuần cặp (i, j) gặp nhau không vượt quá 1
            model.addConstr(gp.quicksum(m_l) <= 1)

    # 5. Symmetry Breaking SB1 & SB2
    for k in range(1, g + 1):
        for i in range((k - 1) * p + 1, k * p + 1):
            model.addConstr(G[i, k, 1] == 1)

    for l in range(2, w + 1):
        for i in range(1, min(g, p) + 1):
            model.addConstr(G[i, i, l] == 1)

    model.update()
    encode_time = time.perf_counter() - t_start

    # Cấu hình tham số giải (1 thread để công bằng với Glucose 3)
    model.setParam("TimeLimit", max(0.01, time_limit - encode_time))
    model.setParam("Threads", 1)

    t_solve_start = time.perf_counter()
    model.optimize()
    solve_time = time.perf_counter() - t_solve_start

    if model.Status == GRB.OPTIMAL or model.SolCount > 0:
        res_status = "SAT"
    elif model.Status == GRB.INFEASIBLE:
        res_status = "UNSAT"
    else:
        res_status = "TIMEOUT"

    model.dispose()
    env.dispose()

    return {
        "status": res_status,
        "encode_time": encode_time,
        "solve_time": solve_time,
        "total_time": encode_time + solve_time
    }