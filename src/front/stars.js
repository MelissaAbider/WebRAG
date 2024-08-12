const STAR_COUNT_TO_CSS_CLASS = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five"
}

/**
 * Attribut la bonne couleur (classe CSS) selon le nombre d'etoiles séléctionnées
 * @param {Number} n Nombre d'etoiles séléctionnées
 * @remakrs si n ne correspond pas à une classe CSS toutes les etoiles seront deséléctionnées
 */
function setStarColors(n) {
    const stars = document.querySelectorAll('.star');
    const className = STAR_COUNT_TO_CSS_CLASS[n] ?? '';


    for (let i = 0; i < stars.length; i++) {
        const star = stars[i];

        // On supprime toutes les classes, si certaines doivent etre préservées dans le futur il faudra changer cette ligne
        star.classList.remove(...star.classList);
        star.classList.add("star");

        if (i < n) {
            star.classList.add(className);
        }
    }
}

/**
 * Met à jour le champ qui sera recupéré par le submit
 * @param {Number} n Nombre d'etoiles séléctionnées, valeur affectée au champ sans autre verification
 */
function updateSelectedStars(n) {
    const hiddenInput = document.getElementById('selected-rating');
    hiddenInput.value = n;
}
/**
 * Initialise les etoiles feedback
 * @param {Number} numberOfStars Nombre d'etoiles à ajouter, 5 par defaut
 */
function initStars(numberOfStars = 5) {
    const rating = document.getElementById('rating');
    rating.innerHTML = ''; //On supprime tout les éléments enfants

    // on a besoin que i aille de 1 à n (et non 0 à n-1)
    for (let i = 1; i <= numberOfStars; i++) {
        const star = document.createElement('span');

        star.innerHTML = '★'; //On utilise le charactere pour representer l'etoile
        star.classList.add('star');
        star.addEventListener('click', () => {
            setStarColors(i);
            updateSelectedStars(i);
        });

        rating.appendChild(star);
    }

    // Les etoiles sont pas defaut toutes desélectionnées
    updateSelectedStars(-1);
    setStarColors(-1);
}