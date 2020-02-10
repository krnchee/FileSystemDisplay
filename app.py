from flask import Flask, request, jsonify
import os, stat
import pwd


app = Flask(__name__)

@app.route("/get_file_info", methods = ['GET'])
def get_file_info():
    path = request.args.get('path')

    files = set_root_dir(path)
    if type(files) == str:
        return files
    return jsonify({'files': files})

@app.route('/add_to_path', methods = ['Post'])
def add_to_path():

    file = request.args.get('file')
    dir = request.args.get('dir')
    path = request.args.get('path')
    if dir:
        dir_path = path + '/' + dir
        if file:
            file_path = dir_path + '/' + file
    if file and not dir:
        file_path = path + '/' + file

    if file:
        if os.path.exists(file_path):
            return "This file already exists."
    if dir:
        if os.path.exists(dir_path):
            return "This dirictory already exists."

    if not os.path.isdir(path):
        return "This is not a valid directory. Please try again."

    if dir:
        os.chdir(path)
        access_rights = 0o755

        try:
            os.mkdir(dir, access_rights)
        except OSError:
            return ("Creation of the directory %s failed" % dir)
        else:
            print ("Successfully created the directory %s" % dir)
            dir_exists = os.path.exists(dir_path)
            if dir_exists and not file:
                return "{} directory successfully added to {}".format(dir, path)
            path = dir_path

    if file:
        os.chdir(path)
        try:
            f= open(file,"w+")
        except OSError:
            return ("Creation of the file %s failed" % file)
        else:
            print ("Successfully created the file %s" % file)
            file_exists = os.path.exists(file_path)
            if file_exists and not dir:
                return "{} file successfully added to {}".format(file, path)

    if file_exists and dir_exists:
        return "{} directory successfully created and {} file successfully added to {}".format(dir, file, path)

@app.route('/delete_from_path', methods = ['Delete'])
def delete_from_path():

    file = request.args.get('file')
    dir = request.args.get('dir')
    path = request.args.get('path')

    if dir:
        dir_path = path + '/' + dir
        if file:
            file_path = dir_path + '/' + file
    if file and not dir:
        file_path = path + '/' + file

    if dir:
        if not os.path.exists(dir_path):
            return "This directory does not exist. Therefore nothing has been deleted."

    if file:
        if not os.path.exists(file_path):
            return "This file does not exist in this path. Therefore nothing has been deleted."

    if not os.path.isdir(path):
        return "This is not a valid path to file/directory. Please try again."

    if dir:
        try:
            os.rmdir(dir_path)
        except OSError:
            return ("Deletion of the %s directory failed" % dir)
        else:
            print ("Successfully deleted the directory %s" % dir)
            dir_exists = os.path.exists(dir_path)

    if file and not dir:
        os.chdir(path)
        try:
            os.remove(file_path)
        except OSError:
            return ("Deletion of the file %s failed" % file)
        else:
            print ("Successfully deleted the file %s" % file)
            file_exists = os.path.exists(file_path)

    if dir:
        if not dir_exists:
            return "{} directory and all subfiles successfully deleted from {}".format(dir, path)
        else:
            return "{} directory has not been deleted from {}. Please try again".format(dir, path)

    if file and not dir:
        if not file_exists:
            return "{} file successfully deleted from {}".format(file, path)
        else:
            return "{} file has not been deleted from {}. Please try again".format(file, path)

def set_root_dir(root_dir) :
    if not os.path.isdir(root_dir):
        return "This is not a valid directory. Please try again."

    list_arr = os.listdir(root_dir)
    file_list = []

    for file in list_arr:
        file_dict = {}
        file_path = root_dir + '/' + file
        file_stat = (os.stat(file_path))
        file_permission = (oct(stat.S_IMODE(file_stat.st_mode)))
        file_size = file_stat.st_size
        file_owner = pwd.getpwuid(file_stat.st_uid).pw_name

        if os.path.isdir(file_path):
            file += '/'

        file_dict['name'] = file
        file_dict['owner'] = file_owner
        file_dict['size'] = file_size
        file_dict['permissions'] = file_permission

        file_list.append(file_dict)

    return file_list

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
