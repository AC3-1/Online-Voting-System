from tkinter import *
from tkinter import messagebox
from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from voting_system import VotingSystem, file_wipe, save_candidates, BinarySearchTree, BST_Node
from admin import Admin

# Install these
# pip install matplotlib
# pip install argon2-cffi
 
class VotingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Online Voting System")
        self.voting_system = VotingSystem()
        self.admin = Admin(self.voting_system)
        self.current_username = None
        self.create_main_menu()
        self.open_login_window()

    # Main Menu
    def create_main_menu(self):
        menu_contain = Frame(self.master, borderwidth=1, bg="black", relief="sunken")
        menu_contain.pack(side="left", fill="y")

        Label(menu_contain, text="Online Voting System", 
              font=("Century Gothic", 20), fg="white", bg="black", padx=20).grid(row=0, column=0)
        
        btn_txt = ["Login", "Exit"]
        func = [self.open_login_window, self.master.quit]

        for i, txt in enumerate(btn_txt):
            Button(menu_contain, anchor="e", width=40, text=txt, font=("Century Gothic", 14), padx=10, pady=15, bg="white",
                   command=func[i]).grid(row=i + 1, column=0)

    # Register Menu
    def open_register_window(self):
        self.clear_widgets()

        register_window = Frame(self.master)
        register_window.pack(fill="both", expand=True)

        for i in range(11):
            register_window.grid_rowconfigure(i, weight=1)
            register_window.grid_columnconfigure(i, weight=1)

        Label(register_window, text="Registration Page", 
              font=("Century Gothic", 24, "bold")).grid(row=1, column=4, columnspan=2, sticky="NSEW")

        Label(register_window, text="Username:", 
              font=("Century Gothic", 24, "bold")).grid(row=3, column=4, sticky="NSEW")

        register_username_entry = Entry(register_window, font=("Century Gothic", 20))
        register_username_entry.grid(row=3, column=5, sticky="EW")
        
        Label(register_window, text="Password:", 
              font=("Century Gothic", 24, "bold")).grid(row=5, column=4, sticky="NSEW")

        register_password_entry = Entry(register_window, show="*", font=("Century Gothic", 20))
        register_password_entry.grid(row=5, column=5, sticky="EW")

        Button(register_window, text="Register", font=("Century Gothic", 18),
               command=lambda: self.register(register_username_entry.get(), register_password_entry.get())).grid(row=7, column=4, columnspan=2, sticky="NSEW")
        
        Button(register_window, text="Back to Login", font=("Century Gothic", 18),
               command=self.open_login_window).grid(row=8, column=4, columnspan=2, sticky="NSEW")

    # Login Menu
    def open_login_window(self):
        self.clear_widgets()
        login_window = Frame(self.master)
        login_window.pack(fill="both", expand=True)

        for i in range(11):
            login_window.grid_rowconfigure(i, weight=1)
            login_window.grid_columnconfigure(i, weight=1)

        Label(login_window, text="Login Page", 
              font=("Century Gothic", 24, "bold")).grid(row=1, column=4, columnspan=2, sticky="NSEW")
        
        Label(login_window, text="Username:", 
              font=("Century Gothic", 24, "bold")).grid(row=3, column=4, sticky="NSEW")
        
        login_username_entry = Entry(login_window, font=("Century Gothic", 20))
        login_username_entry.grid(row=3, column=5, sticky="EW")

        Label(login_window, text="Password:", 
              font=("Century Gothic", 24, "bold")).grid(row=5, column=4, sticky="NSEW")
        
        login_password_entry = Entry(login_window, show="*", font=("Century Gothic", 20))
        login_password_entry.grid(row=5, column=5, sticky="EW")

        Button(login_window, text="Login", font=("Century Gothic", 18),
               command=lambda: self.login(login_username_entry.get(), login_password_entry.get())).grid(row=7, column=4, columnspan=2, sticky="NSEW")
        
        Button(login_window, text="Register", font=("Century Gothic", 18),
               command=self.open_register_window).grid(row=8, column=4, columnspan=2, sticky="NSEW")

    # Login Function for existing users
    def login(self, username, password):
        if username == self.admin.ADMIN_USERNAME:
            if self.admin.login(username, password):
                self.show_admin_menu()
            else:
                messagebox.showerror("Admin Login Error", "Invalid admin credentials.")
        else:
            message = self.voting_system.login(username, password)
            if message == "Login successful!":
                self.current_username = username
                self.show_voting_menu()
            else:
                messagebox.showerror("Login Error", message)

    # Register Function
    def register(self, username, password):
        message = self.voting_system.register(username, password)
        messagebox.showinfo("Registration", message)
        self.open_login_window()

    # Voting Menu
    def show_voting_menu(self):
        self.clear_widgets()
        if not self.voting_system.candidates:
            messagebox.showinfo("Voting Error", "No candidates available. Please contact the admin.")
            self.logout()
            return
        
        Button(self.master, text="Vote", font=("Century Gothic", 18),
            command=self.vote).pack()
        
        Button(self.master, text="Show Results", font=("Century Gothic", 18),
            command=self.show_results).pack()
        
        Button(self.master, text="Logout", font=("Century Gothic", 18),
            command=self.logout).pack()

    # LogOut Function
    def logout(self):
        self.current_username = None
        self.clear_widgets()
        self.create_main_menu()
        self.open_login_window()

    # Vote Function
    def vote(self):
        self.clear_widgets()

        Label(self.master, text="Vote for a Candidate", 
              font=("Century Gothic", 24, "bold")).grid(row=0, column=0, columnspan=3, padx=5, pady=10)
        # Search Section
        Label(self.master, text="Search Candidate:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.search_candidate_entry = Entry(self.master, font=("Century Gothic", 16))
        self.search_candidate_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        search_button = Button(self.master, text="Search", font=("Century Gothic", 12),
                               command=self.search_candidate)
        
        search_button.grid(row=1, column=2, padx=5, pady=5)

        Label(self.master, text="Results:").grid(row=2, column=0, padx=5, pady=5, sticky="ne")

        self.result_listbox = Listbox(self.master, width=50, height=10)
        self.result_listbox.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky="we")
        # Vote Section
        vote_button = Button(self.master, text="Vote", font=("Century Gothic", 14), bg="darkgray",
                             command=self.cast_vote)
        vote_button.grid(row=3, column=1, pady=10)

        back_button = Button(self.master, text="Back", font=("Century Gothic", 14), bg="lightgray",
                             command=self.show_voting_menu)
        back_button.grid(row=4, column=1, pady=10)

    # Search Candidate Function
    def search_candidate(self):
        candidate_name = self.search_candidate_entry.get().strip()
        if candidate_name:
            results = self.voting_system.get_candidates()
            found_candidates = [candidate for candidate in results if candidate_name.lower() in candidate.lower()]
            self.result_listbox.delete(0, END)
            if found_candidates:
                for candidate in found_candidates:
                    self.result_listbox.insert(END, candidate)
            else:
                self.result_listbox.insert(END, "No candidates found.")
        else:
            self.result_listbox.delete(0, END)
            self.result_listbox.insert(END, "No candidate name provided.")

    # Cast Vote Function
    def cast_vote(self):
        selected_candidate = self.result_listbox.get(ANCHOR)
        if not selected_candidate or selected_candidate == "No candidates found.":
            self.result_listbox.delete(0, END)
            self.result_listbox.insert(END, "No candidate selected.")
            return
        if not self.current_username:
            self.result_listbox.delete(0, END)
            self.result_listbox.insert(END, "User not logged in. Please log in first.")
            return
        vote_message = self.voting_system.vote(self.current_username, selected_candidate)
        self.result_listbox.delete(0, END)
        self.result_listbox.insert(END, vote_message)

    # Submit Vote Function
    def submit_vote(self, username, candidate):
        message = self.voting_system.vote(username, candidate)
        messagebox.showinfo("Vote Submission", message)
        self.show_voting_menu(username)

    # Show Results Function
    def show_results(self):
        if not self.current_username:
            messagebox.showerror("Results Error", "You must be logged in to view the results.")
            return
        results = self.voting_system.show_results(self.current_username)
        if isinstance(results, str):  # Assuming errors are returned as strings
            messagebox.showinfo("Results", results)
            return
        if results:
            self.clear_widgets()
            total_votes = sum(results.values())
            labels = list(results.keys())
            sizes = [count / total_votes * 100 for count in results.values()]  # Convert to percentages
            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111)
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')
            canvas = FigureCanvasTkAgg(fig, master=self.master)
            canvas.draw()
            canvas.get_tk_widget().pack()
            Button(self.master, text="Back to Menu",
                   command=self.show_voting_menu).pack()
        else:
            messagebox.showinfo("Results", "No votes recorded yet.")

    # Admin Menu
    def show_admin_menu(self):
        self.clear_widgets()

        Label(self.master, text="Admin Menu",
              font=("Century Gothic", 24, "bold")).place(relx=0.5, rely=0.3, anchor="center")
        
        Button(self.master, text="Manage Candidates", font=("Century Gothic", 18), bg="darkgray",
               fg="black", bd=2, relief="flat",
               command=self.manage_candidates).place(relx=0.5, rely=0.4, anchor="center")
        
        Button(self.master, text="Show/Hide Results", font=("Century Gothic", 18), bg="darkgray",
               fg="black", bd=5, relief="flat",
               command=self.toggle_results_visibility).place(relx=0.5, rely=0.5, anchor="center")
        
        Button(self.master, text="Logout", font=("Century Gothic", 18), bg="darkgray",
               fg="black", bd=2, relief="flat",
               command=self.logout).place(relx=0.5, rely=0.6, anchor="center")

    # Toggle Results Visibility Function
    def toggle_results_visibility(self):
        visibility = self.admin.toggle_results_visibility()
        status = "visible" if visibility else "hidden"
        messagebox.showinfo("Results Visibility", f"Results are now {status} at this time.")

    # Manage Candidates Function
    def manage_candidates(self):
        self.clear_widgets()

        Label(self.master, text="Add/Modify Candidates (comma-separated):").pack()

        candidates_entry = Entry(self.master)
        candidates_entry.pack()

        Button(self.master, text="Add Candidates", font=("Century Gothic", 18),
               command=lambda: self.admin.add_candidates(candidates_entry.get())).pack()
        
        Button(self.master, text="Remove Candidates", font=("Century Gothic", 18),
               command=lambda: self.admin.remove_candidate(candidates_entry.get())).pack()
        
        Button(self.master, text="Reset Candidate List", font=("Century Gothic", 18),
               command=lambda: self.admin.reset_candidates(candidates_entry.get())).pack()
        
        Button(self.master, text="Back to Admin Menu", font=("Century Gothic", 18),
               command=self.show_admin_menu).pack()

    # Clear Widgets Function
    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()