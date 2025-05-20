import os
import shutil

def copy_static(source, destination):
    # First check if destination exists, if so delete it
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    # Create the destination directory
    os.mkdir(destination)
    
    # Now implement the recursive copying logic
    copy_recurse(source, destination)

def copy_recurse(source, destination):
    files = os.listdir(source)
    print(files)
    for file in files:
        if os.path.isfile(os.path.join(source,file)) == True:
            print(f"Copying: {os.path.join(source,file)}")
            shutil.copy(os.path.join(source,file), os.path.join(destination,file))
        else:
            print(f"Recusing into {os.path.join(source,file)}")
            os.mkdir(os.path.join(destination,file))
            copy_recurse(os.path.join(source,file), os.path.join(destination,file))