import time
from ortools.sat.python import cp_model


def solve_sgp_cpsat(g, p, w, time_limit=300.0):
    t_start = time.perf_counter()
    n = g * p
    model = cp_model.CpModel()

    # 1. Tạo biến G_{i,k,l}
    G = {}
    for i in range(1, n + 1):
        for k in range(1, g + 1):
            for l in range(1, w + 1):
                G[i, k, l] = model.NewBoolVar(f"G_{i}_{k}_{l}")

    # 2. Unique Group Assignment: Mỗi người 1 nhóm mỗi tuần
    for i in range(1, n + 1):
        for l in range(1, w + 1):
            model.AddExactlyOne(G[i, k, l] for k in range(1, g + 1))

    # 3. Group Size: Mỗi nhóm có đúng p người
    for k in range(1, g + 1):
        for l in range(1, w + 1):
            model.Add(sum(G[i, k, l] for i in range(1, n + 1)) == p)

    # 4. Unique Pairings: Cặp (i, j) gặp nhau tối đa 1 lần
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            meetings = []
            for l in range(1, w + 1):
                for k in range(1, g + 1):
                    m_ijkl = model.NewBoolVar(f"M_{i}_{j}_{k}_{l}")
                    # G[i,k,l] AND G[j,k,l] => m_ijkl
                    model.AddBoolOr([G[i, k, l].Not(), G[j, k, l].Not(), m_ijkl])
                    meetings.append(m_ijkl)
            model.AddAtMostOne(meetings)

    # 5. Symmetry Breaking SB1 & SB2
    for k in range(1, g + 1):
        for i in range((k - 1) * p + 1, k * p + 1):
            model.Add(G[i, k, 1] == 1)

    for l in range(2, w + 1):
        for i in range(1, min(g, p) + 1):
            model.Add(G[i, i, l] == 1)

    encode_time = time.perf_counter() - t_start

    # Cấu hình bộ giải CP-SAT
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max(0.01, time_limit - encode_time)
    solver.parameters.num_search_workers = 1  # Đặt = 1 để so sánh đơn luồng công bằng với Glucose3

    t_solve_start = time.perf_counter()
    status = solver.Solve(model)
    solve_time = time.perf_counter() - t_solve_start

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        res_status = "SAT"
    elif status == cp_model.INFEASIBLE:
        res_status = "UNSAT"
    else:
        res_status = "TIMEOUT"

    return {
        "status": res_status,
        "encode_time": encode_time,
        "solve_time": solve_time,
        "total_time": encode_time + solve_time
    }