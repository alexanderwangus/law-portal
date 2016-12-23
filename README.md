# Law Portal

## Installation

This project uses Node.js and MongoDB. Make sure you have both installed on your machine, and have MongoDB up and running before proceeding.

With Node installed, navigate to the root directory of this project and run:
```
npm install
```
This will install all the required node modules to run this project.

## Usage

First we must populate the MongoDB with data. We have a script that inserts fake data into MongoDB. Check the load_data_mongo.py file to make sure the url it is connecting to matches what you have set up for your MongoDB.

```
python load_data_mongo.py
```

Next, we can start up the web server:
```
node server.js
```
In your web browser, navigate to `http://localhost:8080` to see the contents of the database printed out. Navigate to `http://localhost:8080/range?start=<START>&end=<END>` to see the contents of the database filtered by a year range printed out. For example, to see all words from the years 2001 to 2004 inclusive, I would navigate to http://`localhost:8080/range?start=2001&end=2004`.

That's it! Feel free to expand on this foundation to add more functionality and support more interesting queries.