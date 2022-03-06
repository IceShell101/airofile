import os, sys, shutil, webbrowser
from flask import Flask , render_template , send_file , request , redirect
print("make sure to install flask library!\nand all of it's files exists")
HOST  = "127.0.0.1" 
PATH = ""
MODE = "user"
PORT = "5005"
user_input = sys.argv
options_list = ["-p" , "-m" , "-h"]
for i in range(0,int(len(user_input))):
    if user_input[i] in options_list[0]:PATH = user_input[i+1]
    if user_input[i] in options_list[1]:MODE = user_input[i+1]
    if user_input[i] in options_list[2]:HOST = user_input[i+1]
def file_type(string):
    dt = {
        "txt" : ['.txt' , '.py' , '.cpp' , '.c++'] ,
        "img" : ['.jpg', 'jpeg' , '.png' , '.gif' , '.webp'],
        "video" : ['.webm' ,'.mp4',".mov"],
        }
    b = '.'+ (string.lower()).split(".")[-1]
    for i in list(dt):
        if b in dt[i]:return i
    return None
app = Flask(__name__)
@app.before_request
def main():
        myurl = request.path
        #services of the app
        if request.method == 'POST':
            if request.form.get("request") == "redierct_request":return redirect(request.form.get("url"))
            if request.form.get("request") == "create_folder_request" and MODE == "admin":
             file_d_path = request.form.get("path").strip("/")
             dirname = request.form.get("dirname")
             os.mkdir(os.path.join(PATH ,file_d_path , dirname))
            if request.form.get("request") == "delete_request" and MODE == "admin":
                if os.path.exists("Trash") != True:os.mkdir("Trash")
                file_d_path = (request.form.get("file_path")).lstrip("/")
                file_copy = file_d_path.split("/")
                if os.path.isfile(os.path.join(PATH , file_d_path)):
                    shutil.copyfile(os.path.join(PATH , file_d_path) , os.path.join("Trash",file_copy[-1]))
                    os.remove(os.path.join(PATH , file_d_path))
                else:os.rmdir(os.path.join(PATH , file_d_path))            
            if request.form.get("request") == "upload_request" and MODE == "admin":
                    def upload_m():
                        all_ = request.files.getlist("file[]")
                        b = (request.form.get("path")).strip("/")
                        for a in all_:
                            if os.path.exists(os.path.join(PATH , b , a.filename)):
                                count_c = 1
                                if os.path.exists(os.path.join(PATH,b,f"({count_c})"+a.filename)):
                                    while os.path.exists(os.path.join(PATH,b,f"({count_c})"+a.filename)):count_c +=1
                                    a.save(os.path.join(PATH,b,f"({count_c})"+a.filename))
                                else: a.save(os.path.join(PATH,b,f"({count_c})"+a.filename))
                            else:a.save(os.path.join(PATH , b , a.filename))
                    upload_m()
            return redirect(request.form.get("path"))
        try:
            try:
                file_c = sorted(os.listdir(os.path.join(PATH,*(myurl.split('/'))))) if os.path.join(PATH,*(myurl.split('/'))) !="" else sorted(os.listdir(None))
                file_path =  '/' if myurl.rstrip('/') != '' else ''
                files_data = [ {'name':f'{i}' , 'path': myurl.rstrip("/")+file_path +i ,'type':f'{file_type(i)}'}  for i in file_c]
                files_folders_count = {'files':[] , 'folders':[]}
                for i in files_data:
                    if os.path.isfile(os.path.join(PATH ,i['path'].strip('/'))):
                        files_folders_count['files'].append(i)
                    else:
                        files_folders_count['folders'].append(i)
                files_folders_count['files'] = len(files_folders_count['files'])
                files_folders_count['folders'] = len(files_folders_count['folders'])
                back_button_path = "/".join(myurl.split('/')[:-1])
                if back_button_path == "":
                    back_button_path = "/"
                print(f"visitor:{request.remote_addr}")
                return render_template("index.html" , files_data=files_data , 
                                       back_button_path=back_button_path , current_path=request.path , 
                                       usermode=MODE , files_num=files_folders_count )
            except NotADirectoryError:
                
                return send_file(os.path.join(PATH , *(myurl.split('/'))))
        except FileNotFoundError:return render_template("error.html" , error_type="error 404" , error_explaination=f"""this happens becaues the requested url "{myurl}" does not exist or not accessable""")  , 404
@app.errorhandler(500)
def error500(e):return render_template("error.html" , error_type="error 500" , error_explaination="it happens when a server error occurs like a code error or may be the opration cant be done") , 500
app.run(port=PORT , host=HOST)
