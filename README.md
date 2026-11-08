# Exact SAT Solving for the Social Golfer Problem via New Sequential Counter Encoding

Dự án nghiên cứu, hiện thực và đánh giá thực nghiệm phương pháp New SAT Encoding (NSE) kết hợp bộ đếm lực lượng New Sequential Counter (NSC) cho bài toán tối ưu hóa tổ hợp Social Golfer Problem (SGP). Kỹ thuật này sử dụng biểu diễn 3 chỉ số ($G_{i,k,l}$), lan truyền hai chiều duy trì tính nhất quán cung (GAC) và áp dụng các vị từ phá vỡ đối xứng tĩnh (SB1, SB2). Mô hình được đối sánh hiệu năng trực tiếp với hai công cụ công nghiệp là Google OR-Tools (CP-SAT) và Gurobi Optimizer (ILP).

---

### Cấu trúc thư mục

```text
BTL2-Social_Golf_Problem-Group_6/
├── solvers/
│   ├── nse_nsc_solver.py    # Mô hình NSE-NSC (Glucose 3 / PySAT)
│   ├── cpsat_solver.py      # Mô hình CP-SAT (Google OR-Tools)
│   └── gurobi_solver.py     # Mô hình ILP (Gurobi Optimizer)
├── results/
│   ├── benchmark_results.csv    # Dữ liệu thực nghiệm thô
│   └── plots/                   # Biểu đồ xuất tự động (.png & .pdf)
│       ├── 1_instance_barplot_log.png
│       ├── 2_cactus_plot.png
│       └── 3_runtime_boxplot.png
├── run_benchmark.py         # Tập lệnh chạy đánh giá tự động
├── plot_results.py          # Tập lệnh dựng biểu đồ từ dữ liệu CSV
├── requirements.txt         # Thư viện phụ thuộc
└── README.md                # Tài liệu hướng dẫn dự án

```

---

### Cách vận hành

1. **Cài đặt thư viện:**

```bash
pip install -r requirements.txt
```

2. **Chạy đánh giá thực nghiệm (Benchmark):**

```bash
python run_benchmark.py

```

Chương trình sẽ tự động giải các instance $g-p-w$ trên 3 bộ giải và lưu kết quả vào results/benchmark_results.csv.

3. **Xuất biểu đồ đồ họa (Plotting):**

```bash
python plot_results.py

```

_(Tập lệnh đọc dữ liệu CSV và xuất các biểu đồ dạng .png và .pdf vào thư mục results/plots/.)_
