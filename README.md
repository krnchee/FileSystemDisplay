# FileSystemDisplay

Run ./start_app.sh to start app

APIs

To retrieve file system info:

GET request on localhost:5000/get_file_info with the following parameters:

path

GET API: get_file_info

Example: 

http://localhost:5000/get_file_info?path=/Users/


To post/delete files/dir to a path with the following parameters:

path, file, dir (file/dir optional. If you post both file and dir, file will be added under newly created dir)

POST API: add_to_path
DELETE API: delete_from_path


Example:

http://localhost:5000/add_to_path?path=/Users/&file=test_file&dir=test

http://localhost:5000/delete_from_path?path=/Users/&dir=test

