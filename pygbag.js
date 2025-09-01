// pygbag.js - Loader Pygbag
window.addEventListener('load', async () => {
    console.log('🎮 Ycrad l\'Aventurier - Chargement...');
    
    const loadingElement = document.getElementById('loading');
    
    try {
        // Configuration Pygbag
        window.pygame = {
            webAssembly: {
                onRuntimeInitialized: () => {
                    console.log('✅ WebAssembly initialisé');
                    if (loadingElement) {
                        loadingElement.style.display = 'none';
                    }
                }
            }
        };
        
        // Charger le runtime Pygbag
        await import('./pygbag/pygbag.js');
        
    } catch (error) {
        console.error('❌ Erreur de chargement:', error);
        if (loadingElement) {
            loadingElement.textContent = 'Erreur de chargement: ' + error.message;
            loadingElement.style.color = 'red';
        }
    }
});

// Gestion des erreurs globales
window.addEventListener('error', (e) => {
    console.error('Erreur globale:', e.error);
});

// Service Worker registration
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js')
        .then(() => console.log('✅ Service Worker enregistré'))
        .catch(err => console.log('❌ Service Worker failed:', err));
}