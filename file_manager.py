import os


payments_dir = os.path.join(os.path.dirname(__file__), 'payments')

def create_files(name):

    if not os.path.exists(payments_dir):
        os.makedirs(payments_dir)
    
    filenames = name.split(',')
    
    for filename in filenames:
        filename = filename.strip()
        if filename:
            file_path = os.path.join(payments_dir, f"{filename}.txt")
            with open(file_path, "w") as file:
                file.write("0")


def update_to_one(name):
    filenames = name.split(',')
    
    for filename in filenames:
        filename = filename.strip()
        if filename:
            file_path = os.path.join(payments_dir, f"{filename}.txt")
            with open(file_path, "w") as file:
                file.write("1")

def update_to_zero(name):
    filenames = name.split(',')
    
    for filename in filenames:
        filename = filename.strip()
        if filename:
            file_path = os.path.join(payments_dir, f"{filename}.txt")
            with open(file_path, "w") as file:
                file.write("0")

def delete_files(name):
    filenames = name.split(',')
    
    for filename in filenames:
        filename = filename.strip()
        if filename:
            file_path = os.path.join(payments_dir, f"{filename}.txt")
            if os.path.exists(file_path):
                os.remove(file_path)

def manage_files(current_names, new_names):
    
    files_to_delete = set(current_names) - set(new_names)
    files_to_create = set(new_names) - set(current_names)

    for filename in files_to_delete:
        filename = filename.strip()
        if filename:
            file_path = os.path.join(payments_dir, f"{filename}.txt")
            if os.path.exists(file_path):
                os.remove(file_path)

    for filename in files_to_create:
        filename = filename.strip()
        if filename:
            file_path = os.path.join(payments_dir, f"{filename}.txt")
            with open(file_path, "w") as file:
                file.write("0")