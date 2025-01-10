class Config:
    def __init__(self):
        self.excluded_folders = set()
        self.show_file_contents = False  # New property

    def add_excluded_folder(self, folder):
        self.excluded_folders.add(folder)

    def remove_excluded_folder(self, folder):
        self.excluded_folders.discard(folder)

    def is_excluded(self, folder):
        return folder in self.excluded_folders

    def set_show_file_contents(self, show):
        self.show_file_contents = show
