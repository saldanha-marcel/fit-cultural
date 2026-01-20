/**
 * Teste de Avaliação de Perfil Comportamental
 * Baseado no modelo dos 4 Quadrantes de Ned Herrmann
 * 25 questões - 5 para cada quadrante
 */

const QUESTIONS = [
    // Quadrante A - Pensador Analítico (Lógico)
    {
        id: 1,
        quadrant: 'A',
        text: 'Eu prefiro analisar os dados antes de tomar decisões'
    },
    {
        id: 2,
        quadrant: 'A',
        text: 'Gosto de entender o "por quê" das coisas em profundidade'
    },
    {
        id: 3,
        quadrant: 'A',
        text: 'Sou uma pessoa que segue a lógica e a razão'
    },
    {
        id: 4,
        quadrant: 'A',
        text: 'Prefiro precisão e fatos ao invés de opiniões'
    },
    {
        id: 5,
        quadrant: 'A',
        text: 'Gosto de resolver problemas complexos de forma metódica'
    },
    
    // Quadrante B - Pensador Prático (Administrativo)
    {
        id: 6,
        quadrant: 'B',
        text: 'Eu sou organizado e gosto de seguir procedimentos estabelecidos'
    },
    {
        id: 7,
        quadrant: 'B',
        text: 'Prefiro planejar e executar tarefas de forma estruturada'
    },
    {
        id: 8,
        quadrant: 'B',
        text: 'Gosto de resultados práticos e mensuráveis'
    },
    {
        id: 9,
        quadrant: 'B',
        text: 'Sou confiável e cumpro com as responsabilidades assumidas'
    },
    {
        id: 10,
        quadrant: 'B',
        text: 'Prefiro trabalhar dentro de regras e regulamentações claras'
    },
    
    // Quadrante C - Pensador Relacional (Interpessoal)
    {
        id: 11,
        quadrant: 'C',
        text: 'Eu valoro o trabalho em equipe e a colaboração'
    },
    {
        id: 12,
        quadrant: 'C',
        text: 'Gosto de ouvir e compreender os sentimentos das pessoas'
    },
    {
        id: 13,
        quadrant: 'C',
        text: 'Sou empático e me importo com o bem-estar dos outros'
    },
    {
        id: 14,
        quadrant: 'C',
        text: 'Prefiro ambientes harmoniosos e cooperativos'
    },
    {
        id: 15,
        quadrant: 'C',
        text: 'Gosto de construir relacionamentos sólidos e duradouros'
    },
    
    // Quadrante D - Pensador Inovador (Criativo)
    {
        id: 16,
        quadrant: 'D',
        text: 'Eu sou criativo e gosto de explorar novas ideias'
    },
    {
        id: 17,
        quadrant: 'D',
        text: 'Prefiro desafiar o status quo e propor mudanças'
    },
    {
        id: 18,
        quadrant: 'D',
        text: 'Gosto de trabalhar em projetos inovadores e estimulantes'
    },
    {
        id: 19,
        quadrant: 'D',
        text: 'Sou entusiasta com novas possibilidades e oportunidades'
    },
    {
        id: 20,
        quadrant: 'D',
        text: 'Prefiro experimentar e aprender com a prática'
    }
];

// Adicionar 5 perguntas misturadas para melhor distribuição
const ADDITIONAL_QUESTIONS = [
    {
        id: 21,
        quadrant: 'A',
        text: 'Gosto de questionar e analisar criticamente as informações'
    },
    {
        id: 22,
        quadrant: 'B',
        text: 'Sou eficiente na execução de tarefas e cumpro prazos'
    },
    {
        id: 23,
        quadrant: 'C',
        text: 'Eu sou alguém que inspira confiança nos outros'
    },
    {
        id: 24,
        quadrant: 'D',
        text: 'Gosto de aprender coisas novas e explorar diferentes abordagens'
    },
    {
        id: 25,
        quadrant: 'A',
        text: 'Prefiro ter informações completas antes de agir'
    }
];

const ALL_QUESTIONS = [...QUESTIONS, ...ADDITIONAL_QUESTIONS];

