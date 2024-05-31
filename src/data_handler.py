from os.path import exists, isfile
import tkinter as tk
from tkinter import filedialog

# Directory Handler
class DirectoryHandler:
    """
    This class takes and stores directories for later use. This
    class was implemented as a Singleton design pattern.
    """

    def __new__(cls):
        """
        If class has not yet been instantiated, create a new one.
        Otherwise, use original instance.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(DirectoryHandler, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        """
        Initialize the paths as a dictionary
        """
        self.paths = dict()

    def add_path(self, data_name: str, path: str):
        """
        Adds a path to the dictionary of paths
        """

        # Assert file or directory exists
        err_msg = f"{path} is neither a valid directory nor a valid file"
        assert exists(path) or isfile(path), err_msg

        self.paths[data_name] = path

def create_guiless_tk():
    # create a tkinter object
    root = tk.Tk()
    # remove the gui element of the tkinter object
    root.withdraw()
    # return the tk object
    return root

def request_open_file(note) -> str:
    # create gui-less tkinter object
    root = create_guiless_tk()

    # record the path
    file_dir = filedialog.askopenfilename(
        filetypes = [("All Files", "*.*")],
        title = note
    )

    root.destroy()
    return file_dir

def request_write_file(note) -> str:
   # create gui-less tkinter object
    root = create_guiless_tk()

    # record the  path
    file_dir = filedialog.asksaveasfilename(
        filetypes = [("All Files", "*.*")],
        title = note
    )

    root.destroy()
    return file_dir