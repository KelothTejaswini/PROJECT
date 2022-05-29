from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd

item_similarity_df = pd.read_csv("movie_similarity.csv", index_col=0)

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_from_root():
    return render_template('./Microsoft/index.html')

@app.route("/recms", methods = ["POST"])
def make_rec():
    if request.method == "POST":
        x = request.form
        print(x)
        data = request.form
        movie = data["movie_title"]
        #curl -X POST http://0.0.0.0:80/recms -H 'Content-Type: application/json' -d '{"movie_title":"Heat (1995)"}'
        try:
            similar_score = item_similarity_df[movie]
            similar_movies = similar_score.sort_values(ascending=False)[1:50]
            api_recommendations = similar_movies.index.to_list()
        except:
            api_recommendations = ['Movie not found']
        print(api_recommendations)
        return render_template('./Microsoft/Movies.html',rec_movie=api_recommendations)


if __name__ == "__main__":
    app.run(host='localhost', port=8080)
