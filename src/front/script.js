/**
 * Initialise le formulaire du retour de l'utilisateur sur la reponse du LLM
 */
function initForm() {
    // on doit dabords afficher la div et ensuite initialiser les etoiles et la zone de commentaire 
    const feedbackContainer = document.getElementById('feedback-form-container');
    if (feedbackContainer) {
        feedbackContainer.classList.remove('hidden');
        console.log("Classe 'hidden' retirée du conteneur de feedback");
    } else {
        console.error("Conteneur de feedback non trouvé");
    }
    initCommentRegion();
    initStars(5);
}

/**
 * Remets le chat à zero
 * Sert quand le feedback est envoyé pour commencer un nouveau prompt
 */
// Remet à zéro le chat et affiche un message de bienvenue.

function resetChat() {
    const chatbox = document.getElementById('chat-box');
    chatbox.innerHTML = '';

    const welcomeMessage = document.createElement('div');
    welcomeMessage.classList.add('message', 'bot-message');
    welcomeMessage.innerHTML = 'Welcome again ! Ask your questions please';

    chatbox.appendChild(welcomeMessage);
}
// L'utilisateur clique sur le bouton d'envoi, le message est affiché dans le chat, et une réponse est générée.

let lastPromptId = null;  // Stocker l'ID du prompt

document.getElementById('send-btn').addEventListener('click', async function () {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    // Afficher le message de l'utilisateur
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = userInput;
    document.getElementById('chat-box').appendChild(userMessage);

    // Afficher l'indicateur de chargement
    const loadingIndicator = document.querySelector('.loader');
    loadingIndicator.classList.remove('hidden');

    // Afficher le message de chargement
    const loadingMessage = document.querySelector('.loading-text');
    loadingMessage.classList.remove('hidden');

    // Désactiver le bouton "Envoyer"
    const sendButton = document.getElementById('send-btn');
    console.log('Désactivation du bouton');
    sendButton.disabled = true;

     // Effacer le champ de saisie
     document.getElementById('user-input').value = '';
    const user_input = document.getElementById('user-input');
    user_input.disabled = true;


    try {
         
        console.log('Envoi de la question à l\'API');
        const response = await sendQuestionToApi(userInput);
        console.log('Réponse reçue:', response);
        lastPromptId = response.id;
        // Masquer l'indicateur de chargement
        loadingIndicator.classList.add('hidden');
        // Masquer le message de chargement
        loadingMessage.classList.add('hidden');
        
        // Afficher la réponse 
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot-message');
        botMessage.textContent = response.answer; // Utiliser le champ 'answer' de la réponse
        document.getElementById('chat-box').appendChild(botMessage);
        
    } catch (error) {
        console.error('Erreur lors de l\'envoi de la question à l\'API:', error);
        // Masquer l'indicateur de chargement en cas d'erreur
        loadingIndicator.classList.add('hidden');
        // Masquer le message de chargement en cas d'erreur
        loadingMessage.classList.add('hidden');
    }

    initForm(); // pour afficher le champ de feedback
});


// Fonction pour envoyer la question à l'API
async function sendQuestionToApi(question) {
    const apiUrl = 'http://localhost:8000/api/ask/'; // url de l'api 

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }), // Envoyer la question dans le corps de la requête
    });

    if (!response.ok) {
        throw new Error('Erreur réseau lors de l\'envoi de la question');
    }

    return await response.json(); // Retourner la réponse JSON de l'API
}



//Cette section gère l'envoi des données de feedback lorsque le formulaire est soumis. Elle vérifie également si la note est valide

document.getElementById('feedback-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const feedbackData = {
        comment: formData.get('comment'),
        rating: parseInt(formData.get('rating')),
        prompt_id: lastPromptId,
    };

    // Vérifier si tous les champs ont été remplis correctement

    if (Number(feedbackData.rating) > 5 || Number(feedbackData.rating) < 1) {
        document.getElementById('form-error').classList.remove('hidden');
    }
    else {
        // Masquer le message d'erreur si tout est rempli
        document.getElementById('form-error').classList.add('hidden');
    
    // Envoyer les données de feedback à l'API
    try {
        await sendFeedback(feedbackData); // Attendre la réponse
    } catch (err) {
    console.error('Erreur lors de l\'envoi du feedback:', err);
        }
        // Réinitialiser le formulaire et masquer le conteneur
        event.target.reset();
        document.getElementById('feedback-form-container').classList.add('hidden');

        // Réactiver le bouton "Envoyer"
        console.log('Réactivation du bouton');
        const sendButton = document.getElementById('send-btn');

        sendButton.disabled = false;
        // Réactiver le champ de sasie
        const user_input = document.getElementById('user-input');
        user_input.disabled = false;
        
        resetChat();
    }
});

let lastUserInput = '';
let lastBotResponse = '';

// Envoie les données de feedback (le commentaire + rating) à l'API 
async function sendFeedback(feedbackData) {
    const apiUrl = `http://localhost:8000/api/feedback/${feedbackData.prompt_id}`;//utilise l'id du prompt pour lier le feedback à la question/reponse 

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            comment: feedbackData.comment,//Le commentaire laissé par l'utilisateur
            rating: parseInt(feedbackData.rating),//La notation donnée par l'utilisateur (1 à 5)
        })
    })
    if (!response.ok) {
        throw new Error('Erreur réseau lors de l\'envoi de la question');
    }

    return await response.json(); // Retourner la réponse JSON de l'API
}

