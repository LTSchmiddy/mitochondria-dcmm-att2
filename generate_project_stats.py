import os
import json

line_count = 0
def scan_directory(current_dir="./"):
    global line_count
    dir_cont = os.listdir(current_dir)

    ignore_fullpath = [
        './.git',
        './.idea',
        './build',
        './dist',
        './mdcmm',
        './node_modules',
        './static/bower_components',
        './venv',
        './src/webview',
        './static/libs'
    ]

    ignore_recursive = [
        '__pycache__'
    ]

    ignore_extensions = [
        '.css',
        '.css.map',
        '.pyc',
        '.pyd'
    ]

    dir_dict = {
        'path': current_dir,
        'dirs': {},
        'files': {}

    }

    for i in dir_cont:
        if i in ignore_recursive:
            continue

        bad_ending = False
        for j in ignore_extensions:
            if i.endswith(j):
                bad_ending = True
        if bad_ending:
            continue

        fullpath = os.path.join(current_dir, i).replace("\\", "/")

        if fullpath in ignore_fullpath:
            continue

        if os.path.isfile(fullpath):
            dir_dict['files'][i] = fullpath
            print(fullpath)

            line_arr = open(fullpath, 'r').read().split("\n")

            for k in line_arr:
                check = k.strip()
                if check == "":
                    continue
                line_count += 1


        elif os.path.isdir(fullpath):
            dir_dict['dirs'][i] = scan_directory(fullpath)

    return dir_dict


out_dict = scan_directory()
json.dump(out_dict, open("dir_tree.json", 'w'), indent=4, sort_keys=True)
print(f"total lines of code: {line_count}")