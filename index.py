import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import get_drive
import list_deleted_files
import main_recovery

# FAT32 Data Recovery Application
class FAT32RecoveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FAT32 Data Recovery")
        self.root.geometry("900x600")
        self.root.configure(bg="#f4f4f9")

        self.disk_var = tk.StringVar()  # Variable for the dropdown menu
        self.selected_disk = None

        # Custom Fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.label_font = Font(family="Arial", size=12)
        self.button_font = Font(family="Arial", size=11, weight="bold")

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        # Frame for dropdown menu and Load button
        self.menu_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.menu_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title Label
        title_label = tk.Label(
            self.menu_frame,
            text="FAT32 Data Recovery",
            font=self.title_font,
            bg="#f4f4f9",
            fg="#34495e"
        )
        title_label.pack(pady=20)

        # Dropdown Menu Label
        dropdown_label = tk.Label(
            self.menu_frame,
            text="Select a Disk:",
            font=self.label_font,
            bg="#f4f4f9",
            fg="#34495e"
        )
        dropdown_label.pack(pady=10)

        # Dropdown Menu
        self.disk_dropdown = ttk.Combobox(
            self.menu_frame, textvariable=self.disk_var, state="readonly", width=40
        )
        self.disk_dropdown.pack(pady=10)

        # Populate Dropdown with connected disks
        disks = get_drive.list_connected_disks()
        self.disk_dropdown["values"] = disks

        # Button to Load Disk Data
        load_button = tk.Button(
            self.menu_frame,
            text="Load Disk Data",
            command=self.load_disk_data,
            font=self.button_font,
            bg="#2980b9",
            fg="white",
            activebackground="#3498db",
            activeforeground="white",
            relief=tk.RAISED
        )
        load_button.pack(pady=20)

        # Frame for displaying files (initially hidden)
        self.file_frame = tk.Frame(self.root, bg="#f4f4f9")

    def load_disk_data(self):
        # Get the selected disk
        self.selected_disk = self.disk_var.get()
        if not self.selected_disk:
            messagebox.showwarning("Warning", "Please select a disk!")
            return

        # Retrieve deleted files data for the selected disk
        disk_data = list_deleted_files.list_deleted_files(self.selected_disk)
        if not disk_data:
            messagebox.showinfo("No Data", f"No files found for {self.selected_disk}.")
            return

        # Clear the dropdown selection and hide the menu frame
        self.disk_var.set("")
        self.menu_frame.pack_forget()

        # Display the file data
        self.display_files(disk_data)

    def display_files(self, data):
        # Clear previous content in the file frame
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        # Show the file frame
        self.file_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Treeview for displaying files
        tree = ttk.Treeview(self.file_frame, columns=("Name", "Size", "Starting Cluster", "Result"), show="headings", height=15)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Define Treeview columns
        tree.heading("Name", text="File Name")
        tree.heading("Size", text="Size")
        tree.heading("Starting Cluster", text="Starting Cluster")
        tree.heading("Result", text="Recovery Result")
        tree.column("Name", anchor=tk.W, width=250)
        tree.column("Size", anchor=tk.CENTER, width=100)
        tree.column("Starting Cluster", anchor=tk.CENTER, width=150)
        tree.column("Result", anchor=tk.CENTER, width=150)

        # Insert data into the Treeview
        for row in data:
            tree.insert("", tk.END, values=(*row, ""))

        # Select File Button
        select_button = tk.Button(
            self.file_frame,
            text="Select File",
            command=lambda: self.select_file(tree),
            font=self.button_font,
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            activeforeground="white",
            relief=tk.RAISED
        )
        select_button.pack(pady=10)

        # Back Button
        back_button = tk.Button(
            self.file_frame,
            text="Back",
            command=self.go_back_to_menu,
            font=self.button_font,
            bg="#c0392b",
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            relief=tk.RAISED
        )
        back_button.pack(pady=10)

    def select_file(self, tree):
        # Get the selected file
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a file!")
            return

        file_data = tree.item(selected_item, "values")
        if file_data:
            # Display a loading label
            loading_label = tk.Label(self.file_frame, text="Loading, please wait...", font=("Arial", 12), fg="#2980b9", bg="#f4f4f9")
            loading_label.pack(pady=10)

            # Force the UI to update
            self.file_frame.update_idletasks()

            # Simulate a recovery process
            self.root.after(2000, self.finish_file_selection, tree, selected_item, file_data, loading_label)

    def finish_file_selection(self, tree, selected_item, file_data, loading_label):
        # Remove the loading label
        loading_label.destroy()

        # Extract file name and starting cluster
        file_name = file_data[0]
        starting_cluster = file_data[2]
        size = file_data[1]

        # Call the recovery function
        recovery_success = main_recovery.recovery_func(file_name, starting_cluster, size, self.selected_disk)

        # Determine the result based on the recovery function
        result = "Success" if recovery_success else "Failure"

        # Update the Treeview with the result
        tree.item(selected_item, values=(*file_data[:3], result))

        # Show a message box with the result
        if recovery_success:
            messagebox.showinfo("Result", f"File '{file_name}' recovered successfully!")
        else:
            messagebox.showerror("Result", f"Failed to recover file '{file_name}'.")

    def go_back_to_menu(self):
        # Clear the file frame
        for widget in self.file_frame.winfo_children():
            widget.destroy()
        self.file_frame.pack_forget()

        # Show the menu frame
        self.menu_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = FAT32RecoveryApp(root)
    root.mainloop()
