
import os
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)


# Quiz questions database
QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "answer": 2
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": 1
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "answer": 1
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "answer": 2
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "answer": 2
    },
    {
        "question": "Which country is home to Machu Picchu?",
        "options": ["Brazil", "Peru", "Chile", "Argentina"],
        "answer": 1
    },
    {
        "question": "What is the fastest land animal?",
        "options": ["Lion", "Cheetah", "Leopard", "Tiger"],
        "answer": 1
    },
    {
        "question": "How many sides does a hexagon have?",
        "options": ["5", "6", "7", "8"],
        "answer": 1
    },
    {
        "question": "What is the smallest country in the world?",
        "options": ["Monaco", "Nauru", "Vatican City", "San Marino"],
        "answer": 2
    },
    {
        "question": "Which gas makes up most of Earth's atmosphere?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
        "answer": 1
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "answer": 1
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "options": ["Gold", "Iron", "Diamond", "Platinum"],
        "answer": 2
    },
    {
        "question": "Which ocean is the largest?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": 3
    },
    {
        "question": "What year did World War II end?",
        "options": ["1944", "1945", "1946", "1947"],
        "answer": 1
    },
    {
        "question": "Which vitamin is produced when skin is exposed to sunlight?",
        "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"],
        "answer": 3
    },
    {
        "question": "What is the currency of Japan?",
        "options": ["Yuan", "Won", "Yen", "Ringgit"],
        "answer": 2
    },
    {
        "question": "How many continents are there?",
        "options": ["5", "6", "7", "8"],
        "answer": 2
    },
    {
        "question": "What is the largest organ in the human body?",
        "options": ["Brain", "Heart", "Liver", "Skin"],
        "answer": 3
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Osmium", "Oxygen", "Oganesson", "Olivine"],
        "answer": 1
    },
    {
        "question": "What is the tallest mountain in the world?",
        "options": ["K2", "Kangchenjunga", "Mount Everest", "Lhotse"],
        "answer": 2
    },
    {
        "question": "Which programming language is known as the 'mother of all languages'?",
        "options": ["Python", "Java", "C", "Assembly"],
        "answer": 2
    },
    {
        "question": "What is the speed of light?",
        "options": ["299,792,458 m/s", "300,000,000 m/s", "299,000,000 m/s", "301,000,000 m/s"],
        "answer": 0
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Stephen Hawking"],
        "answer": 1
    },
    {
        "question": "What is the most abundant element in the universe?",
        "options": ["Oxygen", "Carbon", "Hydrogen", "Helium"],
        "answer": 2
    },
    {
        "question": "Which country invented paper?",
        "options": ["Egypt", "Greece", "China", "India"],
        "answer": 2
    },
    {
        "question": "What is the longest river in the world?",
        "options": ["Amazon", "Nile", "Yangtze", "Mississippi"],
        "answer": 1
    },
    {
        "question": "How many bones are in an adult human body?",
        "options": ["206", "208", "210", "212"],
        "answer": 0
    },
    {
        "question": "What is the study of earthquakes called?",
        "options": ["Geology", "Seismology", "Meteorology", "Oceanography"],
        "answer": 1
    },
    {
        "question": "Which planet has the most moons?",
        "options": ["Jupiter", "Saturn", "Uranus", "Neptune"],
        "answer": 1
    },
    {
        "question": "What does 'WWW' stand for?",
        "options": ["World Wide Web", "World Weather Watch", "World War Winners", "World Wide Winners"],
        "answer": 0
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    name = request.form.get('name', '').strip()
    if not name:
        return redirect(url_for('home'))
    
    # Store user name and generate random questions
    session['user_name'] = name
    session['questions'] = random.sample(QUESTIONS, 10)
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    if 'user_name' not in session:
        return redirect(url_for('home'))
    
    current_q = session.get('current_question', 0)
    if current_q >= 10:
        return redirect(url_for('results'))
    
    question_data = session['questions'][current_q]
    return render_template('quiz.html', 
                         question=question_data, 
                         question_num=current_q + 1,
                         user_name=session['user_name'])

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'user_name' not in session:
        return redirect(url_for('home'))
    
    current_q = session.get('current_question', 0)
    selected_answer = int(request.form.get('answer', -1))
    
    question_data = session['questions'][current_q]
    correct_answer = question_data['answer']
    
    # Store the answer
    session['answers'].append({
        'question': question_data['question'],
        'selected': selected_answer,
        'correct': correct_answer,
        'is_correct': selected_answer == correct_answer
    })
    
    # Update score
    if selected_answer == correct_answer:
        session['score'] += 1
    
    # Move to next question
    session['current_question'] = current_q + 1
    
    return redirect(url_for('quiz'))

@app.route('/results')
def results():
    if 'user_name' not in session:
        return redirect(url_for('home'))
    
    score = session.get('score', 0)
    answers = session.get('answers', [])
    user_name = session.get('user_name', '')
    
    return render_template('results.html', 
                         score=score, 
                         total=10, 
                         answers=answers,
                         user_name=user_name)

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)