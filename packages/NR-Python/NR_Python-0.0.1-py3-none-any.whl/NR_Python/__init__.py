import time

def Sleep(Seconds: float):
    time.sleep(Seconds)

class File():
    def __init__(self, FileLocation: str):
        self.FileLocation = FileLocation

    def ReadAll(self):
        try:
            with open(self.FileLocation, 'r') as FileRead:
                return FileRead.read()
            
        except:
            print("Error no file found")
    
    def ReadLine(self, Line: int):
        try:
            with open(self.FileLocation, 'r') as FileRead:
                Lines = FileRead.readlines()
                return (Lines[Line - 1].strip())
            
        except:
            print("Error no file found")

    def Write(self, WriteWhat: str):
        try:
            with open(self.FileLocation, 'w') as FileRead:
                FileRead.write(WriteWhat)
                
                
            
        except:
            print("Error no file found")

    
    def WriteLine(self, Line: int, WriteWhat: str):
        try:
            with open(self.FileLocation, 'r') as file:
                lines = file.readlines()


            lines[Line-1] = f"{WriteWhat}\n"


            with open(self.FileLocation, 'w') as file:
                file.writelines(lines)
                
                
            
        except:
            print("Error no file found")
            