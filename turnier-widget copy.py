import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

# Global variables
matches = []

# Function to fetch matches from API
def fetch_matches_from_api():
    url = 'https://primebot.me/api/v1/v1_matches_list'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            messagebox.showerror('API Error', f'Failed to fetch data from API. Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Connection Error', f'Error connecting to API: {str(e)}')
    return []

# Function to display matches
def display_matches():
    matches_container.delete(*matches_container.get_children())
    for idx, match in enumerate(matches, start=1):
        result_class = ''
        if 'result' in match:
            if match['result'] == 'Win':
                result_class = 'win'
            elif match['result'] == 'Draw':
                result_class = 'draw'
            elif match['result'] == 'Lose':
                result_class = 'lose'
        
        team_a = match['teams'][0]
        team_b = match['teams'][1]
        
        matches_container.insert('', 'end', iid=f'M{idx}', values=(match['time'], team_a, team_b, match.get('result', '')), tags=(result_class,))

# Function to update result of a match
def update_result():
    selected_item = matches_container.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a match.')
        return
    
    try:
        index = int(selected_item[0][1:])  # Extract index from item ID
        result = result_var.get()
        matches[index - 1]['result'] = result  # Adjust index to match list index
        save_matches()
        display_matches()
    except IndexError:
        messagebox.showerror('Error', 'Invalid selection. Please select a valid match.')

# Function to add a new match
def add_match():
    new_match_time = new_match_time_entry.get().strip()
    new_match_team_a = new_match_team_a_entry.get().strip()
    new_match_team_b = new_match_team_b_entry.get().strip()
    
    if new_match_time and new_match_team_a and new_match_team_b:
        new_match = {'time': new_match_time, 'teams': [new_match_team_a, new_match_team_b]}
        matches.append(new_match)
        save_matches()
        display_matches()
        new_match_time_entry.delete(0, 'end')
        new_match_team_a_entry.delete(0, 'end')
        new_match_team_b_entry.delete(0, 'end')

# Function to delete all matches
def delete_all_matches():
    global matches
    matches = []
    save_matches()
    display_matches()

# Function to save matches to JSON
def save_matches():
    with open('matches.json', 'w') as f:
        json.dump(matches, f)

