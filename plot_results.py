import os
import pandas as pd
import matplotlib.pyplot as plt
import cnsplots as cns


def plot_grouped_bar_comparison(df):
    """
    1. Biểu đồ cột ghép (Grouped Bar Plot) so sánh thời gian chạy từng Instance.
    Thang đo Logarit (yscale='log') giúp hiển thị rõ sự chênh lệch thời gian từ 0.01s đến 300s.
    """
    # Bỏ palette khỏi cns.figure
    cns.figure(height=160, width=280)

    # Truyền palette trực tiếp vào hàm barplot
    ax = cns.barplot(
        data=df,
        x="Instance",
        y="Plot_Time",
        hue="Solver",
        palette="Set2",
        dodge=True,
        width=0.75
    )

    ax.set_yscale("log")
    ax.set_ylabel("Total Solving Time (s) [Log Scale]")
    ax.set_xlabel("SGP Instances (g-p-w)")
    ax.set_title("Execution Time Comparison: NSE-NSC vs. CP-SAT vs. Gurobi")
    ax.legend(title="Method", bbox_to_anchor=(1.02, 1), loc="upper left")

    cns.savefig("results/plots/1_instance_barplot_log.pdf")
    cns.savefig("results/plots/1_instance_barplot_log.png")
    plt.close()


def plot_cactus_curve(df):
    """
    2. Biểu đồ Cactus Plot (Số lượng bài toán giải thành công tích lũy theo thời gian).
    """
    solved_df = df[df["Status"] != "TIMEOUT"].copy()
    cactus_records = []

    for solver, group in solved_df.groupby("Solver"):
        sorted_times = group["Total_Time"].sort_values().values
        for idx, t in enumerate(sorted_times, start=1):
            cactus_records.append({
                "Solver": solver,
                "Solved_Count": idx,
                "Time": t
            })

    cactus_df = pd.DataFrame(cactus_records)

    cns.figure(height=160, width=220)
    ax = cns.lineplot(
        data=cactus_df,
        x="Solved_Count",
        y="Time",
        hue="Solver",
        palette="tab10",
        markers=True
    )

    ax.set_yscale("log")
    ax.set_xlabel("Number of Solved Instances")
    ax.set_ylabel("Time Limit (s) [Log Scale]")
    ax.set_title("Cactus Plot of Solver Performance")
    ax.legend(title="Method", loc="upper left")

    cns.savefig("results/plots/2_cactus_plot.pdf")
    cns.savefig("results/plots/2_cactus_plot.png")
    plt.close()


def plot_time_distribution_boxplot(df):
    """
    3. Biểu đồ Boxplot kết hợp Stripplot thể hiện trung vị và độ phân tán thời gian giải.
    """
    cns.figure(height=160, width=180)

    ax = cns.boxplot(
        data=df,
        x="Solver",
        y="Plot_Time",
        palette="Pastel1",
        showoutliers=False
    )
    # Vẽ đè các điểm thực tế lên boxplot
    cns.stripplot(
        data=df,
        x="Solver",
        y="Plot_Time",
        color="black",
        size=4,
        alpha=0.6
    )

    ax.set_yscale("log")
    ax.set_xlabel("")
    ax.set_ylabel("Total Time (s) [Log Scale]")
    ax.set_title("Runtime Distribution Across Solvers")
    plt.xticks(rotation=15)

    cns.savefig("results/plots/3_runtime_boxplot.pdf")
    cns.savefig("results/plots/3_runtime_boxplot.png")
    plt.close()


if __name__ == "__main__":
    os.makedirs("results/plots", exist_ok=True)
    df_results = pd.read_csv("results/benchmark_results.csv")

    plot_grouped_bar_comparison(df_results)
    plot_cactus_curve(df_results)
    plot_time_distribution_boxplot(df_results)
    print("Đã xuất toàn bộ biểu đồ thành công vào thư mục results/plots/!")