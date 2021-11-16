import pickle

from flask import Flask, request, render_template, url_for

import get_tweets

sentiModel = pickle.load(open("finalized_model.sav", "rb"))

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def hello():
   return render_template('index.html')

@app.route('/sentiment', methods=['POST','GET'])
def get_movie_tweets():
    movie_name = request.form['movie_name']
    final_df = get_tweets.get_data(movie_name)

    tweet_list = []
    tweet_list = final_df['text'].tolist()
    sentiModel = pickle.load(open("finalized_model.sav", "rb"))
    output_list = list(sentiModel.predict(tweet_list))
    listToStr = ' '.join([str(elem) for elem in output_list])

    for i in range(len(output_list)):
        final_df.loc[final_df.index[i], 'sentiment'] = output_list[i]
    cnt_of_pos_neg = list(final_df['sentiment'].value_counts())
    df_final=final_df['text']
    final=df_final.to_frame()
    tweets=final.rename(columns={"text": "Tweets"})
    tweets.index = tweets.index + 1
    return render_template('sentiment.html',  tables=[tweets.to_html(classes='movie')], titles='', cnt_of_pos_neg=cnt_of_pos_neg)


if __name__ == '__main__':
    app.run()
