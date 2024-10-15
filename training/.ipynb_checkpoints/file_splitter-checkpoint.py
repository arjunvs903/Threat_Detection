import os
import random
import shutil

def get_file_names(directory):
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".jpg"):
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                file_names.append(file_name)
    return file_names

def copyfiles(files, source_path, directory):
    image_dir = os.path.join(directory, "images")
    label_dir = os.path.join(directory, "labels")
    os.mkdir(image_dir)
    os.mkdir(label_dir)
    for filename in files:
         shutil.copy2(os.path.join(source_path, filename), os.path.join(image_dir, os.path.basename(filename)))
         shutil.copy2(os.path.join(source_path, filename.replace("jpg", "txt")), os.path.join(label_dir, os.path.basename(filename.replace("jpg", "txt"))))



source_path = r"/mnt/d/projects/MainProject/Weapon Detection/training/source/datalabel"  # Replace with the actual directory path
labels = []
imgs = []
file_names = get_file_names(source_path)
# print(file_names)
# print(file_names)
random.seed(36)
random.shuffle(file_names)
file_len = len(file_names)
train_len = int(0.7*file_len)
test_len = int(0.1*file_len)

train_files = file_names[0:train_len]
test_files = file_names[train_len:train_len+test_len]
val_files = file_names[train_len+test_len:]

destination_path = 'dataset'
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

train_directory = os.path.join(destination_path, 'train')
test_directory = os.path.join(destination_path, 'test')
val_directory = os.path.join(destination_path, 'val')
os.mkdir(train_directory)
os.mkdir(test_directory)
os.mkdir(val_directory)

#Training Set
copyfiles(train_files, source_path, train_directory)

#Testing Set
copyfiles(test_files, source_path, test_directory)

#Validation Set
copyfiles(val_files, source_path, val_directory)
