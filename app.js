/**
 * Arabica - Quranic Arabic Vocabulary App
 * Root-based learning with flashcard interface
 */

// State
let appData = null;
let cards = [];
let currentIndex = 0;
let isFlipped = false;
let history = [];
let currentPack = null;
let testDirection = 'ar-en'; // 'ar-en' or 'en-ar'
let studyMode = 'roots'; // 'roots' or 'words'

// DOM Elements
const elements = {
    // Screens
    homeScreen: document.getElementById('homeScreen'),
    practiceScreen: document.getElementById('practiceScreen'),
    completeScreen: document.getElementById('completeScreen'),

    // Home
    packList: document.getElementById('packList'),
    globalTrickyBtn: document.getElementById('globalTrickyBtn'),
    trickyCount: document.getElementById('trickyCount'),
    totalRoots: document.getElementById('totalRoots'),
    totalLearned: document.getElementById('totalLearned'),
    totalTricky: document.getElementById('totalTricky'),

    // Practice
    backBtn: document.getElementById('backBtn'),
    wordCounter: document.getElementById('wordCounter'),
    packTitle: document.getElementById('packTitle'),
    wordCard: document.getElementById('wordCard'),
    rootBadge: document.getElementById('rootBadge'),
    cardFront: document.getElementById('cardFront'),
    cardBack: document.getElementById('cardBack'),
    arabicMain: document.getElementById('arabicMain'),
    patternInfo: document.getElementById('patternInfo'),
    patternValue: document.getElementById('patternValue'),
    meaningMain: document.getElementById('meaningMain'),
    meaningCore: document.getElementById('meaningCore'),
    derivativesList: document.getElementById('derivativesList'),
    tapHint: document.getElementById('tapHint'),
    verseRef: document.getElementById('verseRef'),
    progressFill: document.getElementById('progressFill'),
    trickyBtn: document.getElementById('trickyBtn'),
    gotItBtn: document.getElementById('gotItBtn'),
    prevBtn: document.getElementById('prevBtn'),
    nextBtn: document.getElementById('nextBtn'),

    // Complete
    statTotal: document.getElementById('statTotal'),
    statGotIt: document.getElementById('statGotIt'),
    statTricky: document.getElementById('statTricky'),
    statPercent: document.getElementById('statPercent'),
    reviewTrickyBtn: document.getElementById('reviewTrickyBtn'),
    homeBtn: document.getElementById('homeBtn')
};

// Progress persistence
function getProgress() {
    const saved = localStorage.getItem('arabicaProgress');
    return saved ? JSON.parse(saved) : {};
}

function saveProgress(progress) {
    localStorage.setItem('arabicaProgress', JSON.stringify(progress));
}

function getCardKey(card) {
    return card.root;
}

function updateCardProgress(cardKey, status) {
    const progress = getProgress();
    progress[cardKey] = status;
    saveProgress(progress);
}

function getTrickyCards() {
    const progress = getProgress();
    return appData.roots.filter(root => progress[root.root] === 'tricky');
}

function getLearnedCards() {
    const progress = getProgress();
    return appData.roots.filter(root => progress[root.root] === 'got-it');
}

// Screen management
function showScreen(name) {
    document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
    document.getElementById(name + 'Screen').classList.remove('hidden');
}

// Data loading
async function loadData() {
    try {
        const response = await fetch('data/app_data.json');
        appData = await response.json();
        initializeApp();
    } catch (error) {
        console.error('Failed to load data:', error);
        document.body.innerHTML = '<div style="padding: 2rem; text-align: center;">Failed to load vocabulary data. Please refresh.</div>';
    }
}

function initializeApp() {
    renderPackList();
    updateStats();
    setupEventListeners();
}

function renderPackList() {
    const progress = getProgress();

    const packs = [
        { id: 'top_50', ...appData.packs.top_50, roots: appData.roots.slice(0, 50) },
        { id: 'top_100', ...appData.packs.top_100, roots: appData.roots.slice(0, 100) },
        { id: 'top_200', ...appData.packs.top_200, roots: appData.roots.slice(0, 200) },
        { id: 'top_500', ...appData.packs.top_500, roots: appData.roots.slice(0, 500) },
        { id: 'all', ...appData.packs.all, roots: appData.roots }
    ];

    elements.packList.innerHTML = packs.map(pack => {
        // Calculate progress
        const learned = pack.roots.filter(r => progress[r.root] === 'got-it').length;
        const progressPercent = Math.round((learned / pack.count) * 100);

        return `
            <div class="pack-card" data-pack="${pack.id}">
                <div class="pack-card-header">
                    <span class="pack-name">${pack.name}</span>
                    <span class="pack-count">${pack.count} roots</span>
                </div>
                <div class="pack-description">${pack.description}</div>
                <div class="pack-progress">
                    <div class="pack-progress-fill" style="width: ${progressPercent}%"></div>
                </div>
            </div>
        `;
    }).join('');

    // Add click handlers
    document.querySelectorAll('.pack-card').forEach(card => {
        card.addEventListener('click', () => startPack(card.dataset.pack));
    });
}

