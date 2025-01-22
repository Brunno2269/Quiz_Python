document.addEventListener('DOMContentLoaded', function () {
    const dificuldadeContainer = document.getElementById('dificuldade');
    const quizContainer = document.getElementById('quiz');
    const questionContainer = document.getElementById('question-container');
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const submitButton = document.getElementById('submit');
    const resultsContainer = document.getElementById('results');

    let questions = [];
    let currentQuestionIndex = 0;
    let userAnswers = [];
    let startTime;
    let responseTimes = [];

    // Seleção de dificuldade
    document.getElementById('facil').addEventListener('click', () => loadQuestions('facil'));
    document.getElementById('medio').addEventListener('click', () => loadQuestions('medio'));
    document.getElementById('dificil').addEventListener('click', () => loadQuestions('dificil'));

    // Carrega as perguntas do backend
    function loadQuestions(dificuldade) {
        fetch(`/questions/${dificuldade}`)
            .then(response => response.json())
            .then(data => {
                questions = data;
                userAnswers = new Array(questions.length).fill(null);
                responseTimes = new Array(questions.length).fill(0);
                dificuldadeContainer.classList.add('hidden');
                quizContainer.classList.remove('hidden');
                startQuestionTimer();
                displayQuestion(currentQuestionIndex);
            });
    }

    // Exibe a pergunta atual
    function displayQuestion(index) {
        const question = questions[index];
        const options = question.options.map((option, i) => `
            <label>
                <input type="radio" name="question${index}" value="${option}" ${userAnswers[index] === option ? 'checked' : ''}>
                ${option}
            </label>
        `).join('');

        questionContainer.innerHTML = `
            <div class="question">
                <h3>${index + 1}. ${question.question}</h3>
                <div class="options">${options}</div>
            </div>
        `;

        prevButton.disabled = index === 0;
        nextButton.disabled = index === questions.length - 1;
    }

    // Inicia o timer para a pergunta atual
    function startQuestionTimer() {
        startTime = Date.now();
    }

    // Salva o tempo de resposta e a resposta do usuário
    function saveAnswer(index) {
        const selectedOption = document.querySelector(`input[name="question${index}"]:checked`);
        if (selectedOption) {
            userAnswers[index] = selectedOption.value;
            responseTimes[index] = (Date.now() - startTime) / 1000; // Tempo em segundos
        }
    }

    // Navega para a pergunta anterior
    prevButton.addEventListener('click', function () {
        saveAnswer(currentQuestionIndex);
        currentQuestionIndex--;
        startQuestionTimer();
        displayQuestion(currentQuestionIndex);
    });

    // Navega para a próxima pergunta
    nextButton.addEventListener('click', function () {
        saveAnswer(currentQuestionIndex);
        currentQuestionIndex++;
        startQuestionTimer();
        displayQuestion(currentQuestionIndex);
    });

    // Verifica as respostas ao enviar
    submitButton.addEventListener('click', function () {
        saveAnswer(currentQuestionIndex);
        let score = 0;

        questions.forEach((question, index) => {
            if (userAnswers[index] === question.answer) {
                score++;
            }
        });

        const totalTime = responseTimes.reduce((acc, time) => acc + time, 0).toFixed(2);
        resultsContainer.innerHTML = `Você acertou ${score} de ${questions.length} perguntas!<br>Tempo total: ${totalTime} segundos.`;
    });

    // Notifica o servidor quando a guia é fechada
    window.addEventListener('beforeunload', function () {
        fetch('/fechar_guia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
        });
    });
});