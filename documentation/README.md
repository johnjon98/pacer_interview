## Objective 
First interview challenge of pacer




#### To load the project
1. run the following codes :
```
    python manage.py migrate    # perform migration of schema into DB
    python manage.py loaddata   # load admin user data so that user can access the admin portal
    python manage.py runserver  # to run the server in localhost 
```

2. In local, go to '127.0.0.1:8000/admin' to access the admin portal 
- superuser  (1234@superuser.com/ abcd1234)
- admin      (1234@admin.com/ abcd1234)  

3. for task 1, can test the API by 2 methods : (URL) *127.0.0.1:8000/api/get_score?input='input'*, where 'input' has to be an integer
    a. the browser itself (fastest way: logged into any of the admin user and access the URL)
        <img src="../images/task1.png" width="1120px" style="display: block; margin-left: auto;margin-right: auto;"> 
    b. postman

4. for task 2, admin user can access the django portal to edit from the changelist page, quicker compared to clicking into each record and opening
       <img src="../images/task2.png" width="1120px" style="display: block; margin-left: auto;margin-right: auto;"> 

5. for task 3, assuming there is a new migration:
```
    # 1. run migration code 
    python manage.py migrate
    python manage.py migrate main # or to be more specific 

    # 2. run unit test 
    python manage.py test

    # 3. if test fail, check and unmigrate 
    python manage.py migrate [app: main] [migration: previous_migration]
```

There's actually another method to test migration schema using 'django-test-migrations', but this method is more code heavy