function updateStats() {
    const trickyCards = getTrickyCards();
    const learnedCards = getLearnedCards();

    elements.totalRoots.textContent = appData.roots.length;
    elements.totalLearned.textContent = learnedCards.length;
    elements.totalTricky.textContent = trickyCards.length;
    elements.trickyCount.textContent = trickyCards.length;

    if (trickyCards.length > 0) {
        elements.globalTrickyBtn.classList.remove('hidden');
    } else {
        elements.globalTrickyBtn.classList.add('hidden');
    }
}

function startPack(packId) {
    const packInfo = appData.packs[packId];
    let packRoots;

    if (packId === 'all') {
        packRoots = appData.roots;
    } else {
        const count = parseInt(packId.split('_')[1]);
        packRoots = appData.roots.slice(0, count);
    }

    currentPack = {
        id: packId,
        name: packInfo.name,
        roots: packRoots
    };

    // Filter to show only cards without 'got-it' status (unless reviewing)
    const progress = getProgress();
    cards = packRoots.filter(r => progress[r.root] !== 'got-it');

    if (cards.length === 0) {
        // All learned - review all
        cards = [...packRoots];
    }

    shuffle(cards);
    currentIndex = 0;
    history = [];

    elements.packTitle.textContent = currentPack.name;
    showScreen('practice');
    updateDisplay();
}

function startTrickyReview() {
    const trickyCards = getTrickyCards();

    if (trickyCards.length === 0) {
        alert('No tricky items to review!');
        return;
    }

    currentPack = {
        id: 'tricky',
        name: 'Tricky Review',
        roots: trickyCards
    };

    cards = [...trickyCards];
    shuffle(cards);
    currentIndex = 0;
    history = [];

    elements.packTitle.textContent = 'Reviewing Tricky Items';
    showScreen('practice');
    updateDisplay();
}

function updateDisplay() {
    if (currentIndex >= cards.length) {
        showCompletion();
        return;
    }

    const card = cards[currentIndex];
    isFlipped = false;

    // Update root badge
    elements.rootBadge.textContent = formatRoot(card.root);

    // Determine what to show based on direction
    if (testDirection === 'ar-en') {
        // Show Arabic, reveal English
        const mainDerivative = card.derivatives[0];
        elements.arabicMain.textContent = mainDerivative ? mainDerivative.lemma : card.root;
        elements.patternValue.textContent = getVerbFormLabel(mainDerivative?.verb_form);
        elements.meaningMain.textContent = card.meaning || 'meaning unavailable';
        elements.meaningCore.textContent = card.core_meaning ? `Core: ${card.core_meaning}` : '';
    } else {
        // Show English, reveal Arabic
        elements.arabicMain.textContent = card.meaning || 'meaning unavailable';
        elements.arabicMain.style.fontFamily = 'var(--font-display)';
        elements.arabicMain.style.fontSize = '1.8rem';
        elements.arabicMain.style.direction = 'ltr';
        elements.patternInfo.classList.add('hidden');

        const mainDerivative = card.derivatives[0];
        elements.meaningMain.textContent = mainDerivative ? mainDerivative.lemma : card.root;
        elements.meaningMain.style.fontFamily = 'var(--font-arabic)';
        elements.meaningMain.style.fontSize = '3rem';
        elements.meaningMain.style.direction = 'rtl';
        elements.meaningCore.textContent = '';
    }

    // Render derivatives
    renderDerivatives(card.derivatives);

    // Show example verse
    if (card.derivatives[0]?.examples?.length > 0) {
        elements.verseRef.textContent = `Example: ${card.derivatives[0].examples[0]}`;
    } else {
        elements.verseRef.textContent = '';
    }

    // Reset visual state
    elements.cardFront.classList.remove('hidden');
    elements.cardBack.classList.add('hidden');
    elements.tapHint.textContent = 'Tap to reveal';
    elements.wordCard.classList.remove('flipped');

    // Reset styles for ar-en mode
    if (testDirection === 'ar-en') {
        elements.arabicMain.style.fontFamily = 'var(--font-arabic)';
        elements.arabicMain.style.fontSize = '3.5rem';
        elements.arabicMain.style.direction = 'rtl';
        elements.patternInfo.classList.remove('hidden');
        elements.meaningMain.style.fontFamily = 'var(--font-display)';
        elements.meaningMain.style.fontSize = '1.8rem';
        elements.meaningMain.style.direction = 'ltr';
    }

    // Update counter and progress
    elements.wordCounter.textContent = `${currentIndex + 1} / ${cards.length}`;
    elements.progressFill.style.width = `${(currentIndex / cards.length) * 100}%`;
}

