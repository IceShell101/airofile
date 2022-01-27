import os, sys, shutil, webbrowser, json

SERVING_TYPE  = "1" 
PATH = None
MODE = "user"
PORT = "5001"
user_input = sys.argv
options_list = ["-p" , "-m" , "-s"]
for i in range(0,int(len(user_input))):
    if user_input[i] in options_list[0]:PATH = user_input[i+1]
    if user_input[i] in options_list[1]:MODE = user_input[i+1]
    if user_input[i] in options_list[2]:SERVING_TYPE = user_input[i+1]
from multiprocess import Process
from flask import Flask , render_template , send_file , request , redirect
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
app.config['UPLOAD_FOLDER'] = "uploads"
@app.route("/" , methods=['GET' , 'POST'])
def home():
    files = sorted(os.listdir(PATH))
    files_data = [{'name':f'{i}' , 'path':f'/{i}' ,  'type':f'{file_type(i)}'} for i in files]
    files_folders_count = {'files':[] , 'folders':[]}
    for i in files_data:
        if os.path.isfile(os.path.join(PATH , i['path'].strip('/'))):files_folders_count['files'].append(i)
        else:files_folders_count['folders'].append(i)
    files_folders_count['files'] = len(files_folders_count['files'])
    files_folders_count['folders'] = len(files_folders_count['folders']) 
    if request.method == 'POST':
        if request.form.get("request") == "redierct_request":return redirect(request.form.get("url"))
        if request.form.get("request") == "create_folder_request" and MODE == "admin":
            file_d_path = request.form.get("path").strip("/")
            dirname = request.form.get("dirname")
            os.mkdir(os.path.join(PATH ,file_d_path , dirname))
        if request.form.get("request") == "delete_request" and MODE == "admin":
            if os.path.exists("Trash") != True:
                os.mkdir("Trash")
            file_d_path = (request.form.get("file_path")).lstrip("/")
            file_copy = file_d_path.split("/")
            if os.path.isfile(os.path.join(PATH , file_d_path)):
                shutil.copyfile(os.path.join(PATH , file_d_path) , os.path.join("Trash",file_copy[-1]))
                os.remove(os.path.join(PATH , file_d_path))
            else:os.rmdir(os.path.join(PATH , file_d_path))
            return redirect(request.form.get("path"))
        elif request.form.get("request") == "upload_request" and MODE == "admin":
            def upload_m():
                a = request.files['file']
                b = (request.form.get("path")).strip("/")
                if os.path.exists(os.path.join(PATH , b , a.filename)):
                    count_c = 1
                    if os.path.exists(os.path.join(PATH,b,f"({count_c})"+a.filename)):
                        while os.path.exists(os.path.join(PATH,b,f"({count_c})"+a.filename)):count_c +=1
                        a.save(os.path.join(PATH,b,f"({count_c})"+a.filename))
                    else: a.save(os.path.join(PATH,b,f"({count_c})"+a.filename))
                else:a.save(os.path.join(PATH , b , a.filename))
            up_m = Process(target=upload_m)
            up_m.start()
            return redirect(request.form.get("path"))
        elif request.form.get("request") == "openurl_request" and MODE == "admin":
            webbrowser.open(request.form.get("url_text"))
        elif request.form.get("request") == "shell_request" and MODE == "admin":os.system(request.form.get("shell_command"))
        else:return redirect(request.form.get("path"))
    return render_template("index.html" , files_data=files_data , back_button_path="/" , current_path=request.path , usermode=MODE , files_num=files_folders_count)

@app.errorhandler(404)
def error404(e):
        myurl = request.path
        try:
            try:
                file_c = sorted(os.listdir(os.path.join(PATH,*(myurl.split('/')))))
                files_data = [ {'name':f'{i}' , 'path':f'{myurl}/{i}' ,  'type':f'{file_type(i)}'}  for i in file_c]
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
                return render_template("index.html" , files_data=files_data , back_button_path=back_button_path , current_path=request.path , usermode=MODE , files_num=files_folders_count)
            except:
                if file_type(myurl) == 'txt':return send_file(os.path.join(PATH,myurl))
                else:return send_file(os.path.join(PATH , myurl))
        except:return render_template("error404.html" , myurl=myurl )  , 404

@app.errorhandler(500)
def error500(e):return "error 500 , (SERVER ERROR)"
if SERVING_TYPE == "2":app.run(port=PORT , host='0.0.0.0' , debug=True)
else:app.run(port=PORT)


