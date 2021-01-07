import logging

log_filename = f'logs/{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log'
os.makedirs(os.path.dirname('/logs'), exist_ok=True)
logging.basicConfig(filename=f'{dynamic_path}\logs\{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# logger = logging.getLogger()

# In your main program or programs, do e.g.:

# def main():
#     "your program code"
# 
# if __name__ == '__main__':
#     import logging.config
#     logging.config.fileConfig('/path/to/logging.conf')
#     main()
# or
# 
# def main():
#     import logging.config
#     logging.config.fileConfig('/path/to/logging.conf')
#     # your program code
# 
# if __name__ == '__main__':
#     main()