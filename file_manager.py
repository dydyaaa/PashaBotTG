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

