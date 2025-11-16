import customtkinter as ctk
import tkinter.messagebox
import tkinter.simpledialog
import os
import tempfile
import psutil
import threading
import queue

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TempRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Temp File Remover")
        self.geometry("800x600")  # Larger size for modern look
        self.resizable(True, True)

        # Left sidebar for tabs
        self.left_frame = ctk.CTkFrame(self, width=180, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Tab buttons
        self.program_btn = ctk.CTkButton(self.left_frame, text="Program", height=50, command=lambda: self.show_tab("program"))
        self.program_btn.pack(pady=10, padx=10, fill="x")

        self.settings_btn = ctk.CTkButton(self.left_frame, text="Settings", height=50, command=lambda: self.show_tab("settings"))
        self.settings_btn.pack(pady=10, padx=10, fill="x")

        self.changelog_btn = ctk.CTkButton(self.left_frame, text="Changelog", height=50, command=lambda: self.show_tab("changelog"))
        self.changelog_btn.pack(pady=10, padx=10, fill="x")

        # Right content frame
        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Content frames
        self.program_frame = ctk.CTkFrame(self.right_frame)
        self.settings_frame = ctk.CTkFrame(self.right_frame)
        self.changelog_frame = ctk.CTkFrame(self.right_frame)

        # Setup each frame
        self.setup_program_frame()
        self.setup_settings_frame()
        self.setup_changelog_frame()

        # Show default tab
        self.show_tab("program")

        self.files_to_delete = []
        self.total_size = 0
        self.queue = queue.Queue()

    def show_tab(self, tab_name):
        # Hide all
        self.program_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.changelog_frame.pack_forget()

        # Reset button states
        self.program_btn.configure(fg_color="transparent")
        self.settings_btn.configure(fg_color="transparent")
        self.changelog_btn.configure(fg_color="transparent")

        # Show selected
        if tab_name == "program":
            self.program_frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.program_btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        elif tab_name == "settings":
            self.settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.settings_btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        elif tab_name == "changelog":
            self.changelog_frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.changelog_btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

    def setup_program_frame(self):
        # Scan button
        self.scan_button = ctk.CTkButton(self.program_frame, text="Scan Temp Folder", height=50, font=ctk.CTkFont(size=14))
        self.scan_button.pack(pady=20)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.program_frame, width=400, height=20)
        self.progress_bar.set(0)
        # Initially hidden

        # Size label
        self.size_label = ctk.CTkLabel(self.program_frame, text="Size to delete: 0 MB (0.00 GB)", font=ctk.CTkFont(size=14))
        self.size_label.pack(pady=20)

        # Delete button
        self.delete_button = ctk.CTkButton(self.program_frame, text="Delete Temp Files", height=50, font=ctk.CTkFont(size=14), state="disabled")
        self.delete_button.pack(pady=20)

    def setup_settings_frame(self):
        # Theme label
        theme_label = ctk.CTkLabel(self.settings_frame, text="Appearance Mode:", font=ctk.CTkFont(size=16))
        theme_label.pack(pady=20)

        # Theme selector
        self.theme_var = ctk.StringVar(value="System")
        theme_menu = ctk.CTkOptionMenu(self.settings_frame, values=["Light", "Dark", "System"], variable=self.theme_var, command=self.change_theme, height=40, font=ctk.CTkFont(size=14))
        theme_menu.pack(pady=20)

    def setup_changelog_frame(self):
        # Changelog text box
        self.changelog_text = ctk.CTkTextbox(self.changelog_frame, wrap="word", state="disabled", font=ctk.CTkFont(size=12))
        self.changelog_text.pack(pady=20, padx=20, fill="both", expand=True)

        # Load initial changelog
        self.load_changelog()

        # Edit button
        self.edit_button = ctk.CTkButton(self.changelog_frame, text="Edit Changelog", height=40, font=ctk.CTkFont(size=14), command=self.edit_changelog)
        self.edit_button.pack(pady=10)

        # Save button (hidden initially)
        self.save_button = ctk.CTkButton(self.changelog_frame, text="Save Changelog", height=40, font=ctk.CTkFont(size=14), command=self.save_changelog)
        # Not packed initially

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def load_changelog(self):
        changelog_file = os.path.join(os.path.dirname(__file__), "changelog.txt")
        if os.path.exists(changelog_file):
            with open(changelog_file, "r") as f:
                content = f.read()
        else:
            content = "Changelog:\n\nVersion 1.0 - Initial release\n- Added temp file scanning and deletion\n- Modern UI with progress bar\n- Size estimation\n"
        self.changelog_text.delete("1.0", "end")
        self.changelog_text.insert("1.0", content)

    def edit_changelog(self):
        password = tkinter.simpledialog.askstring("Password", "Enter password to edit changelog:", show="*")
        if password == "admin123":  # Hardcoded password, change as needed
            self.changelog_text.configure(state="normal")
            self.save_button.pack(pady=10)
            self.edit_button.configure(state="disabled")
        else:
            tkinter.messagebox.showerror("Error", "Incorrect password")

    def save_changelog(self):
        content = self.changelog_text.get("1.0", "end").strip()
        changelog_file = os.path.join(os.path.dirname(__file__), "changelog.txt")
        try:
            with open(changelog_file, "w") as f:
                f.write(content)
            tkinter.messagebox.showinfo("Success", "Changelog saved")
            self.changelog_text.configure(state="disabled")
            self.save_button.pack_forget()
            self.edit_button.configure(state="normal")
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to save: {e}")

    def scan_temp(self):
        self.scan_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        self.size_label.configure(text="Scanning...")
        thread = threading.Thread(target=self._scan_worker)
        thread.start()
        self.check_queue()

    def check_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg[0] == 'progress':
                    self.progress_bar.set(msg[1])
                elif msg[0] == 'done':
                    self._scan_done(msg[1], msg[2])
                    return
        except queue.Empty:
            pass
        self.after(100, self.check_queue)

    def _scan_worker(self):
        try:
            temp_dir = tempfile.gettempdir()
            self.files_to_delete = []
            self.total_size = 0

            # Collect all open file paths first for faster checking
            open_files = set()
            try:
                for proc in psutil.process_iter(['pid']):
                    try:
                        for file in proc.open_files():
                            open_files.add(file.path)
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        continue
            except Exception:
                # If can't collect, proceed without checking
                open_files = set()

            # First, count total files
            total_files = 0
            for root, dirs, files in os.walk(temp_dir):
                total_files += len(files)

            if total_files == 0:
                self.queue.put(('done', True, None))
                return

            processed = 0
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    path = os.path.join(root, file)
                    if path not in open_files:
                        try:
                            size = os.path.getsize(path)
                            self.total_size += size
                            self.files_to_delete.append(path)
                        except OSError:
                            pass
                    processed += 1
                    progress = processed / total_files
                    self.queue.put(('progress', progress))

            self.queue.put(('done', True, None))
        except Exception as e:
            self.queue.put(('done', False, str(e)))

    def _scan_done(self, success, error):
        self.scan_button.configure(state="normal")
        self.progress_bar.pack_forget()
        if success:
            size_mb = self.total_size / (1024 * 1024)
            size_gb = size_mb / 1024
            self.size_label.configure(text=f"Size to delete: {size_mb:.2f} MB ({size_gb:.2f} GB)")
            self.delete_button.configure(state="normal")
            tkinter.messagebox.showinfo("Scan Complete", "Temp folder scanned successfully.")
        else:
            self.size_label.configure(text="Scan failed.")
            tkinter.messagebox.showerror("Scan Error", f"An error occurred during scan: {error}")

    def confirm_delete(self):
        if tkinter.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {len(self.files_to_delete)} temp files?\nSize: {self.total_size / (1024 * 1024):.2f} MB"):
            self.delete_files()

    def delete_files(self):
        deleted_count = 0
        failed_count = 0
        for path in self.files_to_delete:
            try:
                os.remove(path)
                deleted_count += 1
            except OSError:
                failed_count += 1

        if failed_count > 0:
            tkinter.messagebox.showwarning("Deletion Warning", f"Deleted {deleted_count} files. {failed_count} files could not be deleted.")
        else:
            tkinter.messagebox.showinfo("Deletion Complete", f"Successfully deleted {deleted_count} temp files.")
        self.size_label.configure(text="Size to delete: 0 MB (0.00 GB)")
        self.delete_button.configure(state="disabled")
        self.files_to_delete = []
        self.total_size = 0

if __name__ == "__main__":
    app = TempRemoverApp()
    app.mainloop()