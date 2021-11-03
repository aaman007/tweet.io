## Installation and Setup

### 1. Create .env file
Run the following command
```cp .env.example .env```         
Environment [DEVELOPMENT, STAGING, PRODUCTION] and SECRET could be changed optionally.      
Changing the Environment Mode to anything else would require PostgreSQL db configuration to be updated as well.        
As, In DEVELOPMENT mode, sqlite is used as db this is not required
      

### 2. Creating virtual environment
Run ```virtualenv venv``` command inside the project directory       
Run ```source venv/bin/activate``` to activate the environment          
If you are using PyCharm, you can do the same thing using GUI

### 3. Installing Dependencies
All the dependencies are in ```requirements.txt``` file. Run the following command to install them -             
``` pip install -r requirements.txt ```


### 4. Database Migration
Run the following command to migrate changes to the db           
``` python manage.py migrate ```


### 5. Running the application
``` python manage.py runserver ```         
or    
``` python manage.py runserver 0:PORT ``` [This requires the BASE_URL in the frontend to be changed]


### 6. [Optional] Creating Test Data
Fake data can be created by running -     
``` python manage.py create_test_data ```      
1,000 Users, for each user [0 to 10] follow relation and 10,000 tweets with random user would be created        
This could be configured by going to ```core/management/commands/create_test_data.py``` file and  updating the global variables


### 7. [Optional] Create a Superuser
To access the admin panel, a superuser account is required.             
Run the following command to create one -             
``` python manage.py createsuperuser ```