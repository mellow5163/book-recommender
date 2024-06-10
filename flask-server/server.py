from flask import Flask, request, jsonify
import json
import certifi
import pandas as pd
import numpy as np
import seaborn as sns
import sklearn
import sklearn.model_selection
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import re

from flask_cors import CORS
from fuzzywuzzy import process
#from rapidfuzz import process

import knn_model

import pickle as pk
#from knn_model import *


app = Flask(__name__)
CORS(app, resources={r"/register_books": {"origins": "http://localhost:3000"}})


@app.route('/register_books', methods=['OPTIONS'])
def handle_preflight():
    response = jsonify({'message': 'Preflight request successful'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response




url_large = 'https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv'

columns_of_books_table = ['book_id','goodreads_book_id','best_book_id','work_id','books_count','isbn',
                            'isbn13','authors','original_publication_year','original_title','title',
                            'language_code','average_rating','ratings_count','work_ratings_count',
                            'work_text_reviews_count','ratings_1','ratings_2','ratings_3','ratings_4',
                            'ratings_5','image_url','small_image_url']


data = pd.read_csv(url_large, nrows=100)
data.fillna(value='field is empty', inplace = True)

all_books = data.to_json(orient='records', indent=4)

books = data.values.tolist()

#print(data.iloc[:, 9])
#@app.route('/test_model', methods=['GET'])
#def test_model():
#    knn_model.test_find_similar_books_wrapper("Wicked: The Life and Times of the Wicked Witch of the West")
#    return {}

#stores inputted books
@app.route('/register_books', methods=[ 'POST'])
def register_books():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data received"}), 400
    

    books_received = data.get('books_received')
    if books_received is None:
        return jsonify({"error": "Key 'books_recieved' is missing from the data"}), 400

    



    received = list()



    received = list()

    for title in books_received:
        title_found = False
        title = title.lower().strip()

        match = process.extractOne(title, [str(book_info[9]) for book_info in books])

        print(f"Title: {title}, Match: {match}")
        if match and match[1] >= 90:  # Adjust the threshold as needed
            title_found = True
            received.append(match[0])

        if not title_found:
            print("yes")
            return jsonify({"error": f" '{title}' not found in the dataset, please check your spelling or enter another book"}), 400



    

        #if not title_found:
        #    print("yes")
        #    return jsonify({"error": f" '{title}' not found in the dataset, please check your spelling or enter another book"}), 400


 

    print(f"Received: {received}")

    recs = []

    for title in received:
        if knn_model.test_find_similar_books_wrapper != None:
            recs.extend(knn_model.test_find_similar_books_wrapper(title))

    print("recs:", recs)





    return jsonify(recs)

    

    return jsonify({'message': 'Books recieved'})
















if __name__ == "__main__":
    app.run(port=4000, debug=True) #in development mode