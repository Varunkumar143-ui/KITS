from flask import Flask, request, render_template,send_from_directory,jsonify
import re
import sqlite3
import os
from flask_ngrok import run_with_ngrok
import google as go
import test
m = 0

import nibabel as nib
import matplotlib.pyplot as plt
app = Flask(__name__) 
run_with_ngrok(app)
def get_nifti_files(directory):
    nifti_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.nii.gz'):
            nifti_files.append(file_name)
    return nifti_files
def nifti_to_png_slices(nifti_file_path, output_folder):
    # Load the NIfTI image
    img = nib.load(nifti_file_path)

    # Get the image data as a NumPy array
    data = img.get_fdata()

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over the slices along the z-axis
    for slice_index in range(data.shape[0]):
        # Extract the slice data
        slice_data = data[slice_index, :, :]

        # Plot the slice using matplotlib
        plt.imshow(slice_data, cmap='gray')

        # Remove axis labels and ticks
        plt.axis('off')

        # Save the plot as a PNG image
        output_file_path = os.path.join(output_folder, f'slice_{slice_index}.png')
        plt.savefig(output_file_path, bbox_inches='tight', pad_inches=0)

        # Clear the plot
        plt.clf()

# Usage example



def empty_folder(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.rmdir(dir_path)

# Example usage


@app.route("/")
def Home():
    return render_template("index.html")
@app.route("/index.html")
def Home2():
    return render_template("index.html")
@app.route("/register.html")
def Home1():
    return render_template("register.html")
@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
       
        password = request.form['pass']
        email = request.form['email']
        print(password,email)
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return render_template('register.html', error='Invalid email format')
        sql = sqlite3.connect("user.db")
        cur.execute(f"create table user(email)")
        cur.execute(f"select * from user where email=\'{email}\';")
        try:
            a = cur.fetchall()[0]
            if(a[0] == email and a[1] == password):
                return render_template("main.html")
            else:
                return render_template('register.html', error='Invalid email or password')
        except:
            return render_template('register.html', error='Invalid email or password')
    return render_template("main.html")


@app.route("/reg",methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        
        repass = request.form['repass']
        password = request.form['pass']
        email = request.form['email']
        print(repass,password,email)
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) or (password != repass):
            return render_template('register.html', error='Invalid email format or password mismatch')
        sql = sqlite3.connect("user.db")
        cur = sql.cursor()
        cur.execute("create table user(email varchar(20),password varchar(20))")
        cur.execute(f'''insert into user values(\'{email}\',\'{password}\')''')
        sql.commit()
    return render_template("main.html")
@app.route('/image_1-removebg-preview.png')
def get_image():
    return send_from_directory('static', "image_1-removebg-preview.png")
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file selected'

    file = request.files['file']

    if file.filename == '':
        return 'No file selected'

    # Save the file to a desired location
    empty_folder('templates/uploads/input/')
    empty_folder('templates/uploads/output/')
    
    file.save("app\\templates\\uploads\input\\" + file.filename[:-7]+"_0000.nii.gz")
    #file.save('templates/uploads/input/' + file.filename[:-7]+"_0000.nii.gz")
    
    test.upload_image("app\\templates\\uploads\input\\",file.filename[:-7]+"_0000.nii.gz")
    #command = "nnUNet_predict -i  uploads/input/ -o uploads/output/ -t Task135_KiTS2021  -m 3d_lowres --save_npz -f 0"
    #result = subprocess.run(command, shell=True, capture_output=False, text=False)
    
    #send_from_directory('uploads', "ouput/slice_0.png")
    return render_template("Model.html")


@app.route('/process', methods=['POST'])
def process():
    print("post")
    directory_path = 'app\\templates\\uploads\output'
    print("post")
    nifti_files = get_nifti_files(directory_path)
    print("post")
    return send_from_directory('templates', "uploads/output/"+nifti_files[0])
if __name__=='__main__':
    app.run()
