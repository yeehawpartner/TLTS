import tkinter as tk
import pandas as pd
import os
from tkinter import messagebox


EXCEL_FILE_PATH = "fantasy_teams.xlsx"


class FantasyBasketballApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The League IRS Tracking System (TLTS)")
        self.root.geometry("1450x1000")

        self.root.configure(bg="#141414")

        # Add title "IRS" at the top center
        title_label = tk.Label(self.root, text="IRS", bg="#141414", fg="darkgoldenrod", font=("Papyrus", 64, "bold"))
        title_label.pack(pady=20)

        # Load team data from Excel
        self.teams_data = self.load_teams_data()

        # Create team display area under the title
        self.team_frames = []
        self.create_team_grid()

        # Create add team section at the bottom
        self.create_add_team_section()

    def load_teams_data(self):
        """Load team data from the Excel file or create a new one if it doesn't exist."""
        if os.path.exists(EXCEL_FILE_PATH):
            return pd.read_excel(EXCEL_FILE_PATH).to_dict(orient="records")
        else:
            df = pd.DataFrame(columns=["Team Name", "Trades Made", "Infractions Taken", "Waivers Claimed"])
            df.to_excel(EXCEL_FILE_PATH, index=False)
            return []

    def save_teams_data(self):
        """Save the current teams data to the Excel file."""
        df = pd.DataFrame(self.teams_data)
        df.to_excel(EXCEL_FILE_PATH, index=False)

    def create_team_grid(self):
        """Create a grid of teams with stats and buttons."""
        for frame in self.team_frames:
            frame.destroy()

        self.team_frames.clear()

        teams_container = tk.Frame(self.root, bg="#4b4b4b")
        teams_container.pack(pady=10)

        for idx, team in enumerate(self.teams_data):
            team_frame = tk.Frame(teams_container, bg="lightgray", relief="groove", padx=10, pady=10)
            team_frame.grid(row=idx // 4, column=idx % 4, padx=10, pady=10, sticky="nsew")
            self.team_frames.append(team_frame)

            team_name_label = tk.Label(
                team_frame, text=team["Team Name"], bg="lightgray", fg="black", font=("Boulder", 24, "bold")
            )
            team_name_label.pack(pady=(5, 10))

            self.update_team_name_color(team, team_name_label)
            self.create_stat_section(team_frame, team, idx)

            delete_button = tk.Button(
                team_frame, text="Delete Team", command=lambda index=idx: self.delete_team(index), bg="red", fg="white"
            )
            delete_button.pack(pady=5)

        for i in range(4):
            teams_container.grid_columnconfigure(i, weight=1)

    def update_team_name_color(self, team, label):
        infractions = team["Infractions Taken"]
        if infractions >= 50:
            label.config(fg="red")
        elif infractions >= 40:
            label.config(fg="orange")

    def create_stat_section(self, frame, team, index):
        trades_frame = tk.Frame(frame, bg="lightgray")
        trades_frame.pack(pady=5)

        trades_label = tk.Label(trades_frame, text=f"Trades Made: {team['Trades Made']}", bg="lightgray", font=("Arial", 14))
        trades_label.pack(side=tk.LEFT)

        trades_minus_button = tk.Button(trades_frame, text="-",
                                        command=lambda: self.decrement_stat(index, "Trades Made", trades_label),
                                        bg="white", fg="black")
        trades_minus_button.pack(side=tk.LEFT)

        trades_plus_button = tk.Button(trades_frame, text="+",
                                       command=lambda: self.increment_stat(index, "Trades Made", trades_label),
                                       bg="white", fg="black")
        trades_plus_button.pack(side=tk.LEFT)

        infractions_frame = tk.Frame(frame, bg="lightgray")
        infractions_frame.pack(pady=5)

        infractions_label = tk.Label(infractions_frame, text=f"Infractions Taken: {team['Infractions Taken']}",
                                     bg="lightgray", font=("Arial", 14))
        infractions_label.pack(side=tk.LEFT)

        infractions_minus_button = tk.Button(infractions_frame, text="-",
                                             command=lambda: self.decrement_stat(index, "Infractions Taken",
                                                                                 infractions_label), bg="white",
                                             fg="black")
        infractions_minus_button.pack(side=tk.LEFT)

        infractions_plus_button = tk.Button(infractions_frame, text="+",
                                            command=lambda: self.increment_stat(index, "Infractions Taken",
                                                                                infractions_label), bg="white",
                                            fg="black")
        infractions_plus_button.pack(side=tk.LEFT)

        waivers_frame = tk.Frame(frame, bg="lightgray")
        waivers_frame.pack(pady=5)

        waivers_label = tk.Label(waivers_frame, text=f"Waivers Claimed: {team['Waivers Claimed']}", bg="lightgray",
                                 font=("Arial", 14))
        waivers_label.pack(side=tk.LEFT)

        waivers_minus_button = tk.Button(waivers_frame, text="-",
                                         command=lambda: self.decrement_stat(index, "Waivers Claimed", waivers_label),
                                         bg="white", fg="black")
        waivers_minus_button.pack(side=tk.LEFT)

        waivers_plus_button = tk.Button(waivers_frame, text="+",
                                        command=lambda: self.increment_stat(index, "Waivers Claimed", waivers_label),
                                        bg="white", fg="black")
        waivers_plus_button.pack(side=tk.LEFT)

    def increment_stat(self, team_index, stat_key, label):
        self.teams_data[team_index][stat_key] += 1
        label.config(text=f"{stat_key}: {self.teams_data[team_index][stat_key]}")
        self.update_team_name_color(self.teams_data[team_index], label.master.master.winfo_children()[0])
        self.save_teams_data()

    def decrement_stat(self, team_index, stat_key, label):
        if self.teams_data[team_index][stat_key] > 0:
            self.teams_data[team_index][stat_key] -= 1
            label.config(text=f"{stat_key}: {self.teams_data[team_index][stat_key]}")
            self.update_team_name_color(self.teams_data[team_index], label.master.master.winfo_children()[0])
            self.save_teams_data()

    def create_add_team_section(self):
        add_team_frame = tk.Frame(self.root, bg="#4b4b4b", pady=20)
        add_team_frame.pack(side=tk.BOTTOM, fill=tk.X)

        add_team_label = tk.Label(add_team_frame, text="Add New Team:", bg="#4b4b4b", fg="white", font=("Arial", 14))
        add_team_label.pack(side=tk.LEFT, padx=10)

        self.new_team_entry = tk.Entry(add_team_frame, font=("Arial", 14), width=25)
        self.new_team_entry.pack(side=tk.LEFT, padx=10)

        add_team_button = tk.Button(add_team_frame, text="Add Team", command=self.add_team, bg="darkgoldenrod", fg="black",
                                    font=("Arial", 12))
        add_team_button.pack(side=tk.LEFT, padx=10)

        export_button = tk.Button(add_team_frame, text="Export Excel", command=self.export_excel, bg="darkgoldenrod", fg="black",
                                  font=("Arial", 12))
        export_button.pack(side=tk.LEFT, padx=10)

    def add_team(self):
        team_name = self.new_team_entry.get().strip()
        if team_name and team_name not in [team["Team Name"] for team in self.teams_data]:
            new_team = {"Team Name": team_name, "Trades Made": 0, "Infractions Taken": 0, "Waivers Claimed": 0}
            self.teams_data.append(new_team)
            self.save_teams_data()
            self.new_team_entry.delete(0, tk.END)
            self.refresh_display()
        elif team_name:
            messagebox.showwarning("Duplicate Entry", "This team already exists.")

    def delete_team(self, team_index):
        team_name = self.teams_data[team_index]["Team Name"]
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{team_name}'?"):
            del self.teams_data[team_index]
            self.save_teams_data()
            self.refresh_display()

    def refresh_display(self):
        self.create_team_grid()

    def export_excel(self):
        self.save_teams_data()
        messagebox.showinfo("Export Successful", "Teams data has been exported to Excel.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FantasyBasketballApp(root)
    root.mainloop()
