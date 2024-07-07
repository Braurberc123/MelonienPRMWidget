import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv  # Import CSV module for exporting to CSV
import re
from tkinter import filedialog  # Import regular expression module for validation

# Global variables
matches = []

def import_from_csv(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            imported_matches = []
            for row in reader:
                match = {
                    'time': row['Time'],
                    'teams': [row['Team A'], row['Team B']],
                    'result': row.get('Result', '')  # Optional: Check if 'Result' exists in the CSV
                }
                imported_matches.append(match)
            
            # Merge imported matches with existing matches
            matches.extend(imported_matches)
            save_matches()
            display_matches()
            messagebox.showinfo('Import Successful', f'Matches imported from {file_path}')
    except FileNotFoundError:
        messagebox.showerror('File Not Found', f'File not found: {file_path}')
    except Exception as e:
        messagebox.showerror('Import Error', f'An error occurred during import: {str(e)}')

# Function to save matches to JSON
def save_matches():
    with open('matches.json', 'w') as f:
        json.dump(matches, f)

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
    new_match_datetime = new_match_datetime_entry.get().strip()
    new_match_team_a = new_match_team_a_entry.get().strip()
    new_match_team_b = new_match_team_b_entry.get().strip()
    
    # Validate date-time format using regular expression
    if not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', new_match_datetime):
        messagebox.showerror('Invalid Date-Time', 'Please enter a valid date-time in YYYY-MM-DD HH:MM format.')
        return
    
    if new_match_datetime and new_match_team_a and new_match_team_b:
        new_match = {'time': new_match_datetime, 'teams': [new_match_team_a, new_match_team_b]}
        matches.append(new_match)
        save_matches()
        display_matches()
        new_match_datetime_entry.delete(0, 'end')
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
            f.write('            overflow: auto; /* Enable scrolling */\n')
            f.write('            height: 70vh; /* Limit height for scrolling */\n')
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

            # JavaScript for automatic scrolling
            f.write('    <script>\n')
            f.write('    // Function to scroll the page automatically\n')
            f.write('    function autoScroll() {\n')
            f.write('        var widget = document.getElementById("widget");\n')
            f.write('        widget.scrollTop += 1; // Scroll down by 1 pixel\n')
            f.write('        if (widget.scrollTop >= widget.scrollHeight - widget.clientHeight) {\n')
            f.write('            widget.scrollTop = 0; // Start over from the top\n')
            f.write('        }\n')
            f.write('    }\n')

            f.write('    // Call autoScroll function periodically\n')
            f.write('    setInterval(autoScroll, 100); // Adjust scroll speed here\n')
            f.write('    </script>\n')

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

def export_to_csv():
    try:
        with open('matches.csv', 'w', newline='') as csvfile:
            fieldnames = ['Time', 'Team A', 'Team B', 'Result']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for match in matches:
                writer.writerow({
                    'Time': match['time'],
                    'Team A': match['teams'][0],
                    'Team B': match['teams'][1],
                    'Result': match.get('result', '')  # Optional: Check if 'result' exists in match
                })
        
        messagebox.showinfo('Export Successful', 'Matches have been exported to matches.csv')
    except Exception as e:
        messagebox.showerror('Export Error', f'An error occurred during export: {str(e)}')

def save_matches():
    with open('matches.json', 'w') as f:
        json.dump(matches, f)

# Initialize Tkinter
root = tk.Tk()
root.title('Turnier Widget')

# Main frame
main_frame = ttk.Frame(root, padding='20')
main_frame.grid(row=0, column=0)

# Matches container
matches_container = ttk.Treeview(main_frame, columns=('Time', 'Team A', 'Team B', 'Result'), show='headings', height=10)
matches_container.heading('Time', text='Time')
matches_container.heading('Team A', text='Team A')
matches_container.heading('Team B', text='Team B')
matches_container.heading('Result', text='Result')
matches_container.column('Time', width=150)
matches_container.column('Team A', width=150)
matches_container.column('Team B', width=150)
matches_container.column('Result', width=100)
matches_container.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Result options
result_var = tk.StringVar()
result_var.set('')  # Initialize with empty result

result_label = ttk.Label(main_frame, text='Result:')
result_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

result_combobox = ttk.Combobox(main_frame, textvariable=result_var, values=['Win', 'Draw', 'Lose'])
result_combobox.grid(row=1, column=1, padx=10, pady=10)

update_result_button = ttk.Button(main_frame, text='Update Result', command=update_result)
update_result_button.grid(row=1, column=2, padx=10, pady=10)

# Add match section
new_match_frame = ttk.LabelFrame(main_frame, text='Add New Match')
new_match_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

new_match_datetime_label = ttk.Label(new_match_frame, text='Date-Time (YYYY-MM-DD HH:MM):')
new_match_datetime_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

new_match_datetime_entry = ttk.Entry(new_match_frame, width=20)
new_match_datetime_entry.grid(row=0, column=1, padx=10, pady=5)

new_match_team_a_label = ttk.Label(new_match_frame, text='Team A:')
new_match_team_a_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

new_match_team_a_entry = ttk.Entry(new_match_frame, width=20)
new_match_team_a_entry.grid(row=1, column=1, padx=10, pady=5)

new_match_team_b_label = ttk.Label(new_match_frame, text='Team B:')
new_match_team_b_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

new_match_team_b_entry = ttk.Entry(new_match_frame, width=20)
new_match_team_b_entry.grid(row=2, column=1, padx=10, pady=5)

add_match_button = ttk.Button(new_match_frame, text='Add Match', command=add_match)
add_match_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Delete all matches button
delete_all_button = ttk.Button(main_frame, text='Delete All Matches', command=delete_all_matches)
delete_all_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Export buttons
export_html_button = ttk.Button(main_frame, text='Export to HTML', command=export_to_html)
export_html_button.grid(row=4, column=0, padx=10, pady=10)

export_csv_button = ttk.Button(main_frame, text='Export to CSV', command=export_to_csv)
export_csv_button.grid(row=4, column=1, padx=10, pady=10)

# Import button
def import_from_csv_gui():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        import_from_csv(file_path)

import_button = ttk.Button(main_frame, text='Import from CSV', command=import_from_csv_gui)
import_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Display matches initially
display_matches()

# Run the main loop
root.mainloop()