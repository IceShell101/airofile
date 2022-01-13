import os
import sys
import shutil
import webbrowser
import json

libs_list = ["flask"]
settings = json.load(open("settings.json" , "r"))["settings"]
serving_type = settings["serving_type"]
#background_color =  settings["background_color"]
PATH = None
MODE = "user"
PORT = "5001"
user_input = sys.argv
options_list = ["-p" , "-m"]
for i in range(0,int(len(user_input))):
    if user_input[i] in options_list[0]:
        PATH = user_input[i+1]
    if user_input[i] in options_list[1]:
        MODE = user_input[i+1]

try:
    import multiprocess
    from flask import Flask , render_template , send_file , request , redirect
    def file_type(string):
        dt = {
            "txt" : ['.txt' , '.py' , '.cpp' , '.c++'] ,
            "img" : ['.jpg' , '.png' , '.gif' , '.webp'],
            "video" : ['.webm' ,'.mp4',".mov"],
            }

        a = (string.lower()).split(".")
        b = '.'+ a[-1]
        c = []
        for i in list(dt):
            if b in dt[i]:
                return i
            else:
                c.append(False)
        if int(len(c)) == 3:
            return None
    def w_is_url(string):
        text = string.split()
        b = [i for i in text if "://" in i and int(len(i.split("."))) == 2 or int(len(i.split("."))) >= 2]
        result = []
        for i in text:
            if i in b:
                result.append(f'<a href="{i}" style="color:blue;" target="blank">{i}</a>')
            else:
                result.append(i)

        return "\n".join(result)
    folder_path =  PATH


    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = "uploads"

    @app.route("/" , methods=['GET' , 'POST'])
    def home():
        files = os.listdir(folder_path)
        files_data = []
        for i in files:
            files_data.append({'name':f'{i}' , 'path':f'/{i}' ,  'type':f'{file_type(i)}'})


        if request.method == 'POST':
            if request.form.get("request") == "redierct_request":
                a = request.form.get("url")
                #if a == "000$#0uousef":
                    #MODE = "admin"
                    #print(f"-----------------------------------------mode{MODE}")
                    #return redirect("/")
                #else:
                return redirect(a)
            if request.form.get("request") == "create_folder_request" and MODE == "admin":
                file_d_path = request.form.get("path").strip("/")
                dirname = request.form.get("dirname")
                os.mkdir(f"/{file_d_path}/{dirname}")
                
            if request.form.get("request") == "delete_request" and MODE == "admin":
                file_d_path = request.form.get("file_path").lstrip("/")
                file_copy = file_d_path.split("/")
                shutil.copyfile(f"/{file_d_path}", f"Trash/{file_copy[-1]}")
                os.remove(f"/{file_d_path}")
                return redirect(request.form.get("path"))
            if request.form.get("request") == "folder_delete_request" and MODE == "admin":
                file_d_path = request.form.get("file_path").lstrip("/")
                file_copy = file_d_path.split("/")
                #os.mkdir(f"Trash/{file_copy[-1]}")
                #for i in os.listdir(f"/{file_d_path}"):
                    #shutil.copyfile(f"/{file_d_path}/{i}", f"Trash/{file_copy[-1]}/{i}")
                os.rmdir(f"/{file_d_path}")
                return redirect(request.form.get("path"))
            elif request.form.get("request") == "upload_request" and MODE == "admin":
                def upload_m():
                    a = request.files['file']
                    b= request.form.get("path").strip("/")
                    if int(len(b)) != 0 and int(len(a.filename)) != 0:
                        a.save(f"/{b}/{a.filename}")
                    elif int(len(b)) == 0 and int(len(a.filename)) > 0:
                        a.save(f"/{a.filename}")
                        print(f"-----------------------bb = {b}")
                up_m = multiprocess.Process(target=upload_m)
                up_m.start()
                return redirect(request.form.get("path"))
            elif request.form.get("request") == "openurl_request" and MODE == "admin":
                print("-----------------------------------------")
                a = request.form.get("url_text")
                webbrowser.open(a)
            elif request.form.get("request") == "shell_request" and MODE == "admin":
                a = request.form.get("shell_command")
                os.system(a)
            else:
                return redirect(request.form.get("path"))
        return render_template("index.html" , files_data=files_data , back_button_path="/" , current_path=request.path , usermode=MODE)

    @app.errorhandler(404)
    def error404(e):
            myurl = request.path
            try:
                try:
                    file_c = os.listdir(f"{folder_path}/{myurl}")
                    files_data = []
                    back_button_path = "/".join(myurl.split('/')[:-1])
                    if back_button_path == "":
                        back_button_path = "/"

                    for i in file_c:
                        files_data.append({'name':f'{i}' , 'path':f'{myurl}/{i}' ,  'type':f'{file_type(i)}'})
                    return render_template("index.html" , files_data=files_data , back_button_path=back_button_path , current_path=request.path , usermode=MODE)
                except:
                    if file_type(f"{folder_path}/{myurl}") == 'txt':
                        return send_file(f"{folder_path}/{myurl}")
                    else:
                        return send_file(f"{folder_path}/{myurl}")
            except:
                return render_template("error404.html" , myurl=myurl )  , 404
    @app.errorhandler(500)
    def error500(e):
        return "SERVER ERROR"
    if serving_type== "2":
        app.run(port=PORT , debug=True , host='0.0.0.0')
    else:
        app.run(port=PORT , debug=True)

except ModuleNotFoundError:
    for i in libs_list:
        os.system(f"pip3 install '{i}'")
 
