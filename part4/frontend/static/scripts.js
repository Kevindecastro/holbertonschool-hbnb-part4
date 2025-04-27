/**
 * HBnB - Script principal
 * Gère l'authentification, les lieux et les avis
 */

// ==============================================
// CONSTANTES ET VARIABLES GLOBALES
// ==============================================
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';
const DEFAULT_PLACE_IMAGE = '../static/images/default-place.jpg';

// ==============================================
// INITIALISATION DE LA PAGE
// ==============================================

/**
 * Initialise la page quand le DOM est chargé
 * - Vérifie l'authentification
 * - Initialise les composants de la page
 */
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    initPageComponents();
});

/**
 * Initialise les composants en fonction de la page courante
 * - Gère l'authentification
 * - Initialise les composants spécifiques à chaque page
 */
function initPageComponents() {
    // Gestion de l'authentification
    initAuthComponents();
    
    // Page spécifique: Liste des lieux
    if (document.getElementById('places-list')) {
        initHomePage();
    }
    
    // Page spécifique: Détails d'un lieu
    if (document.getElementById('place-details')) {
        initPlaceDetailsPage();
    }
    
    // Page spécifique: Ajout d'un avis
    if (document.getElementById('review-form')) {
        initReviewPage();
    }
}

// ==============================================
// FONCTIONS D'INITIALISATION DES PAGES
// ==============================================

/**
 * Initialise les composants de la page d'accueil
 * - Configure le filtre par prix
 * - Charge la liste des lieux
 */
function initHomePage() {
    setupPriceFilter();
    fetchPlaces(getCookie('token'));
}

/**
 * Initialise les composants de la page de détails
 * - Charge les détails du lieu
 * - Configure le formulaire d'avis
 */
function initPlaceDetailsPage() {
    loadPlaceDetails();
    
    const reviewForm = document.getElementById('review-form-place');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitReview(e, 'review-form-place');
        });
    }
}

/**
 * Initialise les composants de la page d'avis
 * - Charge les infos du lieu pour l'avis
 * - Configure le formulaire d'avis
 */
function initReviewPage() {
    loadPlaceInfoForReview();
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitReview(e, 'review-form');
        });
    }
}

// ==============================================
// GESTION DE L'AUTHENTIFICATION
// ==============================================

/**
 * Initialise les composants d'authentification
 * - Configure les écouteurs d'événements pour:
 *   - Le formulaire de connexion
 *   - Le lien de déconnexion
 */
function initAuthComponents() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', handleLogout);
    }
}

/**
 * Gère la soumission du formulaire de connexion
 * @param {Event} event - Événement de soumission
 * - Envoie les identifiants à l'API
 * - Stocke le token JWT dans un cookie si succès
 * - Met à jour l'interface utilisateur
 * - Redirige vers la page d'accueil
 */
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            setAuthCookie(data.access_token);
            setAuthUI(true);
            redirectToHome();
        } else {
            showError('Login failed. Please check your credentials.');
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('An error occurred during login.');
    }
}

/**
 * Gère la déconnexion de l'utilisateur
 * - Supprime le cookie d'authentification
 * - Met à jour l'interface utilisateur
 * - Redirige vers la page d'accueil
 */
function handleLogout() {
    clearAuthCookie();
    setAuthUI(false);
    redirectToHome();
}

/**
 * Vérifie l'état d'authentification
 * @returns {boolean} True si l'utilisateur est connecté
 * - Vérifie la présence du token dans les cookies
 * - Met à jour l'interface en conséquence
 */
function checkAuthentication() {
    const token = getCookie('token');
    setAuthUI(!!token);
    return !!token;
}

/**
 * Met à jour l'interface en fonction de l'état d'authentification
 * @param {boolean} isLoggedIn - État de connexion
 * - Affiche/masque les liens login/logout
 * - Affiche/masque les formulaires d'avis
 */
function setAuthUI(isLoggedIn) {
    // Gestion des liens login/logout
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    
    if (loginLink && logoutLink) {
        loginLink.style.display = isLoggedIn ? 'none' : 'block';
        logoutLink.style.display = isLoggedIn ? 'block' : 'none';
    }
    
    // Gestion des formulaires d'avis
    const loginPrompt = document.querySelector('.login-prompt');
    const reviewForm = document.getElementById('review-form-place');
    
    if (loginPrompt && reviewForm) {
        loginPrompt.style.display = isLoggedIn ? 'none' : 'block';
        reviewForm.style.display = isLoggedIn ? 'block' : 'none';
    }
}

