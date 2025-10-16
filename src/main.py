
from blockfunctions import *
import os
import shutil
from generate_page import generate_page, generate_pages_recursive
import sys

# copy the files from the static folder to public folder
def copy_static(source, destination):
    # check if path exist
    if not os.path.exists(source):
        raise Exception("Invalid source path")
    if os.path.exists(destination):
        shutil.rmtree(destination) # delete the current destination folder
    if not os.path.exists(destination): # if the folder does not exist, create new one
        os.mkdir(destination) # pass the path of destination to create a new one

    source_items = os.listdir(source) # list all items in source folder
    for item in source_items:
        source_item_path = os.path.join(source, item) # build address/path of the item in source folder
        dest_item_path = os.path.join(destination,item) # build path of item in destination folder

        # if it is a file, copy full path to destination folder.
        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, dest_item_path) 
        else:
            # it is a directory
            # make recursive call to check the directory
            copy_static(source_item_path, dest_item_path)



def main():
    
    if len(sys.argv) < 2:
        basepath = "/" # if no passed argument, default value is "/"
    else: 
        basepath = sys.argv[1]  # else passed argument is value of basepath
    
    destination = "docs" # destination directory where pages will be generated 
    source = "static" #where fonts, images, etc. stuffs that need to always be there to stay
    
    template_path = "template.html" #html template for the page
    content_path = "content/" # the folder that contains the contents of pages. 
    destination_path = "docs/"   # path where pages are generated lives

    # copy files/directories from source to dest
    copy_static(source, destination)
    
    generate_pages_recursive(content_path , template_path , destination_path, basepath)

if __name__ == "__main__":
    main()