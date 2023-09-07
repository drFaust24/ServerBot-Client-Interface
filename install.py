import os

print("Select installation directory:")
local_file = input("")
log_folder = "log.txt"
log_path = os.path.join(local_file, log_folder)

with open('bot-control.ui', 'r', encoding='utf-8') as f:
    old_data = f.read()
new_path = log_path.replace(os.sep, '/')
print(new_path)
new_data = old_data.replace('file:///C:/Users/user/Desktop/BtCtl/log.txt', 'file:///'+new_path)

with open('bot-control.ui', 'w', encoding='utf-8') as f:
    f.write(new_data)

f.close()