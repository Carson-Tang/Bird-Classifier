import os


PATH = os.getcwd() + "/train"
MAX_DIR_SZ = 500
for bird_name in os.listdir(PATH):
    dir_PATH = PATH + "/" + bird_name
    remove = len(os.listdir(dir_PATH))
    if remove < MAX_DIR_SZ:
        continue
    else:
        remove = remove - MAX_DIR_SZ
    for f in os.listdir(dir_PATH[:remove]:
        os.remove(dir_PATH "/" + f)
