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
    for i in range(1, n + 1):
        for l in range(1, w + 1):
            # Ràng buộc At-Least-One (ALO): Người chơi i phải ở ít nhất 1 nhóm trong tuần l
            alo_clause = [get_G_var(vpool, i, k, l) for k in range(1, g + 1)]
            solver.add_clause(alo_clause)

            # Ràng buộc At-Most-One (AMO - Pairwise): Người chơi i ở tối đa 1 nhóm trong tuần l
            for k1 in range(1, g):
                for k2 in range(k1 + 1, g + 1):
                    solver.add_clause([-get_G_var(vpool, i, k1, l),-get_G_var(vpool, i, k2, l)])

def encode_group_size_nsc(solver, vpool, n, g, p, w):

    for k in range(1,g+1):
        for l in range(1, w+1):

            for i in range(1, n):
                solver.add_clause([-get_G_var(vpool, i, k, l), get_R_var(vpool, i, 1, k, l)])

            for i in range(1, p+1):
                solver.add_clause([get_G_var(vpool, i, k, l), -get_R_var(vpool, i, i, k, l)])

            for i in range(2, n):
                for j in range(1, min(i-1, p) + 1):
                    solver.add_clause([-get_R_var(vpool, i-1, j, k, l), get_R_var(vpool, i, j, k, l)])

                for j in range(2, min(i, p) + 1):
                    solver.add_clause([-get_G_var(vpool, i, k, l), -get_R_var(vpool, i-1, j-1, k, l), get_R_var(vpool, i, j, k, l)])

                for j in range (1, min(i-1, p) + 1):
                    solver.add_clause([get_G_var(vpool, i, k, l), get_R_var(vpool, i-1, j, k, l), -get_R_var(vpool, i, j, k, l)])

                for j in range (2, min(i,p)+1):
                    solver.add_clause([get_R_var(vpool, i-1, j-1, k, l), -get_R_var(vpool, i, j, k, l)])

            if p==1:
                solver.add_clause([get_R_var(vpool, n-1, 1, k, l), get_G_var(vpool, n, k, l)])
            else:
                solver.add_clause([get_R_var(vpool, n-1, p, k, l), get_G_var(vpool, n, k, l)])
                solver.add_clause([get_R_var(vpool, n-1, p, k, l), get_R_var(vpool, n-1, p-1, k, l)])

            for i in range(p + 1, n+1):
                solver.add_clause([-get_G_var(vpool, i, k, l), -get_R_var(vpool, i-1, p, k, l)])

def encode_unique_pairings(solver, vpool, n, g, w):
    for l1 in range(1, w):
        for l2 in range(l1 + 1, w + 1):
            for k1 in range(1, g + 1):
                for k2 in range(1, g + 1):
                    for i in range(1, n):
                        for j in range(i + 1, n + 1):
                            solver.add_clause([
                                -get_G_var(vpool, i, k1, l1),
                                -get_G_var(vpool, j, k1, l1),
                                -get_G_var(vpool, i, k2, l2),
                                -get_G_var(vpool, j, k2, l2)
                            ])

def encode_symmetry_breaking_sb1(solver, vpool, g, p):
    for k in range(1, g + 1):
        for i in range((k - 1) * p + 1, k * p + 1):
            solver.add_clause([get_G_var(vpool, i, k, 1)])

def encode_symmetry_breaking_sb2(solver, vpool, g, p, w):
    for l in range(2, w + 1):
        for i in range(1, min(g, p) + 1):
            solver.add_clause([get_G_var(vpool, i, i, l)])

def extract_and_print_schedule(model, vpool, n, g, p, w):
    true_vars = set(var for var in model if var > 0)
    for l in range (1, w + 1):
        week_groups = []
        for k in range(1, g+1):
            group_players = [i for i in range(1, n+1) if get_G_var(vpool, i, k, l) in true_vars]
            week_groups.append(group_players)
        print(f"Tuần {l:2d}: {week_groups}")

def solve_social_golfer_problem(g, p, w):
    n = g*p
    vpool = IDPool()
    solver = Glucose3()

    encode_unique_group_assignment(solver, vpool, n, g, w)
    encode_group_size_nsc(solver, vpool, n, g, p, w)
    encode_unique_pairings(solver, vpool, n, g, w)
    encode_symmetry_breaking_sb1(solver, vpool, g, p)
    encode_symmetry_breaking_sb2(solver, vpool, g, p, w)

    is_sat = solver.solve()
    if is_sat:
        print("Kết quả: SATISFIABLE (Tìm thấy lời giải hợp lệ!)")
        model = solver.get_model()
        extract_and_print_schedule(model, vpool, n, g, p, w)
    else:
        print("Kết quả: UNSATISFIABLE (Không tồn tại lịch thi đấu thỏa mãn!)")

    solver.delete()
    return is_sat

if __name__ == "__main__":
    solve_social_golfer_problem(g=5, p=3, w=5)


