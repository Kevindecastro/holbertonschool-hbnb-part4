# HBnB - Simple Web Client

> Part 4 - Frontend Development  

## Description

HBnB - Simple Web Client est la quatrième phase du projet HBnB.  
Cette partie se concentre sur le développement front-end d'une application interactive connectée aux services d'API back-end développés dans les parties précédentes.  
Le projet utilise **HTML5**, **CSS3**, et **JavaScript ES6** pour créer une interface dynamique et moderne.

---

## Objectifs

- Développer une interface utilisateur conviviale respectant les spécifications du design.
- Implémenter la connexion au back-end via AJAX/Fetch API.
- Assurer une gestion efficace et sécurisée des données client-side.
- Appliquer des pratiques modernes de développement web.

---

## Technologies Utilisées

- HTML5
- CSS3
- JavaScript (ES6+)
- Fetch API
- Cookies pour la gestion de session
- Responsive Web Design

---

## Fonctionnalités

### 🖌️ Design

- Création des pages suivantes :
  - Login
  - Liste des lieux
  - Détails d’un lieu
  - Ajouter un avis
- Respect du design fourni, avec flexibilité sur les couleurs, polices et images.

### 🔑 Authentification

- Formulaire de connexion utilisant l'API.
- Stockage du token JWT dans les cookies.
- Redirection de l'utilisateur après connexion.

### 🏡 Liste des lieux

- Affichage dynamique des lieux récupérés via API.
- Filtrage client-side des lieux selon le prix sélectionné.
- Affichage du bouton de connexion seulement si l'utilisateur n'est pas authentifié.

### 🏠 Détails d’un lieu

- Vue détaillée d'un lieu incluant nom, description, prix, commodités et avis.
- Affichage conditionnel du formulaire pour ajouter un avis si l'utilisateur est connecté.

### 📝 Ajouter un avis

- Formulaire pour publier un avis sur un lieu spécifique.
- Accessibilité réservée aux utilisateurs authentifiés.
- Gestion des soumissions et retours d'erreur via API.

---

## Installation et Lancement

1. **Cloner ce repository :**

```bash
git clone https://github.com/Kevindecastro/holbertonschool-hbnb-part4.git
cd holbertonschool-hbnb-part4/part4
```

2. **Configurer l'API back-end :**  
S'assurer que l'API est configurée pour accepter les requêtes **CORS** depuis le front-end.

3. **Ouvrir le client Web :**

Tu peux simplement ouvrir les fichiers HTML localement, ou utiliser un serveur local pour éviter certains problèmes de CORS.

```bash
# Exemple avec Python
python3 -m http.server
```

4. **Naviguer vers** `http://localhost:5000` dans ton navigateur.


## Pages Disponibles

| Page            | Fichier             | Description |
|-----------------|----------------------|-------------|
| Page de Connexion | `login.html`         | Connexion de l'utilisateur |
| Liste des Lieux | `index.html`          | Affichage de tous les lieux |
| Détail d’un Lieu | `place.html`          | Informations détaillées d'un lieu |
| Ajouter un Avis | `add_review.html`     | Formulaire pour ajouter un avis |

---

## Architecture des Fichiers

```
hbnb/
├── backend/
│    ├── app
│    │    ├── api
│    │    │    ├── v1
│    │    │    │    ├── _init_.py
│    │    │    │    ├── admin.py
│    │    │    │    ├── ameneties.py
│    │    │    │    ├── auth.py
│    │    │    │    ├── places.py
│    │    │    │    ├── reviews.py
│    │    │    │    ├── users.py 
│    │    │    └── _init_.py
│    │    ├── models
│    │    │    ├── _init_.py
│    │    │    ├── ameneties.py
│    │    │    ├── base_model.py
│    │    │    ├── places.py
│    │    │    ├── reviews.py
│    │    │    └── users.py 
│    │    ├── persistence
│    │    │    ├── _init_.py
│    │    │    ├── repository.py
│    │    │    └── user_repository.py
│    │    ├── services
│    │    │    ├── _init_.py
│    │    │    └── facade.py
│    │    ├── _init_.py
│    │    └── extensions.py
│    ├── instance
│    │    └── development.db
│    ├── tests
│    │    ├── _init_.py
│    │    ├── admin.py
│    │    ├── test_ameneties.py
│    │    ├── test_places.py
│    │    ├── test_relations.py
│    │    ├── test_reviews.py
│    │    └── test_users.py
│    ├── config.py
│    ├── hbnb.sql
│    ├── mermaid.js
│    ├── requirements.txt
│    ├── run.py
│    └── README.md
└── frontend/
     ├── static/
     │    ├── styles.css
     │    ├── scripts.js
     │    └── images/
     │         ├── logo.png
     │         ├── icon.png
     │         ├── favicon.ico
     │         ├── favicon.png
     │         ├── default-place.jpg
     │         ├── icon_bath.png
     │         ├── icon_bed.png
     │         ├── icon_wifi.png
     │         ├── place1.jpg
     │         ├── place2.jpg
     │         └── place3.jpg
     └── templates/
  	      ├── index.html
  	      ├── login.html
         ├── place.html
         └── add_review.html

```

---

## Instructions de Validation

- Toutes les pages doivent être **valides W3C**.
- Le projet doit être testé avec :
  - Des utilisateurs authentifiés et non authentifiés.
  - Des filtres appliqués correctement sur la liste des lieux.
  - L'ajout d'avis valide uniquement pour les utilisateurs connectés.

---

## Points d'Attention

- ⚠️ Assurez-vous que l'API gère correctement **CORS** pour autoriser les requêtes front-end.
- 🧹 Respectez la structure HTML5 sémantique et une bonne organisation CSS.
- 📱 L'application doit être **responsive** (adaptée mobile/tablette).

---

## Ressources Utiles

- [HTML5 Documentation](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
- [CSS3 Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript ES6](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Handling Cookies in JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
- [Client-Side Form Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation)

---

## Auteur

- [@Kevin](https://github.com/Kevindecastro)

---