// ==============================================
// GESTION DES LIEUX
// ==============================================

/**
 * Récupère et affiche la liste des lieux
 * @param {string} token - Token d'authentification
 * - Effectue une requête GET à l'API
 * - Affiche les lieux ou un message d'erreur
 */
async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            showFeedback('Failed to load places. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        showFeedback('Failed to load places. Please try again.', 'error');
    }
}

/**
 * Affiche la liste des lieux dans le DOM
 * @param {Array} places - Liste des lieux à afficher
 * - Crée des cartes pour chaque lieu
 * - Affiche un message si aucun lieu n'est trouvé
 * - Utilise une image par défaut si l'URL de l'image est manquante
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '';
    
    if (places.length === 0) {
        placesList.innerHTML = '<p class="no-results">No places found.</p>';
        return;
    }
    
    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <img src="${place.image_url || DEFAULT_PLACE_IMAGE}" 
                 alt="${place.name}" 
                 class="place-image">
            <div class="place-info">
                <h3 class="place-title">${place.name}</h3>
                <p class="place-price">$${place.price_by_night}/night</p>
                <p class="place-description">
                    ${place.description || 'No description available'}
                </p>
                <button onclick="goToDetails('${place.id}')" 
                        class="details-button">
                    View Details
                </button>
            </div>
        `;
        placesList.appendChild(card);
    });
}

/**
 * Configure le filtre par prix
 * - Écoute les changements sur le sélecteur de prix
 * - Filtre les lieux en fonction du prix maximum sélectionné
 * - Recharge la liste des lieux filtrés
 */
function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;
    
    filter.addEventListener('change', async () => {
        const priceLimit = filter.value;
        const token = getCookie('token');
        
        try {
            const response = await fetch(`${API_BASE_URL}/places`, {
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            });
            
            if (response.ok) {
                const places = await response.json();
                const filtered = priceLimit === 'all' 
                    ? places 
                    : places.filter(p => p.price_by_night <= parseInt(priceLimit));
                displayPlaces(filtered);
            }
        } catch (error) {
            console.error('Filter error:', error);
            showFeedback('Error applying filter.', 'error');
        }
    });
}

// ==============================================
// GESTION DES DÉTAILS D'UN LIEU
// ==============================================

/**
 * Charge les détails d'un lieu spécifique
 * - Récupère l'ID du lieu depuis l'URL
 * - Charge les détails du lieu depuis l'API
 * - Charge les avis associés au lieu
 */
async function loadPlaceDetails() {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        showError('Invalid place ID');
        return;
    }
    
    const token = getCookie('token');
    
    try {
        const placeResponse = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        
        if (placeResponse.ok) {
            const place = await placeResponse.json();
            displayPlaceDetails(place);
            await loadReviews(placeId);
        } else {
            showError('Failed to load place details.');
        }
    } catch (error) {
        console.error('Error loading place details:', error);
        showError('Failed to load place details.');
    }
}

/**
 * Affiche les détails d'un lieu dans le DOM
 * @param {Object} place - Données du lieu à afficher
 * - Affiche le nom, le prix, l'image et la description
 * - Utilise une image par défaut si l'URL de l'image est manquante
 */
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    placeDetails.innerHTML = `
        <div class="place-header">
            <h2>${place.name}</h2>
            <p class="place-price">$${place.price_by_night}/night</p>
        </div>
        <img src="${place.image_url || DEFAULT_PLACE_IMAGE}" 
             alt="${place.name}" 
             class="place-image">
        <div class="place-description">
            <p>${place.description || 'No description available'}</p>
        </div>
    `;
}

// ==============================================
// GESTION DES AVIS
// ==============================================

/**
 * Charge les avis pour un lieu spécifique
 * @param {string} placeId - ID du lieu
 * - Effectue une requête GET à l'API pour les avis
 * - Affiche les avis ou un message si aucun avis n'existe
 */
