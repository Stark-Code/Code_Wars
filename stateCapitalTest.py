import random

capitals = {
    'Alabama': 'Montgomery',
    'Alaska': 'Juneau',
    'Arizona':'Phoenix',
    'Arkansas':'Little Rock',
    'California': 'Sacramento',
    'Colorado':'Denver',
    'Connecticut':'Hartford',
    'Delaware':'Dover',
    'Florida': 'Tallahassee',
    'Georgia': 'Atlanta',
    'Hawaii': 'Honolulu',
    'Idaho': 'Boise',
    'Illinios': 'Springfield',
    'Indiana': 'Indianapolis',
    'Iowa': 'Des Monies',
    'Kansas': 'Topeka',
    'Kentucky': 'Frankfort',
    'Louisiana': 'Baton Rouge',
    'Maine': 'Augusta',
    'Maryland': 'Annapolis',
    'Massachusetts': 'Boston',
    'Michigan': 'Lansing',
    'Minnesota': 'St. Paul',
    'Mississippi': 'Jackson',
    'Missouri': 'Jefferson City',
    'Montana': 'Helena',
    'Nebraska': 'Lincoln',
    'Neveda': 'Carson City',
    'New Hampshire': 'Concord',
    'New Jersey': 'Trenton',
    'New Mexico': 'Santa Fe',
    'New York': 'Albany',
    'North Carolina': 'Raleigh',
    'North Dakota': 'Bismarck',
    'Ohio': 'Columbus',
    'Oklahoma': 'Oklahoma City',
    'Oregon': 'Salem',
    'Pennsylvania': 'Harrisburg',
    'Rhoda Island': 'Providence',
    'South Carolina': 'Columbia',
    'South Dakoda': 'Pierre',
    'Tennessee': 'Nashville',
    'Texas': 'Austin',
    'Utah': 'Salt Lake City',
    'Vermont': 'Montpelier',
    'Virginia': 'Richmond',
    'Washington': 'Olympia',
    'West Virginia': 'Charleston',
    'Wisconsin': 'Madison',
    'Wyoming': 'Cheyenne'
}

for i in range(1, 11):
    quizFile = open(f'./CapitalTests/capitals_quiz{i}.txt', 'w')
    answerFile = open(f'./CapitalTests/answers{i}.txt', 'w')

    quizFile.write(f'Name\nDate\n')
    quizFile.write((' ' * 20) + f'State Capitals Quiz {i} \n')

    states = list(capitals.keys())
    random.shuffle(states)

    for questionNum in range(50):
        correctAnswer = capitals[states[questionNum]]
        wrongAnswers = list(capitals.values())
        del wrongAnswers[wrongAnswers.index(correctAnswer)]
        wrongAnswers = random.sample(wrongAnswers, 3)
        answerOptions = [correctAnswer] + wrongAnswers
        random.shuffle(answerOptions)

        quizFile.write(f'{questionNum}. What is the capital of {states[questionNum]}? \n')
        for i in range(4):
            quizFile.write(f'\t {"ABCD"[i]}.  {answerOptions[i]}\n')
        quizFile.write('\n')

        answerFile.write(f'{questionNum}: {"ABCD"[answerOptions.index(correctAnswer)]}\n')
    quizFile.close()
    answerFile.close()
# Create 10 quizzes with unique questions and answers
# Create a Header
# Shuffle order of states
