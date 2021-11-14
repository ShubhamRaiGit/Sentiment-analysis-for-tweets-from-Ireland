from flask import Flask, render_template
import get_tweets
import pickle


sentiModel = pickle.load(open("finalized_model.sav", "rb"))

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    final_df = get_tweets.get_data('Dune OR Venom')
    print(final_df)
    tweet_list = []
    tweet_list = final_df['text'].tolist()
    print(type(tweet_list))
    print(tweet_list)
    sentiModel = pickle.load(open("finalized_model.sav", "rb"))
    output_list = list(sentiModel.predict(tweet_list))
    listToStr = ' '.join([str(elem) for elem in output_list])
    return listToStr


if __name__ == '__main__':
    app.run()
