#!/usr/bin/python
# -*- coding: utf-8 -*-


import flask
from flask import render_template
from flask import request
from fantasticsearch import fantasticsearch
import Recommendation
from elasticsearch import Elasticsearch


#TODO: Configuration
host = "http://localhost:9200"
indexName = "songindex"
aggregationFields = ["text", "text"]


es = Elasticsearch(host)

listSelection = []
recommended = []
titledRecommended = []

Recommendation.test()

Recommendation.create_model()


@fantasticsearch.route('/')
def index():
	term = "*"

	results = performQuery(term, "", 0)
	
	return render_template('index.html', results=results, term=term, aggregationFields = aggregationFields, page=1, listSelection = listSelection)


@fantasticsearch.route('/search')
def search():

	term = request.args.get('term', '')
	filters = request.args.get('filter', '')
	page = request.args.get('page', '')

	

	if not term or term == "null":
		term = "*"
		
	print("search methods with terms : ", term)
	results = performQuery(term, filters, page)


	print("----- Here are the results --------")
	for x in results:
		print (x)

	print("----- Result aggregations  --------")
	for y in results['aggregations']:
		print (y)

	print("----- aggregationFields   ---------")
	for z in results['aggregations'][aggregationFields[0]]:
		print(z)


	print("----- Buckets   ---------")
	for a in results['aggregations'][aggregationFields[0]]['buckets']:
		print(a)

	print("------ Bucket type ------")
	print(type(results['aggregations'][aggregationFields[0]]['buckets']))
	print(results['aggregations'][aggregationFields[0]]['buckets'])
	bucket = results['aggregations'][aggregationFields[0]]['buckets']
	#print("Bucket key : ", bucket.key)

	global Gterm 
	Gterm = term
	Gfilters = filters
	Gpage = page
	global Gresults
	Gresults = results

	print("search term : "+term)
	
	return render_template('index.html', results=results, filters=filters, term=term, page=page, aggregationFields = aggregationFields, listSelection = listSelection)

@fantasticsearch.route('/select')
def select():

	selected_song = request.args.get('song_id','')
	title = request.args.get('title','')
	print("------------------------ Select song --------------------")
	print(selected_song)
	print("----------------------------------------------------------")
	global listSelection
	listSelection.append((selected_song,title))
	print("listSelection :")
	print(listSelection)
	print("term to go back :"+ Gterm)
	return render_template('index.html', results=Gresults, term=Gterm, aggregationFields = aggregationFields, listSelection = listSelection, titledRecommended = titledRecommended)

@fantasticsearch.route('/recommend')
def recommend():
	print("Doing recommendation !")
	user_items = [song_id for (song_id,title) in listSelection]
	print(user_items)
	global recommended
	recommended = Recommendation.recommend(user_items)
	print("recommended songs :")
	print(recommended)

	global titledRecommended
	titledRecommended = [Recommendation.titleOf(song_id) for song_id in recommended]
	print("titledRecommended : ")
	print(titledRecommended)
	return render_template('index.html', results=Gresults, term=Gterm, aggregationFields = aggregationFields, listSelection = listSelection, titledRecommended = titledRecommended)

@fantasticsearch.route('/clear')
def clear():
	print("Clear selection")
	global listSelection
	global titledRecommended
	titledRecommended = []
	listSelection = []
	return render_template('index.html', results=Gresults, term=Gterm, aggregationFields = aggregationFields, listSelection = listSelection, titledRecommended = titledRecommended)


def performQuery(term, filterString, page):

	filters = parseFilters(filterString)

	term = term.encode('utf-8')			
	query = getBasicQuery(filters, term, page)	

	result = es.search(index=indexName, body=query)

	return result 



def parseFilters(filters):
	filterDict = {}
	for f in filters.split(','):
		if f and len(f.split('-')) == 2: 	
			typ = f.split('-')[0].encode('utf-8')
			val = f.split('-')[1].encode('utf-8')
			filterDict[typ] = val
	
	return filterDict


#Those queries implement the filters as AND filter and the query as query_string_query
def getBasicQuery(filters, term, page):
	query = None
	
	if not page:
		page = 0
	start = int(page) * 12

	mustClauses = []
	for k,v in filters.iteritems():
		clause = {"term" : { k : v }}
		mustClauses.append(clause)	
	filterClauses = {"and" : mustClauses }

	aggregations = {}
	for el in aggregationFields:
		aggregations[el] = {"terms" : {"field" : el }}


	if term and filters:
		query = {
			"query": {
		         	"filtered": {
			 	      "filter": filterClauses,
			 	      "query": { "query_string" : { "query" : term } }
				   }
		   		},
		   	"size": 12,
		   	"from": start, 
		   	"aggs" : aggregations
		}

	elif term:
		query = { 
			"query": { 
				"query_string" : { "query" : term }
			},
		   	"size": 12,
		   	"from": start, 
		   	"aggs" : aggregations
		}


	return query

Gterm = "*"
Gresults = performQuery(Gterm, "", 0)