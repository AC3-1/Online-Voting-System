import tkinter as tk
from voting_system import file_wipe, VOTE_FILE, VOTER_FILE
from voting_app import VotingApp

if __name__ == "__main__":
    # Icomment pag mag ddemo na
    #file_wipe(VOTE_FILE)
    #file_wipe(VOTER_FILE)

    win = tk.Tk()
    win.geometry(f"1280x800+{(win.winfo_screenwidth()-1280)//2}+{(win.winfo_screenheight()-800)//2}")  
    app = VotingApp(win)
    win.mainloop()