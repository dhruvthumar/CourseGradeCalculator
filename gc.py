import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class CourseGradeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Grade Calculator")
        self.root.geometry("1000x600")
        self.root.config(padx=20, pady=20)  # overall padding

        self.courses = []
        self.current_course = None
        self.data_file = "courses_data.json"

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Top title label
        self.title_label = tk.Label(self.root, text="Course Grade Calculator", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Course Selection Frame
        course_frame = tk.Frame(self.root)
        course_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20))
        course_frame.grid_columnconfigure(0, weight=1)

        self.course_label = tk.Label(course_frame, text="Select Course:", font=("Arial", 14))
        self.course_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.course_listbox = tk.Listbox(course_frame, selectmode=tk.SINGLE, font=("Arial", 12), height=8)
        self.course_listbox.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.course_listbox.bind("<<ListboxSelect>>", self.load_course)

        course_button_frame = tk.Frame(course_frame)
        course_button_frame.grid(row=2, column=0, pady=(0, 10))
        self.add_course_button = tk.Button(course_button_frame, text="Add Course", command=self.add_course, font=("Arial", 12), width=12)
        self.add_course_button.pack(side=tk.LEFT, padx=5)
        self.delete_course_button = tk.Button(course_button_frame, text="Delete Course", command=self.delete_course, font=("Arial", 12), width=12)
        self.delete_course_button.pack(side=tk.LEFT, padx=5)

        # Grade Entries Frame
        grade_frame = tk.Frame(self.root)
        grade_frame.grid(row=1, column=1, sticky="nsew")
        grade_frame.grid_columnconfigure(0, weight=1)

        self.entries_label = tk.Label(grade_frame, text="Grade Entries:", font=("Arial", 14))
        self.entries_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.grade_listbox = tk.Listbox(grade_frame, font=("Arial", 12), height=8, width=40)
        self.grade_listbox.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        # Buttons for grade entry actions
        grade_button_frame = tk.Frame(grade_frame)
        grade_button_frame.grid(row=2, column=0, pady=(0, 10))
        self.add_entry_button = tk.Button(grade_button_frame, text="Add Grade Entry", command=self.add_grade_entry, font=("Arial", 12), width=15)
        self.add_entry_button.grid(row=0, column=0, padx=5, pady=5)
        self.edit_entry_button = tk.Button(grade_button_frame, text="Edit Grade Entry", command=self.edit_grade_entry, font=("Arial", 12), width=15)
        self.edit_entry_button.grid(row=0, column=1, padx=5, pady=5)
        self.delete_entry_button = tk.Button(grade_button_frame, text="Delete Grade Entry", command=self.delete_grade_entry, font=("Arial", 12), width=15)
        self.delete_entry_button.grid(row=0, column=2, padx=5, pady=5)
        self.calculate_button = tk.Button(grade_button_frame, text="Calculate Final Grade", command=self.calculate_grade, font=("Arial", 12), width=18)
        self.calculate_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Result Label at the bottom
        self.result_label = tk.Label(self.root, text="Final Grade: ", font=("Arial", 16))
        self.result_label.grid(row=2, column=0, columnspan=2, pady=(20, 0))

        # Responsive grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def add_course(self):
        course_name = simpledialog.askstring("Add Course", "Enter Course Name:", parent=self.root)
        if course_name:
            new_course = {"name": course_name, "grades": []}
            self.courses.append(new_course)
            self.course_listbox.insert(tk.END, course_name)
            self.save_data()

    def delete_course(self):
        selected_course_index = self.course_listbox.curselection()
        if selected_course_index:
            selected_course = self.course_listbox.get(selected_course_index)
            for course in self.courses:
                if course["name"] == selected_course:
                    self.courses.remove(course)
                    self.course_listbox.delete(selected_course_index)
                    self.grade_listbox.delete(0, tk.END)
                    self.result_label.config(text="Final Grade: ")
                    self.save_data()
                    break

    def load_course(self, event):
        selected_course_index = self.course_listbox.curselection()
        if selected_course_index:
            selected_course_name = self.course_listbox.get(selected_course_index)
            self.current_course = next(course for course in self.courses if course["name"] == selected_course_name)
            self.grade_listbox.delete(0, tk.END)
            for entry in self.current_course["grades"]:
                self.grade_listbox.insert(tk.END, f"{entry['category']} - {entry['score']} / {entry['total']} - {entry['weight']}%")

    def add_grade_entry(self):
        if not self.current_course:
            messagebox.showwarning("No Course Selected", "Please select a course before adding grade entries.", parent=self.root)
            return
        category = simpledialog.askstring("Add Grade Entry", "Enter Category:", parent=self.root)
        if category:
            score = simpledialog.askfloat("Add Grade Entry", "Enter Score:", parent=self.root)
            total = simpledialog.askfloat("Add Grade Entry", "Enter Total:", parent=self.root)
            weight = simpledialog.askfloat("Add Grade Entry", "Enter Weight (%):", parent=self.root)
            if score is not None and total is not None and weight is not None:
                new_entry = {"category": category, "score": score, "total": total, "weight": weight}
                self.current_course["grades"].append(new_entry)
                self.grade_listbox.insert(tk.END, f"{category} - {score} / {total} - {weight}%")
                self.save_data()

    def delete_grade_entry(self):
        selection = self.grade_listbox.curselection()
        if not self.current_course or not selection:
            messagebox.showwarning("No Grade Selected", "Please select a grade entry to delete.", parent=self.root)
            return
        index = selection[0]
        del self.current_course["grades"][index]
        self.grade_listbox.delete(index)
        self.save_data()

    def edit_grade_entry(self):
        selection = self.grade_listbox.curselection()
        if not self.current_course or not selection:
            messagebox.showwarning("No Grade Selected", "Please select a grade entry to edit.", parent=self.root)
            return
        index = selection[0]
        grade = self.current_course["grades"][index]

        # Ask user for new values; pre-fill current values
        new_category = simpledialog.askstring("Edit Grade Entry", "Enter Category:", initialvalue=grade["category"], parent=self.root)
        if new_category is None:
            return
        new_score = simpledialog.askfloat("Edit Grade Entry", "Enter Score:", initialvalue=grade["score"], parent=self.root)
        if new_score is None:
            return
        new_total = simpledialog.askfloat("Edit Grade Entry", "Enter Total:", initialvalue=grade["total"], parent=self.root)
        if new_total is None:
            return
        new_weight = simpledialog.askfloat("Edit Grade Entry", "Enter Weight (%):", initialvalue=grade["weight"], parent=self.root)
        if new_weight is None:
            return

        # Update the grade entry
        grade["category"] = new_category
        grade["score"] = new_score
        grade["total"] = new_total
        grade["weight"] = new_weight

        # Update the listbox display
        self.grade_listbox.delete(index)
        self.grade_listbox.insert(index, f"{new_category} - {new_score} / {new_total} - {new_weight}%")
        self.save_data()

    def calculate_grade(self):
        if not self.current_course or not self.current_course["grades"]:
            self.result_label.config(text="Final Grade: No grades entered.")
            return

        weighted_sum = 0
        total_weight = 0
        for entry in self.current_course["grades"]:
            if entry["total"] > 0:
                percentage = (entry["score"] / entry["total"]) * 100
                weighted_sum += (percentage * entry["weight"])
                total_weight += entry["weight"]
        final_grade = weighted_sum / total_weight if total_weight > 0 else 0
        self.result_label.config(text=f"Final Grade: {final_grade:.2f}%")

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                try:
                    self.courses = json.load(file)
                    for course in self.courses:
                        self.course_listbox.insert(tk.END, course["name"])
                except json.JSONDecodeError:
                    print("Error loading data.")
        else:
            print("No saved data found.")

    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.courses, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseGradeCalculator(root)
    root.mainloop()
