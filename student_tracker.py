from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

DATABASE_PATH = Path(__file__).with_name("students.db")

@dataclass(frozen=True)
class Student:

    name: str
    age: int
    math_score: float
    literature_score: float
    english_score: float
    id: int | None = None

    @property
    def average(self) -> float:

        return (self.math_score + self.literature_score + self.english_score) / 3

    @property
    def classification(self) -> str:

        if self.average >= 8:
            return "Giỏi"
        if self.average >= 6.5:
            return "Khá"
        if self.average >= 5:
            return "Trung bình"
        return "Yếu"

class StudentRepository:

    def __init__(self, database_path: str | Path = DATABASE_PATH) -> None:

        self.database_path = database_path
        self._create_table()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _create_table(self) -> None:

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL CHECK (trim(name) <> ''),
                    age INTEGER NOT NULL CHECK (age BETWEEN 1 AND 120),
                    math_score REAL NOT NULL CHECK (math_score BETWEEN 0 AND 10),
                    literature_score REAL NOT NULL CHECK (literature_score BETWEEN 0 AND 10),
                    english_score REAL NOT NULL CHECK (english_score BETWEEN 0 AND 10)
                )
                """
            )

    @staticmethod
    def _from_row(row: sqlite3.Row) -> Student:

        return Student(
            id=row["id"],
            name=row["name"],
            age=row["age"],
            math_score=row["math_score"],
            literature_score=row["literature_score"],
            english_score=row["english_score"],
        )

    def add(self, student: Student) -> int:

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO students
                    (name, age, math_score, literature_score, english_score)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    student.name,
                    student.age,
                    student.math_score,
                    student.literature_score,
                    student.english_score,
                ),
            )
            return int(cursor.lastrowid)

    def get_all(self) -> list[Student]:

        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM students ORDER BY id"
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def get_by_id(self, student_id: int) -> Student | None:

        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM students WHERE id = ?", (student_id,)
            ).fetchone()
        return self._from_row(row) if row else None

    def search_by_name(self, query: str) -> list[Student]:

        normalized_query = query.casefold()
        return [
            student
            for student in self.get_all()
            if normalized_query in student.name.casefold()
        ]

    def update(self, student: Student) -> bool:

        if student.id is None:
            return False
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE students
                SET name = ?, age = ?, math_score = ?,
                    literature_score = ?, english_score = ?
                WHERE id = ?
                """,
                (
                    student.name,
                    student.age,
                    student.math_score,
                    student.literature_score,
                    student.english_score,
                    student.id,
                ),
            )
            return cursor.rowcount > 0

    def delete(self, student_id: int) -> bool:

        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM students WHERE id = ?", (student_id,)
            )
            return cursor.rowcount > 0

def prompt_text(label: str, default: str | None = None) -> str:

    while True:
        suffix = f" [{default}]" if default is not None else ""
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("Giá trị không được để trống.")

def prompt_number(
    label: str,
    minimum: float,
    maximum: float,
    default: float | None = None,
) -> float:

    while True:
        suffix = f" [{default:g}]" if default is not None else ""
        raw_value = input(f"{label}{suffix}: ").strip()
        if not raw_value and default is not None:
            return default
        try:
            value = float(raw_value)
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Giá trị phải nằm trong khoảng {minimum:g}-{maximum:g}.")

def prompt_integer(
    label: str,
    minimum: int,
    maximum: int | None = None,
    default: int | None = None,
) -> int:

    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw_value = input(f"{label}{suffix}: ").strip()
        if not raw_value and default is not None:
            return default
        try:
            value = int(raw_value)
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")
            continue
        if value >= minimum and (maximum is None or value <= maximum):
            return value
        if maximum is None:
            print(f"Giá trị phải từ {minimum} trở lên.")
        else:
            print(f"Giá trị phải nằm trong khoảng {minimum}-{maximum}.")

def prompt_student(current: Student | None = None) -> Student:

    return Student(
        id=current.id if current else None,
        name=prompt_text("Tên học sinh", current.name if current else None),
        age=prompt_integer("Tuổi", 1, 120, current.age if current else None),
        math_score=prompt_number(
            "Điểm Toán", 0, 10, current.math_score if current else None
        ),
        literature_score=prompt_number(
            "Điểm Văn", 0, 10, current.literature_score if current else None
        ),
        english_score=prompt_number(
            "Điểm Anh", 0, 10, current.english_score if current else None
        ),
    )

def display_students(students: list[Student]) -> None:

    if not students:
        print("Không có học sinh nào.")
        return

    print(
        f"{'ID':>4}  {'Tên':<24} {'Tuổi':>4}  "
        f"{'Toán':>5} {'Văn':>5} {'Anh':>5} {'ĐTB':>5}  Xếp loại"
    )
    print("-" * 79)
    for student in students:
        print(
            f"{student.id:>4}  {student.name[:24]:<24} {student.age:>4}  "
            f"{student.math_score:>5.1f} {student.literature_score:>5.1f} "
            f"{student.english_score:>5.1f} {student.average:>5.2f}  "
            f"{student.classification}"
        )

def add_students(repository: StudentRepository) -> None:

    count = prompt_integer("Số học sinh cần thêm", 1)
    for index in range(1, count + 1):
        print(f"\nHọc sinh {index}/{count}")
        student_id = repository.add(prompt_student())
        print(f"Đã thêm học sinh với ID {student_id}.")

def search_students(repository: StudentRepository) -> None:

    query = prompt_text("Nhập tên cần tìm")
    students = repository.search_by_name(query)
    if students:
        display_students(students)
    else:
        print("Không tìm thấy.")

def update_student(repository: StudentRepository) -> None:

    student_id = prompt_integer("ID học sinh cần sửa", 1)
    student = repository.get_by_id(student_id)
    if student is None:
        print("Không tìm thấy học sinh.")
        return
    print("Nhấn Enter để giữ nguyên giá trị hiện tại.")
    repository.update(prompt_student(student))
    print("Đã cập nhật học sinh.")

def delete_student(repository: StudentRepository) -> None:

    student_id = prompt_integer("ID học sinh cần xóa", 1)
    student = repository.get_by_id(student_id)
    if student is None:
        print("Không tìm thấy học sinh.")
        return
    confirmation = input(f"Xóa {student.name}? (y/N): ").strip().casefold()
    if confirmation == "y":
        repository.delete(student_id)
        print("Đã xóa học sinh.")
    else:
        print("Đã hủy.")

def print_menu() -> None:

    print(
        """
=== STUDENT TRACKER ===
1. Thêm học sinh
2. Hiển thị danh sách
3. Tìm theo tên
4. Sửa thông tin
5. Xóa học sinh
6. Thoát
"""
    )

def run(repository: StudentRepository | None = None) -> None:

    repository = repository or StudentRepository()
    while True:
        print_menu()
        choice = input("Chọn chức năng: ").strip()
        if choice == "1":
            add_students(repository)
        elif choice == "2":
            display_students(repository.get_all())
        elif choice == "3":
            search_students(repository)
        elif choice == "4":
            update_student(repository)
        elif choice == "5":
            delete_student(repository)
        elif choice == "6":
            print("Hẹn gặp lại!")
            return
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 6.")

if __name__ == "__main__":
    try:
        run()
    except (EOFError, KeyboardInterrupt):
        print("\nĐã thoát chương trình.")
