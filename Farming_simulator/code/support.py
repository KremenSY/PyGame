import os
import pygame

def import_folder(path):
    surface_list=[]

    for folder_name, sub_folder, img_files in os.walk(path):
        # print(img_files)
        for image in img_files:
            # print (image)
            full_path=os.path.join(path, image)
            # print (full_path)
            image_surf=pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def import_folder_dict(path):
    surface_dict = {}
    for folder_name, sub_folder, img_files in os.walk(path):
        for image in img_files:
            full_path=os.path.join(path, image)
            image_surf=pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf
    return surface_dict