function formatRoot(root) {
    // Add spaces between Arabic letters
    return root.split('').join(' ');
}

function getVerbFormLabel(vf) {
    if (!vf) return '—';
    const romanNumerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];
    return `Form ${romanNumerals[vf - 1] || vf}`;
}

function renderDerivatives(derivatives) {
    if (!derivatives || derivatives.length === 0) {
        elements.derivativesList.innerHTML = '<em>No derivatives</em>';
        return;
    }

    elements.derivativesList.innerHTML = derivatives.slice(0, 5).map(d => `
        <div class="derivative-item">
            <span class="derivative-arabic">${d.lemma}</span>
            <span class="derivative-freq">${d.frequency}x</span>
        </div>
    `).join('');
}

function flipCard() {
    isFlipped = !isFlipped;

    if (isFlipped) {
        elements.cardFront.classList.add('hidden');
        elements.cardBack.classList.remove('hidden');
        elements.tapHint.textContent = 'Rate yourself';
        elements.wordCard.classList.add('flipped');
    } else {
        elements.cardFront.classList.remove('hidden');
        elements.cardBack.classList.add('hidden');
        elements.tapHint.textContent = 'Tap to reveal';
        elements.wordCard.classList.remove('flipped');
    }
}

function rate(status) {
    if (!isFlipped) {
        flipCard();
        return;
    }

    const card = cards[currentIndex];
    history.push({ index: currentIndex, card: card, previousStatus: getProgress()[card.root] });
    updateCardProgress(card.root, status);

    currentIndex++;
    updateDisplay();
}

function goBack() {
    if (history.length === 0) return;

    const last = history.pop();
    currentIndex = last.index;

    // Restore previous status
    const progress = getProgress();
    if (last.previousStatus) {
        progress[last.card.root] = last.previousStatus;
    } else {
        delete progress[last.card.root];
    }
    saveProgress(progress);

    updateDisplay();
}

function navigate(direction) {
    const newIndex = currentIndex + direction;
    if (newIndex >= 0 && newIndex < cards.length) {
        currentIndex = newIndex;
        updateDisplay();
    }
}

function showCompletion() {
    // Calculate stats for this session
    const sessionStats = { total: 0, gotIt: 0, tricky: 0 };
    const progress = getProgress();

    cards.forEach(card => {
        sessionStats.total++;
        const status = progress[card.root];
        if (status === 'got-it') sessionStats.gotIt++;
        if (status === 'tricky') sessionStats.tricky++;
    });

    elements.statTotal.textContent = sessionStats.total;
    elements.statGotIt.textContent = sessionStats.gotIt;
    elements.statTricky.textContent = sessionStats.tricky;
    elements.statPercent.textContent = `${Math.round((sessionStats.gotIt / sessionStats.total) * 100)}%`;

    // Hide review button if no tricky items
    if (sessionStats.tricky === 0) {
        elements.reviewTrickyBtn.classList.add('hidden');
    } else {
        elements.reviewTrickyBtn.classList.remove('hidden');
    }

    showScreen('complete');
}

function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
}

function goHome() {
    renderPackList();
    updateStats();
    showScreen('home');
}

function setupEventListeners() {
    // Mode toggle
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            studyMode = btn.dataset.mode;
        });
    });

    // Direction toggle
    document.querySelectorAll('.direction-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.direction-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            testDirection = btn.dataset.dir;
            localStorage.setItem('arabicaDirection', testDirection);
        });
    });

    // Load saved direction
    const savedDirection = localStorage.getItem('arabicaDirection');
    if (savedDirection) {
        testDirection = savedDirection;
        document.querySelectorAll('.direction-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.dir === savedDirection);
        });
    }

    // Global tricky review
    elements.globalTrickyBtn.addEventListener('click', startTrickyReview);

    // Practice screen
    elements.backBtn.addEventListener('click', goHome);
    elements.wordCard.addEventListener('click', flipCard);
    elements.trickyBtn.addEventListener('click', () => rate('tricky'));
    elements.gotItBtn.addEventListener('click', () => rate('got-it'));
    elements.prevBtn.addEventListener('click', goBack);
    elements.nextBtn.addEventListener('click', () => navigate(1));

    // Complete screen
    elements.reviewTrickyBtn.addEventListener('click', startTrickyReview);
    elements.homeBtn.addEventListener('click', goHome);

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (elements.practiceScreen.classList.contains('hidden')) return;

        if (e.code === 'Space') {
            e.preventDefault();
            flipCard();
        } else if (e.code === 'ArrowLeft' || e.key === '1') {
            e.preventDefault();
            rate('tricky');
        } else if (e.code === 'ArrowRight' || e.key === '2') {
            e.preventDefault();
            rate('got-it');
        } else if (e.code === 'Backspace' || e.key === 'b') {
            e.preventDefault();
            goBack();
        }
    });
}

// Initialize
loadData();
