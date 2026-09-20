
from __future__ import annotations

import math

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except ImportError as error:
    raise SystemExit(
        "Tkinter chưa được cài. Trên Ubuntu/Debian, chạy: sudo apt install python3-tk"
    ) from error

from student_tracker import Student, StudentRepository

class StudentTrackerGUI:

    PAPER = "#F5F0E6"
    PANEL = "#FFFCF5"
    INK = "#17352F"
    MUTED = "#66756F"
    TEAL = "#147D72"
    CORAL = "#DF654A"

    def __init__(self, root: tk.Tk) -> None:

        self.root = root
        self.repository = StudentRepository()
        self.selected_id: int | None = None

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.math_var = tk.StringVar()
        self.literature_var = tk.StringVar()
        self.english_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.average_var = tk.StringVar(value="--")
        self.classification_var = tk.StringVar(value="Chưa có điểm")
        self.status_var = tk.StringVar(value="Sẵn sàng")

        self._configure_window()
        self._configure_styles()
        self._build_layout()
        self._bind_events()
        self.refresh_table()

    def _configure_window(self) -> None:

        self.root.title("Student Tracker")
        self.root.geometry("1180x720")
        self.root.minsize(960, 620)
        self.root.configure(bg=self.PAPER)
        self.root.option_add("*Font", ("DejaVu Sans", 10))

    def _configure_styles(self) -> None:

        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("TFrame", background=self.PAPER)
        style.configure("Panel.TFrame", background=self.PANEL)
        style.configure("Header.TFrame", background=self.INK)

        style.configure(
            "TLabel", background=self.PAPER, foreground=self.INK, padding=(0, 2)
        )
        style.configure("Panel.TLabel", background=self.PANEL, foreground=self.INK)
        style.configure(
            "Title.TLabel",
            background=self.INK,
            foreground="#FFF9EC",
            font=("DejaVu Sans", 23, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.INK,
            foreground="#C9D8D3",
            font=("DejaVu Sans", 10),
        )
        style.configure(
            "Section.TLabel",
            background=self.PANEL,
            foreground=self.INK,
            font=("DejaVu Sans", 13, "bold"),
        )
        style.configure(
            "Metric.TLabel",
            background=self.INK,
            foreground="#FFF9EC",
            font=("DejaVu Sans", 17, "bold"),
        )
        style.configure(
            "MetricCaption.TLabel", background=self.INK, foreground="#C9D8D3"
        )

        style.configure(
            "Accent.TButton",
            background=self.TEAL,
            foreground="white",
            borderwidth=0,
            padding=(14, 9),
            font=("DejaVu Sans", 10, "bold"),
        )
        style.map("Accent.TButton", background=[("active", "#0E675E")])
        style.configure(
            "Danger.TButton",
            background=self.CORAL,
            foreground="white",
            borderwidth=0,
            padding=(12, 8),
        )
        style.map("Danger.TButton", background=[("active", "#C8523A")])
        style.configure("TButton", padding=(12, 8))

        style.configure(
            "Treeview",
            background=self.PANEL,
            fieldbackground=self.PANEL,
            foreground=self.INK,
            rowheight=31,
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background="#DCE7E1",
            foreground=self.INK,
            relief="flat",
            font=("DejaVu Sans", 9, "bold"),
        )
        style.map("Treeview", background=[("selected", self.TEAL)])

    def _build_layout(self) -> None:

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self.root, bg=self.INK, padx=30, pady=22)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        ttk.Label(header, text="STUDENT TRACKER", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            header,
            text="Quản lý học sinh, điểm số và xếp loại trong một nơi",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))

        metric = ttk.Frame(header, style="Header.TFrame")
        metric.grid(row=0, column=1, rowspan=2, sticky="e")
        ttk.Label(metric, textvariable=self.average_var, style="Metric.TLabel").grid(
            row=0, column=0, padx=(0, 26)
        )
        ttk.Label(metric, text="ĐIỂM TRUNG BÌNH", style="MetricCaption.TLabel").grid(
            row=1, column=0, padx=(0, 26)
        )
        ttk.Label(
            metric, textvariable=self.classification_var, style="Metric.TLabel"
        ).grid(row=0, column=1)
        ttk.Label(metric, text="XẾP LOẠI", style="MetricCaption.TLabel").grid(
            row=1, column=1
        )

        content = ttk.Frame(self.root, padding=22)
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        form = ttk.Frame(content, style="Panel.TFrame", padding=22)
        form.grid(row=0, column=0, sticky="ns", padx=(0, 18))
        ttk.Label(form, text="Thông tin học sinh", style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
        )
        self._add_field(form, 1, "Họ và tên", self.name_var)
        self._add_field(form, 2, "Tuổi", self.age_var)
        self._add_field(form, 3, "Điểm Toán", self.math_var)
        self._add_field(form, 4, "Điểm Văn", self.literature_var)
        self._add_field(form, 5, "Điểm Anh", self.english_var)

        ttk.Button(
            form, text="Thêm học sinh", style="Accent.TButton", command=self.add_student
        ).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(18, 8))
        ttk.Button(form, text="Cập nhật", command=self.update_student).grid(
            row=7, column=0, sticky="ew", padx=(0, 4)
        )
        ttk.Button(form, text="Làm mới", command=self.clear_form).grid(
            row=7, column=1, sticky="ew", padx=(4, 0)
        )

        list_panel = ttk.Frame(content, style="Panel.TFrame", padding=18)
        list_panel.grid(row=0, column=1, sticky="nsew")
        list_panel.grid_rowconfigure(2, weight=1)
        list_panel.grid_columnconfigure(0, weight=1)

        ttk.Label(list_panel, text="Danh sách học sinh", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        search = ttk.Frame(list_panel, style="Panel.TFrame")
        search.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        search.grid_columnconfigure(0, weight=1)
        search_entry = ttk.Entry(search, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8), ipady=5)
        search_entry.bind("<Return>", lambda _event: self.search_students())
        ttk.Button(search, text="Tìm kiếm", command=self.search_students).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(search, text="Tất cả", command=self.show_all).grid(row=0, column=2)

        table_frame = ttk.Frame(list_panel, style="Panel.TFrame")
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        columns = ("id", "name", "age", "math", "literature", "english", "average", "rank")
        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        headings = {
            "id": "ID",
            "name": "Tên",
            "age": "Tuổi",
            "math": "Toán",
            "literature": "Văn",
            "english": "Anh",
            "average": "ĐTB",
            "rank": "Xếp loại",
        }
        widths = {
            "id": 45,
            "name": 185,
            "age": 55,
            "math": 58,
            "literature": 58,
            "english": 58,
            "average": 62,
            "rank": 90,
        }
        for column in columns:
            self.table.heading(
                column,
                text=headings[column],
                anchor="w" if column == "name" else "center",
            )
            self.table.column(
                column,
                width=widths[column],
                minwidth=widths[column],
                anchor="w" if column == "name" else "center",
                stretch=column == "name",
            )
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        footer = ttk.Frame(list_panel, style="Panel.TFrame")
        footer.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        footer.grid_columnconfigure(0, weight=1)
        ttk.Label(footer, textvariable=self.status_var, style="Panel.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(
            footer,
            text="Xóa học sinh",
            style="Danger.TButton",
            command=self.delete_student,
        ).grid(row=0, column=1, sticky="e")

    @staticmethod
    def _add_field(
        parent: ttk.Frame, row: int, label: str, variable: tk.StringVar
    ) -> None:

        ttk.Label(parent, text=label, style="Panel.TLabel").grid(
            row=row, column=0, sticky="w", pady=7, padx=(0, 14)
        )
        ttk.Entry(parent, textvariable=variable, width=24).grid(
            row=row, column=1, sticky="ew", pady=7, ipady=5
        )

    def _bind_events(self) -> None:

        self.table.bind("<<TreeviewSelect>>", self._load_selection)
        for variable in (self.math_var, self.literature_var, self.english_var):
            variable.trace_add("write", self._update_preview)

    def _read_form(self) -> Student | None:

        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Dữ liệu không hợp lệ", "Tên không được để trống.")
            return None
        try:
            age = int(self.age_var.get())
            scores = [
                float(self.math_var.get()),
                float(self.literature_var.get()),
                float(self.english_var.get()),
            ]
        except ValueError:
            messagebox.showerror("Dữ liệu không hợp lệ", "Tuổi và điểm phải là số.")
            return None
        if not 1 <= age <= 120:
            messagebox.showerror("Dữ liệu không hợp lệ", "Tuổi phải từ 1 đến 120.")
            return None
        if any(not math.isfinite(score) or not 0 <= score <= 10 for score in scores):
            messagebox.showerror("Dữ liệu không hợp lệ", "Mỗi điểm phải từ 0 đến 10.")
            return None
        return Student(name, age, *scores, id=self.selected_id)

    def _update_preview(self, *_args: object) -> None:

        try:
            scores = [
                float(self.math_var.get()),
                float(self.literature_var.get()),
                float(self.english_var.get()),
            ]
            if any(not math.isfinite(score) or not 0 <= score <= 10 for score in scores):
                raise ValueError
        except ValueError:
            self.average_var.set("--")
            self.classification_var.set("Chưa có điểm")
            return
        student = Student("Preview", 1, *scores)
        self.average_var.set(f"{student.average:.2f}")
        self.classification_var.set(student.classification)

    def refresh_table(self, students: list[Student] | None = None) -> None:

        students = self.repository.get_all() if students is None else students
        self.table.delete(*self.table.get_children())
        for student in students:
            self.table.insert(
                "",
                "end",
                iid=str(student.id),
                values=(
                    student.id,
                    student.name,
                    student.age,
                    f"{student.math_score:.1f}",
                    f"{student.literature_score:.1f}",
                    f"{student.english_score:.1f}",
                    f"{student.average:.2f}",
                    student.classification,
                ),
            )
        self.status_var.set(f"{len(students)} học sinh")

    def add_student(self) -> None:

        student = self._read_form()
        if student is None:
            return
        student = Student(
            student.name,
            student.age,
            student.math_score,
            student.literature_score,
            student.english_score,
        )
        self.repository.add(student)
        self.clear_form()
        self.refresh_table()
        self.status_var.set(f"Đã thêm {student.name}")

    def update_student(self) -> None:

        if self.selected_id is None:
            messagebox.showinfo("Chưa chọn học sinh", "Chọn một học sinh trong bảng trước.")
            return
        student = self._read_form()
        if student is None:
            return
        self.repository.update(student)
        self.clear_form()
        self.refresh_table()
        self.status_var.set(f"Đã cập nhật {student.name}")

    def delete_student(self) -> None:

        if self.selected_id is None:
            messagebox.showinfo("Chưa chọn học sinh", "Chọn một học sinh trong bảng trước.")
            return
        student = self.repository.get_by_id(self.selected_id)
        if student is None:
            self.clear_form()
            self.refresh_table()
            return
        if not messagebox.askyesno("Xác nhận xóa", f"Xóa học sinh {student.name}?"):
            return
        self.repository.delete(self.selected_id)
        self.clear_form()
        self.refresh_table()
        self.status_var.set(f"Đã xóa {student.name}")

    def search_students(self) -> None:

        query = self.search_var.get().strip()
        if not query:
            self.show_all()
            return
        students = self.repository.search_by_name(query)
        self.refresh_table(students)
        if not students:
            self.status_var.set(f'Không tìm thấy "{query}"')

    def show_all(self) -> None:

        self.search_var.set("")
        self.refresh_table()

    def clear_form(self) -> None:

        self.selected_id = None
        for variable in (
            self.name_var,
            self.age_var,
            self.math_var,
            self.literature_var,
            self.english_var,
        ):
            variable.set("")
        for selected_item in self.table.selection():
            self.table.selection_remove(selected_item)

    def _load_selection(self, _event: tk.Event[tk.Misc]) -> None:

        selection = self.table.selection()
        if not selection:
            return
        student = self.repository.get_by_id(int(selection[0]))
        if student is None:
            return
        self.selected_id = student.id
        self.name_var.set(student.name)
        self.age_var.set(str(student.age))
        self.math_var.set(f"{student.math_score:g}")
        self.literature_var.set(f"{student.literature_score:g}")
        self.english_var.set(f"{student.english_score:g}")
        self.status_var.set(f"Đang chọn: {student.name}")

def main() -> None:

    try:
        root = tk.Tk()
    except tk.TclError as error:
        raise SystemExit(f"Không thể mở giao diện Tkinter: {error}") from error
    StudentTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
