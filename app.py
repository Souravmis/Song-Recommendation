from flask import Flask, render_template, request


import pickle
import re

from song_recommendation import Recommend_by_neighbors
app = Flask(__name__)


picklefile = open('model', 'rb')
#unpickle the dataframe
model = pickle.load(picklefile)
#close file
picklefile.close()


posts = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/submit", methods=["POST"])
def submit_text():
    song = request.form["text"]
    
    global model, posts
    recommended = model.make_recommendation(new_song = song, n_recommendations= 10)
    
    songs = []
    distance = []
    if recommended != '404' :
        for rec in recommended:
            (s, d) = rec
            songs.append(s)
            distance.append(d)
        posts = []
        for s in songs:
            s = re.sub("[0,1,2,3,4,5,6,7,8,9,-]", "", s)
            posts.append(s)
    else:
        posts = []
        posts.append("No such song found, try it again")

    # # # print(type(a))
    return render_template('submit.html', posts = posts, title = "Your Top 10 Recommendation")


if __name__ == "__main__":
    app.run(port=8069, debug=True)

