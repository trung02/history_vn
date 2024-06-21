document.addEventListener('DOMContentLoaded', () => {
    const questions = [
        {
            question: "What is the capital of France?",
            answers: ["Berlin", "Madrid", "Paris", "Rome"],
            correct: "Paris",
            explanation: "Paris is the capital and most populous city of France."
        },
        {
            question: "What is 2 + 2?",
            answers: ["3", "4", "5", "6"],
            correct: "4",
            explanation: "2 + 2 equals 4."
        },
        {
            question: "Who wrote 'To Kill a Mockingbird'?",
            answers: ["Harper Lee", "J.K. Rowling", "Ernest Hemingway", "Mark Twain"],
            correct: "Harper Lee",
            explanation: "'To Kill a Mockingbird' was written by Harper Lee and published in 1960."
        },
        // Add more questions here...
    ];

    // Shuffle array function
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    // Shuffle questions and answers
    shuffle(questions);
    questions.forEach(q => shuffle(q.answers));

    const questionsContainer = document.getElementById('questions-container');

    questions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';
        questionDiv.innerHTML = `
            <p>${index + 1}. ${q.question} <span id="result${index}"></span></p>
            ${q.answers.map(answer => `
                <div class="answer">
                    <input type="radio" id="answer${index}_${answer}" name="answer${index}" value="${answer}">
                    <label for="answer${index}_${answer}">${answer}</label>
                </div>
            `).join('')}
            <div class="explanation-btn" id="explanation-btn${index}" type="text">Explanation>></div>
            <div class="explanation" id="explanation${index}">
                <p><strong>Correct answer: ${q.correct}</strong>. ${q.explanation}</p>
            </div>
        `;
        questionsContainer.appendChild(questionDiv);
    });

    document.getElementById('submit-btn').addEventListener('click', () => {
        let correctAnswers = 0;
        questions.forEach((q, index) => {
            const selectedAnswer = document.querySelector(`input[name="answer${index}"]:checked`);
            const resultSpan = document.getElementById(`result${index}`);
            const explanationBtn = document.getElementById(`explanation-btn${index}`);
            const explanationDiv = document.getElementById(`explanation${index}`);

            // Reset previous classes
            resultSpan.textContent = '';
            resultSpan.classList.remove('correct', 'incorrect');
            explanationDiv.classList.remove('correct-bg', 'incorrect-bg');

            if (selectedAnswer) {
                if (selectedAnswer.value === q.correct) {
                    correctAnswers++;
                    resultSpan.textContent = "Correct";
                    resultSpan.classList.add('correct');
                    explanationDiv.classList.add('correct-bg');
                } else {
                    resultSpan.textContent = "Incorrect";
                    resultSpan.classList.add('incorrect');
                    explanationDiv.classList.add('incorrect-bg');
                }
                explanationBtn.style.display = "block";
            }
        });
        const resultDiv = document.getElementById('result');
        resultDiv.textContent = `You got ${correctAnswers} out of ${questions.length} correct!`;
    });

    questionsContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('explanation-btn')) {
            const index = event.target.id.replace('explanation-btn', '');
            const explanationDiv = document.getElementById(`explanation${index}`);
            explanationDiv.style.display = explanationDiv.style.display === 'block' ? 'none' : 'block';
        }
    });
});