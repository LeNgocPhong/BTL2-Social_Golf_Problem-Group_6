import os
import pandas as pd
from solvers.sgp_nse_solver import solve_sgp_sat_nse
from solvers.cpsat_solver import solve_sgp_cpsat
from solvers.gurobi_solver import solve_sgp_gurobi

# Danh sách các bộ test (g, p, w) tiêu biểu
INSTANCES = [
    (4, 3, 4), (5, 3, 5), (5, 3, 7),
    (6, 3, 6), (6, 3, 7), (6, 4, 5),
    (7, 3, 7), (7, 4, 5), (8, 4, 6)
]

TIME_LIMIT = 300.0  # Giới hạn 300 giây (5 phút) mỗi instance

SOLVERS = {
    "NSE-NSC (Glucose3)": solve_sgp_sat_nse,
    "CP-SAT (OR-Tools)": solve_sgp_cpsat,
    "ILP (Gurobi)": solve_sgp_gurobi,
}


def main():
    os.makedirs("results", exist_ok=True)
    records = []

    for (g, p, w) in INSTANCES:
        inst_name = f"{g}-{p}-{w}"
        print(f"\n=== Đang chạy Instance: {inst_name} ===")
        for solver_name, solver_fn in SOLVERS.items():
            print(f"  -> Đang chạy {solver_name}...", end=" ", flush=True)
            try:
                res = solver_fn(g, p, w, time_limit=TIME_LIMIT)
            except Exception as e:
                print(f"[ERROR: {type(e).__name__}]")
                res = {
                    "status": "LICENSE_LIMIT" if "size-limited" in str(e).lower() else "ERROR",
                    "encode_time": 0.0,
                    "solve_time": 0.0,
                    "total_time": TIME_LIMIT
                }
            print(f"[{res['status']}] Total: {res['total_time']:.2f}s")
            # Nếu TIMEOUT, gán thời gian bằng ngưỡng TIME_LIMIT để vẽ biểu đồ
            plot_time = res["total_time"] if res["status"] != "TIMEOUT" else TIME_LIMIT

            records.append({
                "Instance": inst_name,
                "Solver": solver_name,
                "Status": res["status"],
                "Encode_Time": round(res["encode_time"], 4),
                "Solve_Time": round(res["solve_time"], 4),
                "Total_Time": round(res["total_time"], 4),
                "Plot_Time": round(plot_time, 4)
            })

            # Lưu ngay sau mỗi lần chạy để tránh mất dữ liệu nếu chương trình bị ngắt
            pd.DataFrame(records).to_csv("results/benchmark_results.csv", index=False)


if __name__ == "__main__":
    main()