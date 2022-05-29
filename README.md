# flask-server
## Description about the files
1. .gitignore - file created to ignore subdirectories of pycache and venv while creating the git repository.
2. Procfile - declaring what commands are run by application’s dynos on the Heroku platform, here gunicorn web server is used along with websocket support provided by gevent websocket.
3. app.py - Main python file
4. export.pkl - Model used to predict facial expression (downloaded as pickle file)
5. requirements.txt - packages along with versions required to run the file
6. shape_predictor_68_face_landmarks.dat - dlib's pre trained model, will be used here to identify the locations of important facial landmarks such as the corners of the eyes
## Installation
1. Please ensure you have Python installed in your system and pip as well.
2. We will run our files in a virtual environment. It is used to manage Python packages for different projects. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects.
3. Clone the repository or download it as a zip file. When you extract your downloaded zip files, you will get a folder flask-server-main. Open your command prompt in this directory. For example, you download it on desktop. Then your command prompt should be pointing at someRootPath\Desktop\flask-server-main>
4. Write this in the terminal to install virtual envrionment.</br> 
```bash
pip install virtualenv
```
5. To create virtualenv for this project, write the following command. Here, venv represents the folder for the virtual environment. 
```bash
virtualenv venv
```
6. To activate this virtualenv, write the following command (On Windows).
```bash
venv\Scripts\activate
```
7. Now, we can install all the required libraries in this virtualenv using requirements.txt
```bash
pip install -r requirements.txt
```

##### It will take some time to install all the requirements as it requires libraries like dlib, pytorch
8. After this, we just need to run the app.py file to start our flask server. For this write,
```bash
python app.py
```
