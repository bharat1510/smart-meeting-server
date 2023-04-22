
# Smart Meetings Server Side

This is the Django backend application of the project.

The root structure of the app - 
-   Smartmeeting
    -   smartmeeting (root directory of the project)
    -   meeting (model/app of the project)
    -   model   (contains model and label file)
    -   requiremnt.txt  (libraries and dependencies)


## How to run the application

-   Create a virtual env 
```base 
python -m venv smart-env
```
- activate it
```base
source smart-env/bin/activate
```
- Run the migrations command
```base
python manage.py makemigrations
python manage.py migrate
```

- Run the application
```base
python manage.py runserver
```

## APIs
- Upload Audio API
```base
http://127.0.0.1:8000/upload
```

- Get Generated Summary API
```base
http://127.0.0.1:8000/sendSummary
```# smart-meeting-server
