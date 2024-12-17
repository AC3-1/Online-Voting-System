import os
import argon2
from  argon2.exceptions import VerifyMismatchError

VOTER_FILE = "voters.txt"
VOTE_FILE = "votes.txt"
CANDIDATE_FILE = "candidates.txt"

# File Wipe Function (for testing purposes)
def file_wipe(file_path):
    with open(file_path, 'w') as file:
        pass

# Load Voters from the voters file into a dictionary
def load_voters():
    voters = {}
    if os.path.exists(VOTER_FILE):
        with open(VOTER_FILE, 'r') as file:
            for line in file:
                username, _ = line.strip().split('|')
                voters[username] = None
    return voters
 
# Save the votes to the votes file
def save_vote(username, candidate):
    with open(VOTE_FILE, 'a') as file:
        file.write(f"{username}|{candidate}\n")

# Load votes from the votes file
def load_votes():
    votes = {}
    if os.path.exists(VOTE_FILE):
        with open(VOTE_FILE, 'r') as file:
            for line in file:
                username, candidate = line.strip().split('|')
                votes[username] = candidate
    return votes

# Load candidates from the candidates file
def load_candidates():
    candidates = []
    if os.path.exists(CANDIDATE_FILE):
        with open(CANDIDATE_FILE, 'r') as file:
            for line in file:
                candidates.append(line.strip())
    return candidates

# Save candidates to the candidates file
def save_candidates(candidates):
    with open(CANDIDATE_FILE, 'w') as file:
        for candidate in candidates:
            file.write(f"{candidate}\n")

class BST_Node: #  NEW UPDATE
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key

class BinarySearchTree: #   NEW UPDATE
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = BST_Node(key)
        else:
            self.push(self.root, key)

    def push(self, node, key):
        if str(key) < str(node.value):
            if node.left is None:
                node.left = BST_Node(key)
            else:
                self.push(node.left, key)
        else:
            if node.right is None:
                node.right = BST_Node(key)
            else:
                self.push(node.right, key)

    def search(self, value):
        return self.peek(self.root, value)

    def peek(self, node, value):
        if node is None or node.value == value:
            return node is not None
        if str(value) < str(node.value):
            return self.peek(node.left, value)
        return self.peek(node.right, value)

    def get_candidates_from_file(self):
        file_path = "candidates.txt"
        candidates = {}
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    values = file.read().splitlines()
                    for value in values:
                        candidates[value] = self.insert(str(value))
            return candidates
        except Exception as error:
            print(f"An error occurred: {error}")

class VotingSystem:
    def __init__(self):
        self.voters = load_voters()
        self.votes = load_votes()
        self.candidates = load_candidates()
        self.results_visible = False
    
    # Hash the voters password
    def hash_password(self, password):
        password_hasher = argon2.PasswordHasher()
        hashed = password_hasher.hash(password)
        return hashed
    
    # Verify the voters password
    def verify_password(self, username, password):
        password_hasher = argon2.PasswordHasher()
        stored_hashed = self.get_stored_hash(username)
        if not stored_hashed:
            return False
        try: 
            password_hasher.verify(stored_hashed, password) 
            return True 
        except VerifyMismatchError: 
            return False
        
    # Get the stored hashed password
    def get_stored_hash(self, username):
        if not os.path.exists(VOTER_FILE):
            return None
        with open(VOTER_FILE, 'r') as file:
            for line in file:
                stored_username, stored_hashed = line.strip().split('|')
                if stored_username == username:
                    return stored_hashed
        return None
    
    # Save the hashed password
    def save_hash_password(self, username, password):
        hash_password = self.hash_password(password)
        if '|' in username:
            raise ValueError("Invalid username: contains a pipe character '|'.")
        with open(VOTER_FILE, "a") as file:
            file.write(f"{username}|{hash_password}\n")  

    # Check if the password needs to be rehashed
    def check_verified_password(self):
        password_hasher = argon2.PasswordHasher()
        return password_hasher.check_needs_rehash(self.verify_password)

    # Register a new voter
    def register(self, username, password):
        if not username.strip():
            return "Invalid username. Username cannot be blank."
        if not password.strip():
            return "Invalid password. Password cannot be blank."
        if '|' in username:
            return "Invalid username. Commas are not allowed."
        if '|' in password:
            return "Invalid password. Commas are not allowed."
        if username in self.voters:
            return "Username already exists."
        self.voters[username] = None
        self.save_hash_password(username, password)
        return "Registration successful!"

    # Log in a voter function
    def login(self, username, password):
        if not username.strip():
            return "Invalid username. Username cannot be blank."
        if not password.strip():
            return "Invalid password. Password cannot be blank."
        if username in self.voters and self.verify_password(username, password):
            return "Login successful!"
        return "Invalid username or password."

    # Cast a vote function
    def vote(self, username, candidate):
        if username in self.votes:
            return "You have already voted."
        bst = BinarySearchTree()
        bst.get_candidates_from_file()
        if not bst.search(candidate):
            return "Invalid candidate."
        self.votes[username] = candidate
        save_vote(username, candidate)
        return "Your vote has been recorded."
  
    # Show the results function
    def show_results(self, username):
        if not self.results_visible:
            return "Results are currently hidden at this time."
        if username not in self.votes:
            return "You must vote to see the results."
        candidates_count = {}
        for candidate in self.votes.values():
            candidates_count[candidate] = candidates_count.get(candidate, 0) + 1
        return candidates_count
    
    # Toggle the results visibility
    def toggle_results_visibility(self):
        self.results_visible = not self.results_visible
        return self.results_visible
    
    def get_candidates(self):
        return self.candidates