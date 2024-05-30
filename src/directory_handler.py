from os.path import exists, isfile

# Retriever Object
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
        self.paths = dict

    def add_path(self, data_name: str, path: str):
        """
        Adds a path to the dictionary of paths
        """

        # Assert file or directory exists
        err_msg = f"{path} is neither a valid directory nor a valid file"
        assert exists(path) or isfile(path), err_msg

        self.paths[data_name] = path
        
    file_path = ""
    def full_path(self, folder_path:str, file_name:str):
        self.file_path = os.path.join(folder_path,file_name)
        return  self.file_path