# Project: Build an Item Catalog Application

## Part of Udacity Full Stack Web Developer Nanodegree Program

### Project Overview
Develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

### Project's files:
database_setup.py - creates the sqlite database and related tables
server.py - runs the web app
populate_database.py - inserts values to the tables created by database_setup.py
auth.py - authentication function and helper function to work with users
static - for css styles
templates - for HTML templates


### Requirements
  * Install Python 3, to check version: `Python --version`
  * Install [Vagrant](https://www.vagrantup.com/) 
  * Install [Virtual Box](https://www.virtualbox.org/)
  * [google Oauth Cient](https://console.developers.google.com/)

 ### Run 
  * Start Terminal and navigate to the project folder.
  * cd to the vagrant directory
  * Launch the Vagrant VM inside Vagrant sub-directory:
    using command: `vagrant up` and log in command `vagrant ssh` 
  * Run `python3 database_setup.py` to create sqlite database and tables.
  * To populate the database run populate_database.py
  * Run `python3 server.py` to run the application.
  * In a web browser connect to the localhost:8000 
  * If your are an authenticated user (Google or Facebook sign in), you can manage categories and items. 


  ### How to use Google sign in
    * Go to [Google APIs Console](https://console.developers.google.com/apis)
    * Sign up or Login.
    * Go to Credentials.
    * Select OAuth Client ID.
    * Select Web Application.
    * Enter the name of your project 'My Project'.
    * Set the authorized JavaScript origins `http://localhost:8000`, save changes.
    * Copy the Client ID and paste it into login.html in your templates folder.
    * On the consol download JSON file.
    * Rename JSON file to client_secrets.json
    * Put JSON file in your project's directory.
    * Run your application.