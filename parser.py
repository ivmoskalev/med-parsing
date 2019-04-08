import subprocess
import os
import os.path as path


# data_path = '/home/igor/Development/med-parsing/Data/'

# for rootpath, dirs, files in os.walk(data_path):
#     os.chdir(rootpath)
#     for filename in files:
#         if filename.endswith('.doc'):
#             file_path = path.normpath(path.join(rootpath, filename))
#             subprocess.call(['soffice', '--headless', '--convert-to', 'docx', file_path])
#             os.remove(file_path)
data_path = '/home/igor/Development/med-parsing/Data/2013 год/'
os.chdir(data_path)
for filename in os.listdir(os.getcwd()):
    old_file_path = path.normpath(path.join(data_path, filename))
    new_file_path = path.normpath(path.join(data_path, f'13№{filename}'))
    os.rename(old_file_path, new_file_path)
    # subprocess.call(['soffice', '--headless', '--convert-to', 'docx', file_path])
    # os.remove(file_path)