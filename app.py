from flask import Flask, render_template, jsonify, request
import webbrowser
import os
import signal
import sys

app = Flask(__name__)

# Perguntas para cada nível de dificuldade
questions = {
    "facil": [
        {
        "question": "Qual é a capital do Brasil?", 
        "options": ["Rio de Janeiro", "Brasília", "São Paulo"], 
        "answer": "Brasília"
        },
        {
        "question": "Qual é a capital da França?",
        "options": ["Paris", "Londres", "Berlim"],
        "answer": "Paris"
        },
        {
        "question": "Quantos planetas existem no sistema solar?",
        "options": ["7", "8", "9"],
        "answer": "8"
        },
        {
        "question": "Qual é o maior mamífero do mundo?",
        "options": ["Elefante", "Baleia Azul", "Tubarão Branco"],
        "answer": "Baleia Azul"
        },
        {
        "question": "Quem pintou a Mona Lisa?",
        "options": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso"],
        "answer": "Leonardo da Vinci"
        },
        {
        "question": "Qual é o maior oceano do mundo?",
        "options": ["Atlântico", "Índico", "Pacífico"],
        "answer": "Pacífico"
        },
        {
        "question": "Qual é o nome do presidente dos Estados Unidos em 2021?",
        "options": ["Donald Trump", "Joe Biden", "Barack Obama"],
        "answer": "Joe Biden"
        },
        {
        "question": "Qual é o símbolo químico da água?",
        "options": ["H2O", "CO2", "O2"],
        "answer": "H2O"
        },
        {
        "question": "Quantos dias tem um ano bissexto?",
        "options": ["365", "366", "364"],
        "answer": "366"
        },
        {
        "question": "Qual é o maior país do mundo em área territorial?",
        "options": ["Estados Unidos", "China", "Rússia"],
        "answer": "Rússia"
        },
        {
        "question": "Qual é o nome do maior deserto do mundo?",
        "options": ["Deserto do Saara", "Deserto de Gobi", "Deserto da Arábia"],
        "answer": "Deserto do Saara"
        },
        {
        "question": "Qual é o animal símbolo da Austrália?",
        "options": ["Canguru", "Coala", "Ornitorrinco"],
        "answer": "Canguru"
        },
        {
        "question": "Qual é a cor do céu em um dia claro?",
        "options": ["Azul", "Verde", "Vermelho"],
        "answer": "Azul"
        },
        {
        "question": "Quantos continentes existem no mundo?",
        "options": ["5", "6", "7"],
        "answer": "7"
        },
        {
        "question": "Qual é o nome do maior rio do mundo?",
        "options": ["Rio Amazonas", "Rio Nilo", "Rio Yangtzé"],
        "answer": "Rio Amazonas"
        },
        {
        "question": "Qual é o nome da estrela mais próxima da Terra?",
        "options": ["Sirius", "Alpha Centauri", "Sol"],
        "answer": "Sol"
        },
        {
        "question": "Qual é o nome do processo de fotossíntese?",
        "options": ["Respiração", "Fotólise", "Fotossíntese"],
        "answer": "Fotossíntese"
        },
        {
        "question": "Qual é o nome do maior felino do mundo?",
        "options": ["Leão", "Tigre", "Onça-pintada"],
        "answer": "Tigre"
        },
        {
        "question": "Qual é o nome do maior osso do corpo humano?",
        "options": ["Fêmur", "Tíbia", "Úmero"],
        "answer": "Fêmur"
        },
        {
        "question": "Qual é o nome do inventor da lâmpada?",
        "options": ["Thomas Edison", "Nikola Tesla", "Albert Einstein"],
        "answer": "Thomas Edison"
        }
    ],

    "medio": [
        {
        "question": "Quem escreveu 'Dom Quixote'?", 
        "options": ["Miguel de Cervantes", "William Shakespeare", "Machado de Assis"], 
        "answer": "Miguel de Cervantes"
        },
        {
        "question": "Quem foi o primeiro homem a pisar na Lua?",
        "options": ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin"],
        "answer": "Neil Armstrong"
        },
        {
        "question": "Qual é o nome do autor de '1984'?",
        "options": ["George Orwell", "Aldous Huxley", "Ray Bradbury"],
        "answer": "George Orwell"
        },
        {
        "question": "Qual é o maior planeta do sistema solar?",
        "options": ["Terra", "Júpiter", "Saturno"],
        "answer": "Júpiter"
        },
        {
        "question": "Qual é o nome do processo de divisão celular que resulta em duas células idênticas?",
        "options": ["Mitose", "Meiose", "Fotossíntese"],
        "answer": "Mitose"
        },
        {
        "question": "Qual é o nome do maior osso do corpo humano?",
        "options": ["Fêmur", "Tíbia", "Úmero"],
        "answer": "Fêmur"
        },
        {
        "question": "Qual é o nome do inventor da lâmpada?",
        "options": ["Thomas Edison", "Nikola Tesla", "Albert Einstein"],
        "answer": "Thomas Edison"
        },
        {
        "question": "Qual é o nome do maior felino do mundo?",
        "options": ["Leão", "Tigre", "Onça-pintada"],
        "answer": "Tigre"
        },
        {
        "question": "Qual é o nome do processo de fotossíntese?",
        "options": ["Respiração", "Fotólise", "Fotossíntese"],
        "answer": "Fotossíntese"
        },
        {
        "question": "Qual é o nome da estrela mais próxima da Terra?",
        "options": ["Sirius", "Alpha Centauri", "Sol"],
        "answer": "Sol"
        },
        {
        "question": "Qual é o nome do maior rio do mundo?",
        "options": ["Rio Amazonas", "Rio Nilo", "Rio Yangtzé"],
        "answer": "Rio Amazonas"
        },
        {
        "question": "Qual é o nome do maior deserto do mundo?",
        "options": ["Deserto do Saara", "Deserto de Gobi", "Deserto da Arábia"],
        "answer": "Deserto do Saara"
        },
        {
        "question": "Qual é o nome do maior país do mundo em área territorial?",
        "options": ["Estados Unidos", "China", "Rússia"],
        "answer": "Rússia"
        },
        {
        "question": "Qual é o nome do maior mamífero do mundo?",
        "options": ["Elefante", "Baleia Azul", "Tubarão Branco"],
        "answer": "Baleia Azul"
        },
        {
        "question": "Qual é o nome do maior oceano do mundo?",
        "options": ["Atlântico", "Índico", "Pacífico"],
        "answer": "Pacífico"
        },
        {
        "question": "Qual é o nome do maior planeta do sistema solar?",
        "options": ["Terra", "Júpiter", "Saturno"],
        "answer": "Júpiter"
        },
        {
        "question": "Qual é o nome do maior osso do corpo humano?",
        "options": ["Fêmur", "Tíbia", "Úmero"],
        "answer": "Fêmur"
        },
        {
        "question": "Qual é o nome do maior felino do mundo?",
        "options": ["Leão", "Tigre", "Onça-pintada"],
        "answer": "Tigre"
        },
        {
        "question": "Qual é o nome do maior rio do mundo?",
        "options": ["Rio Amazonas", "Rio Nilo", "Rio Yangtzé"],
        "answer": "Rio Amazonas"
        },
        {
        "question": "Qual é o nome do maior deserto do mundo?",
        "options": ["Deserto do Saara", "Deserto de Gobi", "Deserto da Arábia"],
        "answer": "Deserto do Saara"
        }
    ],

    "dificil": [
        {
        "question": "Qual é o símbolo químico do ouro?", 
        "options": ["Au", "Ag", "Fe"], 
        "answer": "Au"
        },
        {
        "question": "Qual é o nome do processo de divisão celular que resulta em quatro células haploides?",
        "options": ["Mitose", "Meiose", "Fotossíntese"],
        "answer": "Meiose"
        },
        {
        "question": "Qual é o nome do cientista que propôs a teoria da relatividade?",
        "options": ["Isaac Newton", "Albert Einstein", "Stephen Hawking"],
        "answer": "Albert Einstein"
        },
        {
        "question": "Qual é o nome do maior vulcão ativo do sistema solar, localizado em Marte?",
        "options": ["Monte Olimpo", "Monte Everest", "Monte Kilimanjaro"],
        "answer": "Monte Olimpo"
        },
        {
        "question": "Qual é o nome do processo de conversão de luz solar em energia química nas plantas?",
        "options": ["Respiração", "Fotossíntese", "Fermentação"],
        "answer": "Fotossíntese"
        },
        {
        "question": "Qual é o nome do maior osso do corpo humano?",
        "options": ["Fêmur", "Tíbia", "Úmero"],
        "answer": "Fêmur"
        },
        {
        "question": "Qual é o nome do inventor da lâmpada?",
        "options": ["Thomas Edison", "Nikola Tesla", "Albert Einstein"],
        "answer": "Thomas Edison"
        },
        {
        "question": "Qual é o nome do maior felino do mundo?",
        "options": ["Leão", "Tigre", "Onça-pintada"],
        "answer": "Tigre"
        },
        {
        "question": "Qual é o nome do processo de fotossíntese?",
        "options": ["Respiração", "Fotólise", "Fotossíntese"],
        "answer": "Fotossíntese"
        },
        {
        "question": "Qual é o nome da estrela mais próxima da Terra?",
        "options": ["Sirius", "Alpha Centauri", "Sol"],
        "answer": "Sol"
        },
        {
        "question": "Qual é o nome do maior rio do mundo?",
        "options": ["Rio Amazonas", "Rio Nilo", "Rio Yangtzé"],
        "answer": "Rio Amazonas"
        },
        {
        "question": "Qual é o nome do maior deserto do mundo?",
        "options": ["Deserto do Saara", "Deserto de Gobi", "Deserto da Arábia"],
        "answer": "Deserto do Saara"
        },
        {
        "question": "Qual é o nome do maior país do mundo em área territorial?",
        "options": ["Estados Unidos", "China", "Rússia"],
        "answer": "Rússia"
        },
        {
        "question": "Qual é o nome do maior mamífero do mundo?",
        "options": ["Elefante", "Baleia Azul", "Tubarão Branco"],
        "answer": "Baleia Azul"
        },
        {
        "question": "Qual é o nome do maior oceano do mundo?",
        "options": ["Atlântico", "Índico", "Pacífico"],
        "answer": "Pacífico"
        },
        {
        "question": "Qual é o nome do maior planeta do sistema solar?",
        "options": ["Terra", "Júpiter", "Saturno"],
        "answer": "Júpiter"
        },
        {
        "question": "Qual é o nome do maior osso do corpo humano?",
        "options": ["Fêmur", "Tíbia", "Úmero"],
        "answer": "Fêmur"
        },
        {
        "question": "Qual é o nome do maior felino do mundo?",
        "options": ["Leão", "Tigre", "Onça-pintada"],
        "answer": "Tigre"
        },
        {
        "question": "Qual é o nome do maior rio do mundo?",
        "options": ["Rio Amazonas", "Rio Nilo", "Rio Yangtzé"],
        "answer": "Rio Amazonas"
        },
        {
        "question": "Qual é o nome do maior deserto do mundo?",
        "options": ["Deserto do Saara", "Deserto de Gobi", "Deserto da Arábia"],
        "answer": "Deserto do Saara"
        }
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions/<dificuldade>')
def get_questions(dificuldade):
    return jsonify(questions.get(dificuldade, []))

@app.route('/fechar_guia', methods=['POST'])
def fechar_guia():
    print("Guia fechada. Encerrando servidor...")
    os._exit(0)
    return '', 204

def abrir_navegador():
    webbrowser.open_new('http://127.0.0.1:5000/')

def encerrar_servidor(signal, frame):
    print("\nServidor encerrado. Fechando o terminal...")
    sys.exit(0)

if __name__ == '__main__':
    abrir_navegador()
    signal.signal(signal.SIGINT, encerrar_servidor)
    app.run(debug=False)