const QUADRANT_INFO = {
    A: {
        name: 'Pensador Analítico',
        color: '#4A90E2',
        description: 'Lógico, Crítico, Analítico'
    },
    B: {
        name: 'Pensador Prático',
        color: '#50E3C2',
        description: 'Organizado, Administrativo, Estruturado'
    },
    C: {
        name: 'Pensador Relacional',
        color: '#F5A623',
        description: 'Empático, Colaborativo, Interpessoal'
    },
    D: {
        name: 'Pensador Inovador',
        color: '#BD10E0',
        description: 'Criativo, Inovador, Explorador'
    }
};

let currentStep = 0;
let answers = {};
let allAnswers = [];

// Elementos DOM
let wizardContainer;
let welcomeScreen;
let questionsScreen;
let finalScreen;
let progressFill;
let progressText;
let progressPercent;
let startBtn;
let prevBtn;
let nextBtn;
let submitBtn;
let questionsContainer;
let backBtn;

/**
 * Inicializa o teste
 */
function init() {
    // Obter elementos do DOM
    wizardContainer = document.getElementById('wizard-container');
    welcomeScreen = document.getElementById('instructions-screen');
    questionsScreen = document.getElementById('questions-screen');
    finalScreen = document.getElementById('final-screen');
    progressFill = document.getElementById('progress-fill');
    progressText = document.getElementById('progress-text');
    progressPercent = document.getElementById('progress-percent');
    startBtn = document.getElementById('start-btn');
    prevBtn = document.getElementById('prev-btn');
    nextBtn = document.getElementById('next-btn');
    submitBtn = document.getElementById('submit-btn');
    questionsContainer = document.getElementById('questions-container');
    backBtn = document.getElementById('back-btn-final');

    // Event listeners
    startBtn.addEventListener('click', startTest);
    prevBtn.addEventListener('click', previousStep);
    nextBtn.addEventListener('click', nextStep);
    submitBtn.addEventListener('click', submitTest);
    backBtn.addEventListener('click', () => window.history.back());

    // Inicializar respostas
    answers = {};
    ALL_QUESTIONS.forEach(q => {
        answers[q.id] = null;
    });
}

/**
 * Inicia o teste
 */
function startTest() {
    welcomeScreen.classList.add('hidden');
    questionsScreen.classList.remove('hidden');
    currentStep = 0;
    renderQuestions();
}

/**
 * Renderiza as perguntas do passo atual
 */
function renderQuestions() {
    // Calcular perguntas por página (5 perguntas)
    const questionsPerPage = 5;
    const startIdx = currentStep * questionsPerPage;
    const endIdx = startIdx + questionsPerPage;
    const pageQuestions = ALL_QUESTIONS.slice(startIdx, endIdx);

    // Atualizar progresso
    const progress = ((currentStep + 1) / 5) * 100;
    progressFill.style.width = `${progress}%`;
    progressText.textContent = `Passo ${currentStep + 1} de 5`;

    progressPercent.textContent = `${Math.round(progress)}%`;

    // Limpar container
    questionsContainer.innerHTML = '';

    // Renderizar perguntas
    pageQuestions.forEach((question) => {
        const questionEl = createQuestionElement(question);
        questionsContainer.appendChild(questionEl);
    });

    // Atualizar botões
    prevBtn.disabled = currentStep === 0;
    nextBtn.style.display = currentStep < 4 ? 'flex' : 'none';
    submitBtn.style.display = currentStep === 4 ? 'flex' : 'none';
}

/**
 * Cria um elemento de pergunta
 */
