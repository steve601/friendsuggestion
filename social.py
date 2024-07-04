from flask import Flask,render_template,request
import pickle
import numpy as np

app = Flask(__name__)
data = pickle.load(open('facebook.pkl','rb'))
sim = pickle.load(open('facebooksim.pkl','rb'))

person_names = data['name'].values

#defining recommendation function
def suggest(new_person):
    # obtaining the index of the new person from the dataframe
    ind = data[data['name'] == new_person].index[0]
    #'cosine[ind]' obtains the similarity for the 'new person','list(enumerate())'  creates a list of an 
    # iterable that produces pairs of (index, value),'sorted' sorts the list, 'reverse=True' sorts
    # the list in descending order rather than default ascending order,'key = lambda x:x[1]' specifies that 
    # list should be sorted using the similarity not its index i.e [(3,0.98),(2,0.67),(1,0.45)]
    distance = sorted(list(enumerate(sim[ind])),reverse = True,key = lambda x: x[1])
    suggestions = list()
    for i in distance[1:11]:
        suggestions.append(data['name'].iloc[i[0]])
        
    return suggestions

@app.route('/')
def homepage():
    return render_template('social.html',person_names = person_names)


#getting movie from the form and calling the recommendation function
@app.route('/suggest',methods=['POST'])
def predict():
    name_of_person = request.form.get('person')
    sugg = suggest(name_of_person)
    return render_template('social.html',suggestions = sugg,person_names = person_names,name_of_person = name_of_person)


if __name__ == '__main__':
    app.run(host = "0.0.0.0")
    
