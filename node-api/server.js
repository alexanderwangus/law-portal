// BASE SETUP
// =============================================================================

// call the packages we need
var express    = require('express');
var bodyParser = require('body-parser');
var app        = express();
var morgan     = require('morgan');

// configure app
app.use(morgan('dev')); // log requests to the console

// configure body parser
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port     = process.env.PORT || 8080; // set our port

// ROUTES FOR OUR API
// =============================================================================

// create our router
var router = express.Router();

// middleware to use for all requests
router.use(function(req, res, next) {
	// do logging
	console.log('Something is happening.');
	next();
});

router.get('/', function(req, res) {
	var MongoClient = require('mongodb').MongoClient;
	MongoClient.connect("mongodb://localhost:27017/test", function(err, db) {
	  if(err) { return console.dir(err); }

	  var collection = db.collection('test');


	  var stream = collection.find({}).stream();
	  var responseString = ""
	  stream.on("data", function(item){
	  	console.log("data");
	  	console.log(item);
	  	responseString += item.word + " ";
	  });
	  stream.on("end", function(){
	  	res.send(responseString)
	  	db.close();
	  })
	});
});

router.get('/range', function(req, res) {
	var startYear = parseInt(req.query.start);
	var endYear = parseInt(req.query.end);
	var MongoClient = require('mongodb').MongoClient;
	MongoClient.connect("mongodb://localhost:27017/test", function(err, db) {
	  if(err) { return console.dir(err); }

	  var collection = db.collection('test');


	  var stream = collection.find({
	  	"$and": [
		  	{"year": {"$gte": startYear}}, 
		  	{"year": {"$lte": endYear}}
		  ]
		}).stream();
	  var responseString = ""
	  stream.on("data", function(item){
	  	console.log("data");
	  	console.log(item);
	  	responseString += item.word + " ";
	  });
	  stream.on("end", function(){
	  	res.send(responseString)
	  	db.close();
	  })
	});
});


// REGISTER OUR ROUTES -------------------------------
app.use('/', router);

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);
