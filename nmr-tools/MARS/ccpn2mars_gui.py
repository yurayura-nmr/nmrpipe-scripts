# Author: DeepSeek

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class MARSInputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MARS Input Builder")
        self.root.geometry("1100x500")

        # Data storage: list of dicts
        self.data = []

        # Define columns: Name (required), Residue (optional for fixation), then the 7 shift columns
        self.columns = [
            "Name", "Residue", "N", "HN", "CA", "CB", "CO-1", "CA-1", "CB-1"
        ]

        # Create Treeview
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings", selectmode="browse")
        for col in self.columns:
            self.tree.heading(col, text=col)
            # Set column widths
            width = 80 if col in ["Name", "Residue"] else 70
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Entry frame for new row
        entry_frame = ttk.Frame(root)
        entry_frame.pack(fill=tk.X, padx=5, pady=5)

        self.entries = {}
        for i, col in enumerate(self.columns):
            lbl = ttk.Label(entry_frame, text=col)
            lbl.grid(row=0, column=i, padx=2, pady=2)
            ent = ttk.Entry(entry_frame, width=10)
            ent.grid(row=1, column=i, padx=2, pady=2)
            self.entries[col] = ent

        # Buttons
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(btn_frame, text="Add Row", command=self.add_row).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Save", command=self.save_files).pack(side=tk.LEFT, padx=2)

    def add_row(self):
        # Collect values from entries
        row = {}
        for col in self.columns:
            val = self.entries[col].get().strip()
            row[col] = val if val != "" else None   # None will be replaced by "-" later

        # Validate that Name is provided
        if not row["Name"]:
            messagebox.showerror("Error", "Pseudoresidue Name is required.")
            return

        # Append to data
        self.data.append(row)

        # Insert into tree
        values = [row[col] if row[col] is not None else "" for col in self.columns]
        self.tree.insert("", tk.END, values=values)

        # Clear entries
        for ent in self.entries.values():
            ent.delete(0, tk.END)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        # Get index of selected item
        item = selected[0]
        index = self.tree.index(item)
        # Remove from data list
        del self.data[index]
        # Remove from tree
        self.tree.delete(item)

    def clear_all(self):
        self.data.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

    def save_files(self):
        if not self.data:
            messagebox.showwarning("No data", "No rows to save.")
            return

        # Ask for directory and base name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".tab",
            filetypes=[("Tab files", "*.tab"), ("All files", "*.*")],
            title="Save files (base name)"
        )
        if not file_path:
            return

        base, ext = os.path.splitext(file_path)
        cs_file = base + "_cs.tab"
        fix_file = base + "_fix.tab"

        # Write chemical shift table
        with open(cs_file, "w") as f:
            # Header: the order must match MARS expectation: Name N HN CA CB CO-1 CA-1 CB-1
            header = "Name\tN\tHN\tCA\tCB\tCO-1\tCA-1\tCB-1\n"
            f.write(header)

            for row in self.data:
                name = row["Name"]
                # Shifts in the order of header
                shifts = [
                    row["N"] if row["N"] is not None else "-",
                    row["HN"] if row["HN"] is not None else "-",
                    row["CA"] if row["CA"] is not None else "-",
                    row["CB"] if row["CB"] is not None else "-",
                    row["CO-1"] if row["CO-1"] is not None else "-",
                    row["CA-1"] if row["CA-1"] is not None else "-",
                    row["CB-1"] if row["CB-1"] is not None else "-"
                ]
                line = name + "\t" + "\t".join(shifts) + "\n"
                f.write(line)

        # Write fixation table if any residues assigned
        with open(fix_file, "w") as f:
            fix_written = False
            for row in self.data:
                if row["Residue"] and row["Residue"].strip():
                    # Write as "name   residue"
                    f.write(f"{row['Name']}\t{row['Residue'].strip()}\n")
                    fix_written = True
            if not fix_written:
                # Write a comment to indicate no fixes
                f.write("# No fixed assignments\n")

        messagebox.showinfo("Success", f"Files saved:\n{cs_file}\n{fix_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MARSInputGUI(root)
    root.mainloop()
