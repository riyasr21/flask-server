# flask-server
## Description about the files
1. .gitignore - file created to ignore subdirectories of pycache and venv while creating the git repository.
2. Procfile - declaring what commands are run by application’s dynos on the Heroku platform, here gunicorn web server is used along with websocket support provided by gevent websocket.
3. app.py - Main python file
4. export.pkl - Model used to predict facial expression (downloaded as pickle file)
5. requirements.txt - packages along with versions required to run the file
6. shape_predictor_68_face_landmarks.dat - dlib's pre trained model, will be used here to identify the locations of important facial landmarks such as the corners of the eyes
