## project name = Task_Management

## Project Description 
-  The Task_management project is a task managing django api that provide features such as creating, deleting, and updating task status, filtering, searching and sorting tasks and categories with their title, due_date, status and priority. The api additionaly offers user management and authentication features.

- to biuld this api i used 
    -Django
    -rest_framework
    -mySQL
    -rest_framework.authtoken,
    -rest_framework_simplejwt.token_blacklist

- to manage users properly the api uses custom User model with fields such as 'username' and 'email'. it extends 'AbstractUser' class from 'django.contrib.auth.models' and have a user manager model to create user and super user extending 'BaseUserManager' class from 'django.contrib.auth.models'.

- the api have two more model to manage Tasks and Categories. 'Task' model with 'title', 'description', 'due_date', 'priority', 'status', 'completed_at', 'user' and 'category' fields and 'Category' model with 'name' and 'user' fields.

- the 'Task' and 'Category' models are both linked to 'User' model with 'ForeignKey' field to ensure one to many relationship and both are conected to each other with 'ForeignKey' field to ensure one task can only have one user and category, one category can have multiple tasks and only one user and a user having multiople categories and tasks.

- for users authentication the project is using 'rest_framework_simplejwt.authentication.JWTAuthentication' authentication class for token authentication.

- to create a task, view availeble tasks and categories, delete or update tasks and categories a user must be authenticated.

- for a first time a user must sign up or register by sending his/her information to {user/register/} with POST request and raw JSON data 
{
    "username": "username",
    "password":"password",
    "email": "email"
}

- after complete registration a user can get its auth token by loging in by sendig a POST request to {user/login/} with raw JSON data of its email and password
{
    "email": "email",
    "password":"password" 
}
if the user data is valid the api sends respons with "refresh" and "access" tokens.

- after getting "refresh" and "access" tokens, a user can send other requests for creating, updatin, deleting tasks and categoryies and to logout and delete their acount.

- to create task a user can send a POST request to {task/create/} with authentication header containing accsess token and the raw JSON data 
{
    "title": "title",
    "description": "description",
    "due_date": "due_date",
    "priority": "priority choice from 'Low', 'Medium' and 'High'
}

- to create category a user can send a POST request to {task/category/create} with authentication header containing accsess token and the raw JSON data 
{
    "name": "name of the category"
}

- to update a task to create task a user can send a POST request to {task/update/<str:title>} with authentication header containing accsess token, the title of the task in the url and the raw JSON data 
{
    "title": "title",
    "description": "description",
    "due_date": "due_date",
    "priority": "priority choice from 'Low', 'Medium' and 'High'
    "status":"status choice from "Pending" and "Completed"
}

- to update a category a user can send a PUT or PATCH request to {task/category/update/<str:name>} with authentication header containing accsess token, the name of the category in the url and the raw JSON data 
{
    "name": "name"
}

- to delete a task a user can send a DELETE request to {task/delete/<str:title>} with authentication header  containing accsess token.

- to delete a category a user can send a DELETE request to {task/category/delete/<str:name>} with authentication header  containing accsess token.

- to list all the tasks of the user a user can send GET request to {task/list/} with authentication header  containing accsess token. optionaly a user can search to a task by title or by description by sendig it to {task/list/?title="title"} and {task/list/?description="description"} and to sort with due_date a user can use {task/list/?sort_by=due_date} for assendig and {task/list/?sort_by=due_date&sort_order=desc} for dessending sorting.

- for filltering tasks by due_date, status, category and prioirty a user can use {task/list/?status="status"},{ task/list/?due_date="due_date"}, 
{task/list/?category="category"}, 
{task/list/?priority="priority"}

- to access the details of a specific task a user can send a GET request to {task/detail/<str:title>/}  with authentication header  containing accsess token.


