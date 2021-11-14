import pickle

from flask import Flask, request, render_template

import get_tweets

sentiModel = pickle.load(open("finalized_model.sav", "rb"))

app = Flask(__name__)

@app.route("/")
def hello():
   return render_template('index.html')

@app.route('/sentiment', methods=['POST','GET'])
def hello_world():  # put application's code here
    movie_name = request.form['movie_name']
    final_df = get_tweets.get_data(movie_name)

    tweet_list = []
    tweet_list = final_df['text'].tolist()
    sentiModel = pickle.load(open("finalized_model.sav", "rb"))
    output_list = list(sentiModel.predict(tweet_list))
    listToStr = ' '.join([str(elem) for elem in output_list])

    for i in range(len(output_list)):
        final_df.loc[final_df.index[i], 'sentiment'] = output_list[i]
    return render_template('sentiment.html',  tables=[final_df.to_html(classes='data')], titles=final_df.columns.values)


if __name__ == '__main__':
    app.run()
