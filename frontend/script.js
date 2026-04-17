// API Configuration
const API_BASE = 'http://localhost:5000/api';

// DOM Elements
const targetInput = document.getElementById('targetInput');
const portInput = document.getElementById('portInput');
const durationInput = document.getElementById('durationInput');
const attackCards = document.querySelectorAll('.attack-card');
const stopBtn = document.getElementById('stopAttackBtn');
const clearBtn = document.getElementById('clearBtn');
const clearConsoleBtn = document.getElementById('clearConsole');
const consoleOutput = document.getElementById('consoleOutput');
const mascotMessage = document.getElementById('mascotMessage');
const packetsSent = document.getElementById('packetsSent');
const bytesSent = document.getElementById('bytesSent');
const currentTarget = document.getElementById('currentTarget');
const attackStatus = document.getElementById('attackStatus');

// State
let activeAttack = null;
let statsInterval = null;

// Console Functions
function addConsoleMessage(message, type = 'info') {
    const line = document.createElement('div');
    line.className = `console-line ${type}`;
    line.textContent = `> ${new Date().toLocaleTimeString()} - ${message}`;
    consoleOutput.appendChild(line);
    consoleOutput.scrollTop = consoleOutput.scrollHeight;
    
    // Limit console lines
    if (consoleOutput.children.length > 50) {
        consoleOutput.removeChild(consoleOutput.children[0]);
    }
}

function clearConsole() {
    consoleOutput.innerHTML = '';
    addConsoleMessage('Console cleared');
}

// Mascot Messages
const mascotMessages = {
    idle: ['Pilih senjata digitalmu, El Manco-sama! >_<', 'Menunggu perintah... nyan~', 'Siap melindungi goa!', 'Semua sistem normal!'],
    attack: ['Serangan dimulai! Ganbatte!', 'Koneksi terputus-putus... Ureshii~', 'Mengirim paket dengan kekuatan penuh!', 'Target dalam jangkauan!'],
    stop: ['Serangan dihentikan. Otsukaresama!', 'Kembali ke mode siaga...', 'Misi selesai!', 'Menunggu perintah selanjutnya...']
};

function updateMascotMessage(type) {
    const messages = mascotMessages[type];
    const randomMsg = messages[Math.floor(Math.random() * messages.length)];
    mascotMessage.textContent = randomMsg;
}

// Stats Update
async function updateStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const stats = await response.json();
        
        packetsSent.textContent = stats.packets_sent.toLocaleString();
        
        const mb = stats.bytes_sent / (1024 * 1024);
        bytesSent.textContent = mb.toFixed(2) + ' MB';
        
        currentTarget.textContent = stats.current_target || '-';
        attackStatus.textContent = stats.attack_type ? 
            stats.attack_type.toUpperCase() : 'IDLE';
        
        if (!stats.attack_type) {
            attackStatus.style.color = '#888';
            activeAttack = null;
            attackCards.forEach(card => card.classList.remove('active'));
        } else {
            attackStatus.style.color = '#ff0040';
        }
    } catch (error) {
        console.error('Stats error:', error);
    }
}

// Attack Functions
async function startAttack(type) {
    const target = targetInput.value.trim();
    const port = parseInt(portInput.value) || 80;
    const duration = parseInt(durationInput.value) || 60;
    
    if (!target) {
        addConsoleMessage('Error: Target tidak boleh kosong!', 'error');
        updateMascotMessage('idle');
        return;
    }
    
    // Stop any ongoing attack
    if (activeAttack) {
        await stopAttack();
    }
    
    try {
        const response = await fetch(`${API_BASE}/attack/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: type,
                target: target,
                port: port,
                duration: duration
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'attack_started') {
            activeAttack = type;
            
            // Update UI
            attackCards.forEach(card => {
                if (card.dataset.type === type) {
                    card.classList.add('active');
                }
            });
            
            addConsoleMessage(`Attack ${type.toUpperCase()} dimulai ke ${target}:${port}`, 'success');
            addConsoleMessage(`Durasi: ${duration} detik`, 'warning');
            updateMascotMessage('attack');
            
            // Start stats polling
            if (statsInterval) clearInterval(statsInterval);
            statsInterval = setInterval(updateStats, 1000);
        }
    } catch (error) {
        addConsoleMessage(`Error: ${error.message}`, 'error');
    }
}

async function stopAttack() {
    try {
        const response = await fetch(`${API_BASE}/attack/stop`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.status === 'attack_stopped') {
            activeAttack = null;
            attackCards.forEach(card => card.classList.remove('active'));
            addConsoleMessage('Attack dihentikan', 'warning');
            updateMascotMessage('stop');
            
            if (statsInterval) {
                clearInterval(statsInterval);
                statsInterval = null;
            }
            
            // Final stats update
            await updateStats();
        }
    } catch (error) {
        addConsoleMessage(`Error stopping attack: ${error.message}`, 'error');
    }
}

// Event Listeners
attackCards.forEach(card => {
    card.addEventListener('click', () => {
        const type = card.dataset.type;
        
        if (activeAttack === type) {
            // If same attack type, stop it
            stopAttack();
        } else {
            startAttack(type);
        }
    });
});

stopBtn.addEventListener('click', stopAttack);

clearBtn.addEventListener('click', () => {
    targetInput.value = '';
    portInput.value = '80';
    durationInput.value = '60';
    addConsoleMessage('Form direset', 'info');
});

clearConsoleBtn.addEventListener('click', clearConsole);

// Initialize
addConsoleMessage('Sistem El Cienco online...');
addConsoleMessage('7 Fitur DDoS siap digunakan');
addConsoleMessage('Backend API aktif di port 5000');

// Start stats polling
statsInterval = setInterval(updateStats, 1000);
updateMascotMessage('idle');

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to start HTTP flood (default)
    if (e.ctrlKey && e.key === 'Enter') {
        startAttack('http');
    }
    // Escape to stop attack
    if (e.key === 'Escape') {
        stopAttack();
    }
});

// Prevent form submission
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    });
});