function createQuestionElement(question) {
    const div = document.createElement('div');
    div.className = 'question-item';
    div.innerHTML = `
        <div class="question-label">${question.text}</div>
        <div class="scale-options">
            <div class="scale-option">
                <input type="radio" id="q${question.id}_1" name="q${question.id}" value="1" 
                    ${answers[question.id] === 1 ? 'checked' : ''} 
                    onchange="updateAnswer(${question.id}, 1)">
                <label for="q${question.id}_1">
                    <div class="scale-label">Discordo</div>
                </label>
            </div>
            <div class="scale-option">
                <input type="radio" id="q${question.id}_2" name="q${question.id}" value="2"
                    ${answers[question.id] === 2 ? 'checked' : ''}
                    onchange="updateAnswer(${question.id}, 2)">
                <label for="q${question.id}_2">
                    <div class="scale-label">Discordo Um Pouco</div>
                </label>
            </div>
            <div class="scale-option">
                <input type="radio" id="q${question.id}_3" name="q${question.id}" value="3"
                    ${answers[question.id] === 3 ? 'checked' : ''}
                    onchange="updateAnswer(${question.id}, 3)">
                <label for="q${question.id}_3">
                    <div class="scale-label">Neutro</div>
                </label>
            </div>
            <div class="scale-option">
                <input type="radio" id="q${question.id}_4" name="q${question.id}" value="4"
                    ${answers[question.id] === 4 ? 'checked' : ''}
                    onchange="updateAnswer(${question.id}, 4)">
                <label for="q${question.id}_4">
                    <div class="scale-label">Concordo</div>
                </label>
            </div>
            <div class="scale-option">
                <input type="radio" id="q${question.id}_5" name="q${question.id}" value="5"
                    ${answers[question.id] === 5 ? 'checked' : ''}
                    onchange="updateAnswer(${question.id}, 5)">
                <label for="q${question.id}_5">
                    <div class="scale-label">Concordo Totalmente</div>
                </label>
            </div>
        </div>
    `;
    return div;
}

/**
 * Atualiza uma resposta
 */
function updateAnswer(questionId, value) {
    answers[questionId] = value;
}

/**
 * Vai para o passo anterior
 */
function previousStep() {
    if (currentStep > 0) {
        currentStep--;
        renderQuestions();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

/**
 * Vai para o próximo passo
 */
function nextStep() {
    // Validar se todas as perguntas foram respondidas
    const questionsPerPage = 5;
    const startIdx = currentStep * questionsPerPage;
    const endIdx = startIdx + questionsPerPage;
    const pageQuestions = ALL_QUESTIONS.slice(startIdx, endIdx);

    const allAnswered = pageQuestions.every(q => answers[q.id] !== null);

    if (!allAnswered) {
        alert('Por favor, responda todas as perguntas antes de continuar.');
        return;
    }

    if (currentStep < 4) {
        currentStep++;
        renderQuestions();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

/**
 * Submete o teste e calcula os resultados
 */
function submitTest() {
    // Validar se todas as perguntas foram respondidas
    const allAnswered = ALL_QUESTIONS.every(q => answers[q.id] !== null);

    if (!allAnswered) {
        alert('Por favor, responda todas as perguntas antes de finalizar.');
        return;
    }

    // Calcular scores
    const scores = calculateScores();
    
    // Preparar dados para salvar
    allAnswers = ALL_QUESTIONS.map(q => ({
        questionId: q.id,
        quadrant: q.quadrant,
        answer: answers[q.id]
    }));

    // Mostrar resultados
    showResults(scores);
    
    // Salvar no servidor
    saveResults(scores);
}

/**
 * Calcula os scores dos quadrantes
 */
function calculateScores() {
    const scores = {
        A: 0,
        B: 0,
        C: 0,
        D: 0
    };

    // Somar as respostas por quadrante
    ALL_QUESTIONS.forEach(question => {
        const answer = answers[question.id];
        if (answer !== null) {
            scores[question.quadrant] += answer;
        }
    });

    // Normalizar para escala 0-100
    // Cada quadrante tem um número diferente de questões
    Object.keys(scores).forEach(quadrant => {
        const quadrantCount = ALL_QUESTIONS.filter(q => q.quadrant === quadrant).length;
        const maxScore = quadrantCount * 5; // Máximo possível (5 = escala máxima)
        scores[quadrant] = Math.round((scores[quadrant] / maxScore) * 100);
    });

    // Encontrar quadrante dominante
    const dominant = Object.keys(scores).reduce((a, b) => 
        scores[a] > scores[b] ? a : b
    );
    scores.dominant = dominant;

    return scores;
}

/**
 * Mostra os resultados
 */
function showResults(scores) {
    questionsScreen.classList.add('hidden');
    finalScreen.classList.remove('hidden');
}

/**
 * Salva os resultados no servidor
 */
function saveResults(scores) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    fetch('/app/api/save-behavioral-test/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            answers: allAnswers,
            scores: {
                A: scores.A,
                B: scores.B,
                C: scores.C,
                D: scores.D,
                dominant: scores.dominant
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Resultados salvos com sucesso:', data);
        } else {
            console.error('Erro ao salvar:', data.message);
        }
    })
    .catch(error => console.error('Erro na requisição:', error));
}

/**
 * Inicializa quando o DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', init);
