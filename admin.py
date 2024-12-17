from voting_system import VotingSystem, save_candidates
from tkinter import messagebox


class Admin:
    def __init__(self, voting_system):
        self.ADMIN_USERNAME = "admin"
        self.ADMIN_PASSWORD = "1"
        self.voting_system = voting_system

    # Admin Login Function
    def login(self, username, password):
        return username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD

    # Add Candidates Function
    def add_candidates(self, candidates):
        # Split the input string into a list of candidate names, stripping whitespace
        candidates_list = [candidate.strip() for candidate in candidates.split(",") if candidate.strip()]

        if not candidates_list:
            messagebox.showerror("Error", "No valid candidates provided.")
            return

        added_candidates = []
        skipped_candidates = []

        for candidate in candidates_list:
            if candidate not in self.voting_system.candidates:
                self.voting_system.candidates.append(candidate)
                added_candidates.append(candidate)
            else:
                skipped_candidates.append(candidate)

        # Save the updated candidate list
        save_candidates(self.voting_system.candidates)

        # Construct the message for feedback
        message = ""
        if added_candidates:
            message += f"Added candidates: {', '.join(added_candidates)}.\n"
        if skipped_candidates:
            message += f"Skipped duplicates: {', '.join(skipped_candidates)}."

        # Show success or mixed feedback
        messagebox.showinfo("Manage Candidates", message if message else "No changes made.")

    # Remove Candidates Function
    def remove_candidate(self, candidate):
        # Remove a candidate from the list if present
        candidate = candidate.strip()
        if candidate in self.voting_system.candidates:
            self.voting_system.candidates.remove(candidate)
            save_candidates(self.voting_system.candidates)
            messagebox.showinfo("Manage Candidates", f"Candidate '{candidate}' removed successfully.")
        else:
            messagebox.showerror("Manage Candidates", f"Candidate '{candidate}' does not exist.")

    # Reset Candidate ListFunction
    def reset_candidates(self, candidates):
        # Replace the entire candidate list with a new list
        if not candidates:
            self.voting_system.candidates = []
            messagebox.showinfo("Manage Candidates", "Candidate list has been reset to empty.")
        else:
            unique_candidates = list({candidate.strip() for candidate in candidates.split(",") if candidate.strip()})
            self.voting_system.candidates = [candidate.strip() for candidate in candidates.split(",") if candidate.strip()]
            messagebox.showinfo("Manage Candidates", "Candidate list has been reset.")
        save_candidates(self.voting_system.candidates)

    # Admin Toggle Results Visibility 
    def toggle_results_visibility(self):
        visibility = self.voting_system.toggle_results_visibility()
        return visibility