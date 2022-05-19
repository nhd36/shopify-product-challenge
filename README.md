# Shopify Backend Challenge

> Demo Link: 

## Introduction
- --
- The project was designed and built based on the requirements of **Shopify Backend Challenge**
- Features completed so far:
  - Basic CRUD Functionality to interact with Inventory data
  - Allow image uploads and store image with generated thumbnails
  - When deleting, allow deletion comments and undeletion

- Technology I am using in this project: ***Flask, Python, SQLAlchemy(ORM), MySQL, Docker, Docker-Compose, AWS S3***
- I don't have enough time to implement ***test*** API. I will include in the future.
## Database Design
- --
- Inventory:
    - Inventory schema has fields: id, name, amount, created_at, deleted_at, has_image; represent basic information of an inventory.
    - I index 4 fields, since I will mainly query based on these fields: **id, added_by, created_at, deleted_at**
    - *has_image* will boolean value if inventory has image, then we will be able to use the id to query for particular image.
    - *created_at* and *created_at* will store the number of seconds in UTC. 
    - *deleted_at* will always be NULL at the beginning, so whenever we want to implement soft delete, we can fill the row with timestamp in seconds data. If we want to undelete, we can make the this field NULL again.

## Documentation
- --
- You can find the documentation for the application in this link: https://app.swaggerhub.com/apis-docs/nhd36/ShopifyChallenge/1.0.0 (Continue to update)

## Setup
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
  #### Enjoy!

### Setup with Docker
- Your machine must have *Docker* installed to be able to run this setup.
- We make a little change in .env file in order to be able to connect different containers in Docker system.
  > **NOTES**: You can customize the docker-compose file to fit with your technology services 
- To run on *dev* environment, we will use ***docker-compose***
  > source ./env/.env && docker-compose -f docker-compose.yml up

  #### Enjoy!