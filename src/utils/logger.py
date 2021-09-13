class Logger:
    def __init__(self, max_logs=3, max_errors=1):
        self.logs = []
        self.max_logs = max_logs
        self.errors = []
        self.max_errors = max_errors

    def log(self, line):
        self.logs.append(line)
        if len(self.logs) > self.max_logs:
            self.write_logs()
            self.logs = []
        return self

    def error(self, err):
        try:
            self.errors.append(err)
            if len(self.errors) > self.max_errors:
                self.write_errors()
                self.errors = []
        except Exception as fuck:
            print('Caught an error while trying to log an error...')
            print(fuck)

    def write_logs(self, file_path='logs.txt'):
        with open(file_path, 'a') as logs:
            logs.writelines(self.logs)

    def write_errors(self):
        with open('error_logs.txt', 'a') as logs:
            logs.writelines(self.errors)
