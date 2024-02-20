from flask import Flask, render_template, request
import pandas as pd
import numpy as np


popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')

app = Flask(__name__)

@app.route('/')
def index():
   
    rating_column = 'avg_rating' if 'avg_rating' in popular_df.columns else None

    return render_template('indexed.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df[rating_column].values) if rating_column else []
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
   
    index_array = np.where(pt.index == user_input)[0]

    if len(index_array) > 0:
        index = index_array[0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        print(data)
    else:
        
        data = []

    return render_template('recommend.html', data=data)

@app.route('/contact')
def contact_us():
    return render_template('contact.html')


@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
