from datetime import datetime

class Logger:
    def __init__(self, log_file:str):
        self.log_file = log_file
        # try to open file in append mode (a); if file doesn't exist
        # the (+) mode will get the syscall to create the file. 
        self.file = open(log_file, "a+")

    def __del__(self):
        print(f"Logger: Closing file {self.log_file}")
        self.file.close()

    def log(self, line: str):
        self.file.write(f"[{datetime.now().strftime('%c')}] {line}\n")
        self.file.flush()
    
def create_logger(log_file:str) -> Logger:
    return Logger(log_file)