async function loadReviews(placeId) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`);
        
        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            console.error('Failed to load reviews');
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

/**
 * Affiche les avis dans le DOM
 * @param {Array} reviews - Liste des avis à afficher
 * - Crée une carte pour chaque avis
 * - Affiche le nom de l'utilisateur, la note et le texte
 * - Formate la date de création
 * - Affiche les notes sous forme d'étoiles (★ pour pleines, ☆ pour vides)
 */
function displayReviews(reviews) {
    const reviewsList = document.querySelector('.reviews-list');
    if (!reviewsList) return;
    
    reviewsList.innerHTML = '';
    
    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p class="no-reviews">No reviews yet.</p>';
        return;
    }
    
    reviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.className = 'review-card';
        reviewElement.innerHTML = `
            <div class="review-header">
                <strong>${review.user_name}</strong>
                <div class="review-rating">
                    ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}
                </div>
            </div>
            <p class="review-text">${review.text}</p>
            <div class="review-date">
                ${new Date(review.created_at).toLocaleDateString()}
            </div>
        `;
        reviewsList.appendChild(reviewElement);
    });
}

/**
 * Soumet un nouvel avis pour un lieu
 * @param {Event} event - Événement de soumission
 * @param {string} formId - ID du formulaire
 * - Vérifie que l'utilisateur est connecté
 * - Récupère l'ID du lieu depuis l'URL
 * - Envoie les données du formulaire à l'API
 * - Recharge la page si succès pour afficher le nouvel avis
 */
async function submitReview(event, formId) {
    event.preventDefault();
    
    if (!checkAuthentication()) {
        alert('Please login to post a review.');
        return;
    }
    
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert('Invalid place ID');
        return;
    }

    const form = document.getElementById(formId);
    if (!form) return;
    
    const text = form.querySelector('[name="text"]').value;
    const rating = form.querySelector('[name="rating"]').value;
    const token = getCookie('token');
    
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                text, 
                rating: parseInt(rating) 
            })
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            const error = await response.json();
            showError(error.message || "Failed to submit review");
        }
    } catch (error) {
        console.error("Review submission error:", error);
        showError('Connection error. Please try again.');
    }
}

// ==============================================
// FONCTIONS UTILITAIRES
// ==============================================

/**
 * Récupère la valeur d'un cookie
 * @param {string} name - Nom du cookie
 * @returns {string|null} Valeur du cookie ou null
 * - Parse la chaîne document.cookie pour trouver le cookie demandé
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Définit le cookie d'authentification
 * @param {string} token - Token JWT
 * - Configure le cookie avec les attributs Secure et SameSite=Strict
 */
function setAuthCookie(token) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (24 * 60 * 60 * 1000)); // 24 heures
    document.cookie = `token=${token}; expires=${expires.toUTCString()}; path=/; Secure; SameSite=Strict`;
}

/**
 * Supprime le cookie d'authentification
 * - Définit une date d'expiration passée pour effacer le cookie
 */
function clearAuthCookie() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
}

/**
 * Redirige vers la page d'accueil
 */
function redirectToHome() {
    window.location.href = 'index.html';
}

/**
 * Récupère l'ID du lieu depuis l'URL
 * @returns {string|null} ID du lieu ou null
 * - Parse les paramètres de l'URL (ex: ?id=123)
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Affiche un message d'erreur
 * @param {string} message - Message à afficher
 * - Affiche le message dans un élément dédié ou via une alerte
 */
function showError(message) {
    const errorElement = document.getElementById('error-message');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    } else {
        alert(message);
    }
}

/**
 * Affiche un message de feedback
 * @param {string} message - Message à afficher
 * @param {string} type - Type de message ('success' ou 'error')
 * - Affiche le message avec un style correspondant au type
 * - Masque automatiquement le message après 5 secondes
 */
function showFeedback(message, type) {
    const feedbackElement = document.getElementById('feedback-message');
    if (feedbackElement) {
        feedbackElement.textContent = message;
        feedbackElement.className = `feedback-message ${type}`;
        feedbackElement.style.display = 'block';
        
        setTimeout(() => {
            feedbackElement.style.display = 'none';
        }, 5000);
    } else {
        alert(message);
    }
}

/**
 * Redirige vers la page de détail d'un lieu
 * @param {string} placeId - ID du lieu à afficher
 */
function goToDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}

/**
 * Charge les informations d'un lieu pour la page d'avis
 * - Récupère l'ID du lieu depuis l'URL
 * - Charge le nom et la description du lieu pour les afficher
 */
async function loadPlaceInfoForReview() {
    const placeId = getPlaceIdFromURL();
    if (!placeId) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
        if (response.ok) {
            const place = await response.json();
            const placeName = document.getElementById('place-name');
            const placeDesc = document.getElementById('place-description');
            
            if (placeName) placeName.textContent = place.name;
            if (placeDesc) placeDesc.textContent = place.description || 'No description available';
        }
    } catch (error) {
        console.error('Error loading place info:', error);
        showError('Failed to load place information');
    }
}

// Gestion du scroll pour l'en-tête
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (header) {
        header.classList.toggle('header-scrolled', window.scrollY > 10);
    }
});
