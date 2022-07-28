import os

save_py_list = ['main.py','setup.py','修改 pyd 文件名 + 删除 c 文件.py']

path = os.getcwd()
for item in os.listdir(path):
    item_path = os.path.join(path, item)
    if os.path.isdir(item_path):
        print('文件夹：', item)
    elif os.path.isfile(item_path):
        print('文件：', item)
        if item.endswith('.pyd') and len(item.split('.')) > 2:
            temp_item = item.split('.')[0] + '.' + item.split('.')[2]
            os.rename(os.path.join(path, item), os.path.join(path, temp_item))
        if item.endswith('.c'):
            os.remove(os.path.join(path, item))
        # if item.endswith('.py') and item not in save_py_list:
        #     os.remove(os.path.join(path, item))
