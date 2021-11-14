import pickle
loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
predict_this = ["Sarthak is extra ordinary","This is really bad", "I fell asleep for the SECOND time watching dune. Not because it’s a bad movie but I just keep watching it when I’m"]
print(loaded_model.predict(predict_this))
