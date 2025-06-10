import os
import json
import argparse
from datetime import datetime

current_dir = os.path.dirname(__file__)
Database = os.path.join(current_dir, 'Data.json')

def waktu():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_tugas():
    if not os.path.exists(Database):
        return []
    with open(Database, 'r') as f:
        return json.load(f)
    
def save_tugas(tasks):
    with open(Database, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_tugas(title):
    tasks = load_tugas() 
    next_id = max([t['id'] for t in tasks]) + 1 if tasks else 1
    
    tugas = {
        'id': next_id,
        'title': title, 
        'status': "todo", 
        'created_at': waktu(), 
        'updated_at': "-" 
    }
    tasks.append(tugas)
    save_tugas(tasks)
    print(f"Tugas '{title}' berhasil ditambahkan dengan ID {next_id}.")
    
def update_tugas(tugas_id, title):
    tasks = load_tugas()
    found_tugas = False 
    for tugas in tasks:
        if tugas["id"] == tugas_id: 
            tugas["title"] = title
            tugas["updated_at"] = waktu() 
            save_tugas(tasks)
            print(f"Tugas ID {tugas_id} berhasil diupdate.")
            found_tugas = True
            break 
    if not found_tugas: 
        print(f'ID {tugas_id} tidak ditemukan')

def delete_tugas(tugas_id):
    tasks = load_tugas()
    filtered_tasks = [t for t in tasks if t["id"] != tugas_id]
    
    if len(filtered_tasks) < len(tasks): 
        save_tugas(filtered_tasks) 
        print(f"Tugas ID {tugas_id} berhasil dihapus.")
    else:
        print(f'ID {tugas_id} tidak ditemukan')

def status_tugas(status, tugas_id):
    tasks = load_tugas()
    valid_status = ["todo", "in-progress", "done"]
    
    if status not in valid_status:
        return print(f'Status tidak valid. Gunakan status: {", ".join(valid_status)}')
    
    found_tugas = False
    for tugas in tasks:
        if tugas["id"] == tugas_id:
            tugas["status"] = status
            tugas["updated_at"] = waktu() 
            save_tugas(tasks)
            print(f"Status tugas ID {tugas_id} berhasil diupdate menjadi '{status}'.")
            found_tugas = True
            break 
    
    if not found_tugas: 
        print(f'ID {tugas_id} tidak ditemukan')

def display_tugas(tugas):
    # Helper function to print a single task's details.
    print (f'ID: {tugas["id"]}')
    print (f'Judul: {tugas.get("title", "N/A")}') 
    print (f'Status: {tugas.get("status", "N/A")}')
    print (f'Dibuat Pada: {tugas.get("created_at", "N/A")}') 
    print (f'Di Edit Pada: {tugas.get("updated_at", "N/A")}') 
    print ("-" * 30)

def list_tugas(filter_status=None): # Combined List_tugas and List_tugas_status
    tasks = load_tugas()
    
    if filter_status == "in progress":
        filter_status = "in-progress"

    if filter_status:
        valid_status = ["todo", "in-progress", "done"] # Corrected internal valid status
        if filter_status not in valid_status:
            return print(f'Status filter tidak valid. Gunakan status: {", ".join(valid_status)}')

    found_any_task = False
    
    for tugas in tasks:
        # Check if filter_status is provided AND matches, OR if no filter_status is provided
        if filter_status is None or tugas.get("status") == filter_status:
            display_tugas(tugas)
            found_any_task = True
    
    if not found_any_task:
        if filter_status:
            print(f'Tidak ada tugas dengan status: {filter_status}')
        else:
            print('Tidak ada tugas apapun dalam daftar.')

# Main function to be used as the entry point
def main():
    parser = argparse.ArgumentParser(description="Task CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add subcommand
    parser_add = subparsers.add_parser("add", help="Add a new task.")
    parser_add.add_argument("title", type=str, help="Title of the new task.")

    # Update subcommand
    parser_update = subparsers.add_parser("update", help="Update an existing task.")
    parser_update.add_argument("tugas_id", type=int, help="ID of the task to update.")
    parser_update.add_argument("title", type=str, help="New title for the task.")

    # Delete subcommand
    parser_delete = subparsers.add_parser("delete", help="Delete a task.")
    parser_delete.add_argument("tugas_id", type=int, help="ID of the task to delete.")

    # Status subcommand (to change a task's status)
    parser_status = subparsers.add_parser("status", help="Change the status of a task.")
    parser_status.add_argument("status", choices=["todo", "in-progress", "done"], 
                                help="New status for the task (todo, in-progress, or done).")
    parser_status.add_argument("tugas_id", type=int, help="ID of the task to update status for.")

    # List subcommand (can filter by status)
    parser_list = subparsers.add_parser("list", help='List tasks. Can filter by status.')
    parser_list.add_argument("status", nargs="?", default=None, 
                             choices=["todo","in progress","done"], # User-facing choices
                             help="Optional: Filter tasks by status (e.g., 'todo', 'in progress', 'done').")

    args = parser.parse_args() 

    if args.command == "add":
        add_tugas(args.title)
    elif args.command == "update":
        update_tugas(args.tugas_id, args.title)
    elif args.command == "delete":
        delete_tugas(args.tugas_id)
    elif args.command == "status":
        status_tugas(args.status, args.tugas_id) 
    elif args.command == "list":
        list_tugas(args.status) 
    elif args.command is None: 
        parser.print_help()

if __name__ == "__main__":
    main()