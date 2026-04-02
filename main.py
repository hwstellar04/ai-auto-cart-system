import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from collections import defaultdict


class AutoCartSystem:
    def __init__(self):
        self.records = []

    def add_record(self, user_id, item, date):
        self.records.append({
            "user": user_id,
            "item": item,
            "date": datetime.strptime(date, "%Y-%m-%d")
        })

    def get_user_history(self, user_id):
        grouped = defaultdict(list)
        for r in self.records:
            if r["user"] == user_id:
                grouped[r["item"]].append(r["date"])

        for item in grouped:
            grouped[item].sort()

        return grouped

    def calc_cycle(self, dates):
        if len(dates) < 2:
            return 60  # 기본값

        gaps = []
        for i in range(1, len(dates)):
            gaps.append((dates[i] - dates[i-1]).days)

        return sum(gaps) / len(gaps)

    def recommend(self, user_id):
        today = datetime.today()
        history = self.get_user_history(user_id)

        result = []

        for item, dates in history.items():
            cycle = self.calc_cycle(dates)
            last = dates[-1]
            next_date = last + timedelta(days=cycle)
            diff = (next_date - today).days

            if diff <= 7:
                result.append({
                    "item": item,
                    "cycle": round(cycle, 1),
                    "next": next_date.strftime("%Y-%m-%d"),
                    "diff": diff
                })

        result.sort(key=lambda x: x["diff"])
        return result


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Auto Cart System")
        self.root.geometry("700x500")

        self.system = AutoCartSystem()
        self.load_sample_data()

        self.build_ui()

    def load_sample_data(self):
        self.system.add_record("user1", "치약", "2025-10-01")
        self.system.add_record("user1", "치약", "2025-12-01")
        self.system.add_record("user1", "치약", "2026-01-30")

        self.system.add_record("user1", "로션", "2025-09-15")
        self.system.add_record("user1", "로션", "2025-11-14")
        self.system.add_record("user1", "로션", "2026-01-13")

        self.system.add_record("user1", "샴푸", "2026-02-01")

    def build_ui(self):
        title = tk.Label(self.root, text="AI Auto Cart Recommendation", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        tk.Button(self.root, text="추천 생성", command=self.run_recommend).pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("item", "cycle", "next", "diff"), show="headings")
        self.tree.heading("item", text="Item")
        self.tree.heading("cycle", text="Cycle (days)")
        self.tree.heading("next", text="Next Purchase Date")
        self.tree.heading("diff", text="Days Left")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

    def run_recommend(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        results = self.system.recommend("user1")

        for r in results:
            self.tree.insert("", "end", values=(
                r["item"],
                r["cycle"],
                r["next"],
                r["diff"]
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
