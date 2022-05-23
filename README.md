# Shopify Backend Challenge

> Replit Link: 
> -   Backend API: https://shopify-product-challenge.nhd36.repl.co
> -   Frontend: https://replit.com/@nhd36/shopify-product-challenge-frontend

## 1. Introduction
- --
- The project was designed and built based on the requirements of **Shopify Backend Challenge**
- Features completed so far:
  - Basic CRUD Functionality to interact with Inventory data
  - Allow image uploads and store image with generated thumbnails
  - When deleting, allow deletion comments and undeletion

- Technology I am using in this project: ***Flask, Python, SQLAlchemy(ORM), MySQL, Docker, Docker-Compose***
## 2. Database Design
- --
- Inventory:
    - Inventory schema has fields: id, name, amount, created_at, deleted_at, has_image; represent basic information of an inventory.
    - I index 4 fields, since I will mainly query based on these fields: **id, added_by, created_at, deleted_at**
    - *has_image* will boolean value if inventory has image, then we will be able to use the id to query for particular image.
    - *created_at* and *created_at* will store the number of seconds in UTC. 
    - *deleted_at* will always be NULL at the beginning, so whenever we want to implement soft delete, we can fill the row with timestamp in seconds data. If we want to undelete, we can make the this field NULL again.
    
## 3. File Folder Structure and Explanation:
- --

```
shopify
└───backend
│   │   └───src
│   │   │   │   __init__.py
│   │   │   │   utils.py <containing supporting methods>
│   │   │   └───database
│   │   │   │   __init__.py
│   │   │   │   database.db <SQLite database file>
│   │   │   │   interface.py <containing interface of Inventory>
│   │   │   │   models.py <containing schemas of the Inventory>
│   │   │   └───services
│   │   │   │   │   __init__.py
│   │   │   │   └───inventory <API will be designed in this folder>
│   │   │   │   │   │   __init__.py
│   │   │   │   │   │   interface.py <containing interface of each layer to apply Single Responsibility>
│   │   │   │   │   │   database_handler.py <Database integration layer, converts all Inventory object to dictionary>
│   │   │   │   │   │   logic_handler.py <Logic interact creation layer, all logic goes into this layer>
│   │   │   │   │   │   transport.py <Transport layer which converts all the logic into API format>
│   │   └───static <Contains all images of Inventory uploading from client>
│   │   └───test <folder to write test for each layer>
│   │   app.py <Run application>
│   │   Dockerfile <Application can be run as Docker container, expose to port 5000>
│   │   docker-compose.yml <Application can be run with Docker Compose>
│   │   start.sh <Script to run everything from the start>
│   │   ...
└───frontend <containing frontend code to support understanding API>
│   │   ...
```
    
## 4. API Endpoints
- --



## 5. Setup
- --
- Make sure that you filled out all the requiring fields based on ***.env.format***
### Setup Manually with Local Machine
- The machine that I am using right now is Ubuntu 20.04. For those who run in different OS, I don't really know if setup will work, so I recommend running the Docker setup below.
- Make sure that you have Python >= 3.6 in your machine, for those lower version of Python, I do not guarantee that it will run smoothly.
- Create virtual environment for your project:
  > python3 -m virtualenv venv
- Activate your virtual environment
  > pip3 install -r requirements.txt
- Run script with **start.sh**
  > ./start.sh

### Setup with Docker
- Your machine must have *Docker* installed to be able to run this setup.
- We make a little change in .env file in order to be able to connect different containers in Docker system.
  > **NOTES**: You can customize the docker-compose file to fit with your technology services 
- To run on *dev* environment, we will use ***docker-compose***
  > source ./env/.env && docker-compose -f docker-compose.yml up

  #### Enjoy!