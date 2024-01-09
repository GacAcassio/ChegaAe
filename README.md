# Chêga Ae
### Video demo: <https://youtu.be/xCHVq3vSLRo>
### Description:

Hello, I'm Gabriel, and this project marks the culmination of my CS50x journey. I chose to create a website focused on the material history of my city (Cuiabá - Brazil), aiming to increase its popularity and educate people about its significance and rich history. The website has pages dedicated to Cuiabá history, a forum, a contact  and a page to see the weather.

For the design, I opted for a flat art style due to its simplicity, making the webpage more appealing and accessible to a diverse audience. I used Adobe Illustrator for page layout and illustration creation, as I have more experience with it compared to other tools like Figma.

The technologies employed in the project include HTML, JavaScript, Python, Flask, MySQL, and WeatherAPI (www.weatherapi.com). For purpose of knowledge, the website has a forum, an account system and a weather API connection.

> The title "Chêga Ae" is a reference to the local Portuguese accent,  an important piece of our culture and indentity. It sounds like an invitation to visit us, like "come  here".


## Files

For my project I used the file design pattern taught in CS50, using a folder to statics, a folder to templates and a main folder.

## Flask_session

This folder is form flask  library, and stores user's sessions.

## Statics

### icon.ico

This file  is my website icon, it is a picture of the sun. I made this choice because my city is one of the hottest city in Brazil, and one of the ones with most sunny days in the year.  Then, I thought the sun could represent well Cuiabá.

### files .txt

  These files are  dedicated to store the website contents. Making this, I can save the program main memory and have a better organization.

### files .svg

These files store my illustration to the project. We have already four, but I have plans of making more.

### file style.css

These file store my css ids and classes.

## Templates

### about.html

In this template i tell people about the project and its execution.

### contact.html

In this page the visitor can send me a message. The message will be redirected to my email using flask_mail.

### error.html

This page is to return to users the errors. The image in it makes reference to a non successful train project in Cuiabá.

### forum.html

This page is dedicated to show users all the topics on the forum. They also can be redirected to specific topics or redirected to newtopic.html.

### home.html

This page is my home page, using app.py i show a random image each time that a user opens it. I tried some JavaScript in the bottom History.

### layout.html

This page defines page's navigation bar and footer. i applied it to other pages using Jinja blocks.

### login.html

This page is dedicated to users login and is based on CS50 finance project.

### newtopic.html

In this page a user can create a new forum topic. They are also able to delete their own topics.

### place.html

This page is for showing users information about  remarkable places in Cuiabá. The page imports texts from static folder.

### places.html

This page lists all pages already registered on the website. I plan to create a page to send the picture  and text of place page and then store it in the database.

### register.html

This page is dedicated to users register and is based on CS50 finance project.I just changed the style.

### viewtopic.html

In this page a user can see topic's details and comment on them.

### weather.html

This page displays actual weather in Cuiabá. The data is imported using an API.

## FinalProject

### App.py

This is my main code and controls the routes, mail service and sessions.

### chegae.db

This is my database document.

### helpers.py

This file contains session function and the connection with the weather API.
