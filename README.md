# sqlalchemy-challenge
My submission for the SQL Alchemy homework challenge

Hello!

This project was tough but I managed to work through it!

To complete this project I take the following steps:

1. Basic analysis in Jupyter Lab
2. create a Flask app to show the data

### BASIC ANALYSIS IN JUPYTER LAB ###

To create the basic analysis I first connect my engine to my sqlite database and convert the found tables into thir own variables

From there I use various queries to find the final date of the data, the most active station in the data, as well as the highest, lowest, and average temperature.

I use these queries to create pandas DataFrames and display a bar graph of dates and precipitation for a single year in hawaii across all stations as well as a histogram of temperatures from the most active station.

### FLASK APP ##

I created a flask app and stated the many routes. My first route defines what routes can be reached in the app.

Each app connects to a session, performs a query, closes the session, then commits a for loop based on the response and returns the data commited to a list through the loop in a JSON.