# Function to export matches to HTML
def export_to_html():
    try:
        with open('turnier-widget.html', 'w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html lang="de">\n')
            f.write('<head>\n')
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write('    <title>Turnier-Widget</title>\n')
            f.write('    <style>\n')
            f.write('        body {\n')
            f.write('            font-family: Arial, sans-serif;\n')
            f.write('            background-color: #f0f0f0;\n')
            f.write('            display: flex;\n')
            f.write('            justify-content: center;\n')
            f.write('            align-items: center;\n')
            f.write('            height: 100vh;\n')
            f.write('            margin: 0;\n')
            f.write('            position: relative;\n')
            f.write('        }\n')
            f.write('        #widget {\n')
            f.write('            background: #ffffff;\n')
            f.write('            padding: 20px;\n')
            f.write('            border-radius: 8px;\n')
            f.write('            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);\n')
            f.write('            width: 350px;\n')
            f.write('            max-width: 100%;\n')
            f.write('        }\n')
            f.write('        .match {\n')
            f.write('            margin-bottom: 20px;\n')
            f.write('            padding: 15px;\n')
            f.write('            border-radius: 8px;\n')
            f.write('            border-left: 5px solid #3498db;\n')
            f.write('            background-color: #f0f0f0;\n')
            f.write('        }\n')
            f.write('        .match.win {\n')
            f.write('            border-left-color: #2ecc71;\n')
            f.write('        }\n')
            f.write('        .match.draw {\n')
            f.write('            border-left-color: #95a5a6;\n')
            f.write('        }\n')
            f.write('        .match.lose {\n')
            f.write('            border-left-color: #e74c3c;\n')
            f.write('        }\n')
            f.write('        .time {\n')
            f.write('            font-size: 18px;\n')
            f.write('            font-weight: bold;\n')
            f.write('            margin-bottom: 10px;\n')
            f.write('            color: #27ae60;\n')
            f.write('        }\n')
            f.write('        .title {\n')
            f.write('            text-align: center;\n')
            f.write('            color: #27ae60;\n')
            f.write('            font-size: 24px;\n')
            f.write('            font-weight: bold;\n')
            f.write('            margin-bottom: 20px;\n')
            f.write('        }\n')
            f.write('        .teams {\n')
            f.write('            display: flex;\n')
            f.write('            justify-content: space-between;\n')
            f.write('            align-items: center;\n')
            f.write('            margin-bottom: 10px;\n')
            f.write('        }\n')
            f.write('        .team {\n')
            f.write('            font-size: 16px;\n')
            f.write('            font-weight: bold;\n')
            f.write('            color: #333333;\n')
            f.write('        }\n')
            f.write('        .result {\n')
            f.write('            font-size: 14px;\n')
            f.write('            font-weight: bold;\n')
            f.write('            padding: 5px 10px;\n')
            f.write('            border-radius: 4px;\n')
            f.write('            color: #ffffff;\n')
            f.write('            text-transform: uppercase;\n')
            f.write('            display: inline-block;\n')
            f.write('            width: 60px;\n')
            f.write('            text-align: center;\n')
            f.write('        }\n')
            f.write('        .result.win {\n')
            f.write('            background-color: #2ecc71;\n')
            f.write('        }\n')
            f.write('        .result.draw {\n')
            f.write('            background-color: #95a5a6;\n')
            f.write('        }\n')
            f.write('        .result.lose {\n')
            f.write('            background-color: #e74c3c;\n')
            f.write('        }\n')
            f.write('    </style>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write('    <div id="widget">\n')
            f.write('        <h2 class="title">Turnier Matches</h2>\n')
            f.write('        <div id="matches">\n')

            for idx, match in enumerate(matches, start=1):
                f.write('            <div class="match">\n')
                f.write(f'                <div class="time">{match["time"]}</div>\n')
                f.write('                <div class="teams">\n')
                f.write(f'                    <span class="team">{match["teams"][0]}</span>\n')
                if match.get('result'):
                    result_class = match['result'].lower()
                    f.write(f'                    <span class="result {result_class}">{match["result"]}</span>\n')
                f.write('                </div>\n')
                f.write('                <div class="teams">\n')
                f.write(f'                    <span class="team">{match["teams"][1]}</span>\n')
                f.write('                </div>\n')
                f.write('            </div>\n')

            f.write('        </div>\n')
            f.write('    </div>\n')
            f.write('</body>\n')
            f.write('</html>\n')

        messagebox.showinfo('Export Successful', 'Matches have been exported to turnier-widget.html')
    except Exception as e:
        messagebox.showerror('Export Error', f'An error occurred during export: {str(e)}')

# Function to fetch and display matches from API
def fetch_and_display_matches():
    global matches
    matches = fetch_matches_from_api()
    display_matches()

# Initialize tkinter
root = tk.Tk()
root.title('Turnier-Widget')

# Create widgets
matches_frame = ttk.Frame(root)
matches_frame.pack(padx=10, pady=10)

matches_container = ttk.Treeview(matches_frame, columns=('Time', 'Team A', 'Team B', 'Result'), show='headings', height=10)
matches_container.heading('Time', text='Time')
matches_container.heading('Team A', text='Team A')
matches_container.heading('Team B', text='Team B')
matches_container.heading('Result', text='Result')
matches_container.column('Time', width=100)
matches_container.column('Team A', width=150)
matches_container.column('Team B', width=150)
matches_container.column('Result', width=100)
matches_container.pack(padx=10, pady=10)

result_var = tk.StringVar(root)
result_var.set('')  # Default value

result_option_menu = ttk.OptionMenu(root, result_var, '', 'Win', 'Draw', 'Lose')
result_option_menu.pack(pady=5)

update_result_button = ttk.Button(root, text='Update Result', command=update_result)
update_result_button.pack(pady=5)

new_match_frame = ttk.Frame(root)
new_match_frame.pack(pady=10)

new_match_time_label = ttk.Label(new_match_frame, text='Time:')
new_match_time_label.grid(row=0, column=0, padx=5, pady=5)
new_match_time_entry = ttk.Entry(new_match_frame)
new_match_time_entry.grid(row=0, column=1, padx=5, pady=5)

new_match_team_a_label = ttk.Label(new_match_frame, text='Team A:')
new_match_team_a_label.grid(row=1, column=0, padx=5, pady=5)
new_match_team_a_entry = ttk.Entry(new_match_frame)
new_match_team_a_entry.grid(row=1, column=1, padx=5, pady=5)

new_match_team_b_label = ttk.Label(new_match_frame, text='Team B:')
new_match_team_b_label.grid(row=2, column=0, padx=5, pady=5)
new_match_team_b_entry = ttk.Entry(new_match_frame)
new_match_team_b_entry.grid(row=2, column=1, padx=5, pady=5)

add_match_button = ttk.Button(new_match_frame, text='Add Match', command=add_match)
add_match_button.grid(row=3, columnspan=2, padx=5, pady=10)

delete_all_button = ttk.Button(root, text='Delete All Matches', command=delete_all_matches)
delete_all_button.pack(pady=10)

export_button = ttk.Button(root, text='Export to HTML', command=export_to_html)
export_button.pack(pady=10)

# Button to fetch matches from API
fetch_from_api_button = ttk.Button(root, text='Fetch Matches from API', command=fetch_and_display_matches)
fetch_from_api_button.pack(pady=10)

# Load initial matches from JSON file
try:
    with open('matches.json', 'r') as f:
        matches = json.load(f)
except FileNotFoundError:
    pass

# Display matches initially
display_matches()

# Run the tkinter main loop
root.mainloop()

