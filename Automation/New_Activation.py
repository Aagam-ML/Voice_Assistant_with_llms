import subprocess

def get_reminders():
    script = '''
    tell application "Reminders"
        set reminderList to ""
        repeat with reminderListObject in lists
            set reminderList to reminderList & name of reminderListObject & ":"
            repeat with reminderObject in reminders of reminderListObject
                set reminderList to reminderList & name of reminderObject & ", "
            end repeat
        end repeat
        return reminderList
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    print(result.stdout)

def add_reminder(list_name, reminder_name):
    script = f'''
    tell application "Reminders"
        set reminderList to first list whose name is "{list_name}"
        make new reminder at end of reminders of reminderList with properties {{name:"{reminder_name}"}}
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully added '{reminder_name}' to the '{list_name}' list.")
    else:
        print(f"Error: {result.stderr}")

# Example usage
def remove_all_reminders(list_name):
    script = f'''
    tell application "Reminders"
        set reminderList to first list whose name is "{list_name}"
        delete reminders of reminderList
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully removed all reminders from the '{list_name}' list.")
    else:
        print(f"Error: {result.stderr}")

remove_all_reminders("Personal")