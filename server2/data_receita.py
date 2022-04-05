class File_edit():
    def __init__(self, path=None):
        pass

    def write(self, path,file, mode, txt):
        if mode == 'w':
            with open(path, 'w') as file:
                file.write(txt)
        print("write()", txt)

    def read(self, path):
        pass

