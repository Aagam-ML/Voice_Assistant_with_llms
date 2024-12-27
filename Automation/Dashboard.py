from appscript import app

reminders = app('Reminders')
all_lists = reminders.lists()

for reminder_list in all_lists:
    print(f"List: {reminder_list.name()}")
    for reminder in reminder_list.reminders():
        print(f"  Reminder: {reminder.name()} (Completed: {reminder.completed()})")
