// Dados do teste
const phrases = [
    "A tecnologia transforma a forma como trabalhamos todos os dias.",
    "A análise de dados é essencial para decisões estratégicas.",
    "Velocidade e precisão são fundamentais em ambientes corporativos."
];

let currentPhase = 0;
let startTime = null;
let results = [];
let timerInterval = null;

// Elementos DOM
let welcomeScreen;
let phaseScreen;
let finalScreen;
let startBtn;
let phraseText;
let inputText;
let finishPhaseBtn;
let currentPhaseSpan;
let progressFill;
let phaseProgress;
let timeDisplay;
let wpmDisplay;
let accuracyDisplay;
let backBtn;

/**
 * Inicializa o teste quando o DOM está pronto
 */
function init() {
    // Obter elementos do DOM
    welcomeScreen = document.getElementById('welcome-screen');
    phaseScreen = document.getElementById('phase-screen');
    finalScreen = document.getElementById('final-screen');
    startBtn = document.getElementById('start-btn');
    phraseText = document.getElementById('phrase-text');
    inputText = document.getElementById('input-text');
    finishPhaseBtn = document.getElementById('finish-phase-btn');
    currentPhaseSpan = document.getElementById('current-phase');
    progressFill = document.getElementById('progress-fill');
    phaseProgress = document.getElementById('phase-progress');
    timeDisplay = document.getElementById('time-display');
    wpmDisplay = document.getElementById('wpm-display');
    accuracyDisplay = document.getElementById('accuracy-display');
    backBtn = document.getElementById('back-btn');

    // Configurar event listeners
    setupEventListeners();
}

/**
 * Configura todos os event listeners
 */
function setupEventListeners() {
    startBtn.addEventListener('click', startTest);
    finishPhaseBtn.addEventListener('click', finishPhase);
    backBtn.addEventListener('click', () => window.location.href = '/');
    
    // Bloquear copiar, colar e cortar
    inputText.addEventListener('copy', (e) => e.preventDefault());
    inputText.addEventListener('paste', (e) => e.preventDefault());
    inputText.addEventListener('cut', (e) => e.preventDefault());

    // Digitação
    inputText.addEventListener('input', () => {
        if (!startTime) {
            startTime = Date.now();
            timerInterval = setInterval(updateMetrics, 100);
        }
        finishPhaseBtn.disabled = inputText.value.trim() === '';
        updateMetrics();
    });
}

/**
 * Inicia o teste
 */
function startTest() {
    welcomeScreen.classList.add('hidden');
    phaseScreen.classList.remove('hidden');
    showPhase(0);
}

/**
 * Exibe a tela da fase específica
 */
function showPhase(phaseIndex) {
    currentPhase = phaseIndex;
    currentPhaseSpan.textContent = phaseIndex + 1;
    const progressPercent = ((phaseIndex + 1) / 3) * 100;
    progressFill.style.width = `${progressPercent}%`;
    phaseProgress.textContent = `${Math.round(progressPercent)}%`;

    phraseText.textContent = phrases[phaseIndex];
    inputText.value = '';
    inputText.focus();
    finishPhaseBtn.disabled = true;
    startTime = null;
    clearInterval(timerInterval);
    updateMetrics();
}

/**
 * Finaliza a fase atual e passa para a próxima
 */
function finishPhase() {
    const endTime = Date.now();
    const timeSeconds = (endTime - startTime) / 1000;
    const typedText = inputText.value;
    const originalText = phrases[currentPhase];
    const accuracy = calculateAccuracy(typedText, originalText);
    const wpm = calculateWPM(typedText, timeSeconds);

    results.push({
        phase: currentPhase + 1,
        originalPhrase: originalText,
        typedText: typedText,
        timeSeconds: timeSeconds.toFixed(1),
        wpm: wpm.toFixed(1),
        accuracy: accuracy.toFixed(1)
    });

    clearInterval(timerInterval);

    if (currentPhase < 2) {
        showPhase(currentPhase + 1);
    } else {
        showFinal();
    }
}

/**
 * Calcula a acurácia em percentual
 */
function calculateAccuracy(typed, original) {
    let correct = 0;
    const minLength = Math.min(typed.length, original.length);
    for (let i = 0; i < minLength; i++) {
        if (typed[i] === original[i]) correct++;
    }
    return (correct / original.length) * 100;
}

/**
 * Calcula WPM (Palavras por Minuto)
 */
function calculateWPM(typed, timeSeconds) {
    const words = typed.length / 5; // 5 caracteres por palavra
    const minutes = timeSeconds / 60;
    return minutes > 0 ? words / minutes : 0;
}

/**
 * Atualiza as métricas em tempo real
 */
function updateMetrics() {
    if (!startTime) {
        timeDisplay.textContent = '0.0s';
        wpmDisplay.textContent = '0';
        accuracyDisplay.textContent = '0%';
        return;
    }

    const elapsed = (Date.now() - startTime) / 1000;
    timeDisplay.textContent = `${elapsed.toFixed(1)}s`;

    const typed = inputText.value;
    const wpm = calculateWPM(typed, elapsed);
    wpmDisplay.textContent = Math.round(wpm);

    const accuracy = calculateAccuracy(typed, phrases[currentPhase]);
    accuracyDisplay.textContent = `${Math.round(accuracy)}%`;
}

/**
 * Exibe a tela final
 */
function showFinal() {
    phaseScreen.classList.add('hidden');
    finalScreen.classList.remove('hidden');
    
    // Enviar dados ao servidor
    saveResults();
}

/**
 * Salva os resultados no servidor
 */
function saveResults() {
    // Obter token CSRF
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    
    if (!csrfToken) {
        console.error('CSRF token não encontrado');
    }
    
    console.log('Enviando resultados:', results);
    
    fetch('/app/api/save-typing-test/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(results)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Resposta do servidor:', data);
        if (data.status === 'success') {
            console.log('Resultados salvos com sucesso:', data);
            // Redirecionar para dashboard após 2 segundos
            setTimeout(() => {
                window.location.href = '/app/';
            }, 2000);
        } else {
            console.error('Erro ao salvar:', data.message);
            alert('Erro ao salvar resultados: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        alert('Erro ao salvar resultados. Tente novamente.');
    });
}

/**
 * Inicializa quando o DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', init);
