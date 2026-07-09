document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.fade-in');
    cards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(function() {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });

    const surveyCards = document.querySelectorAll('.survey-card');
    surveyCards.forEach(function(card) {
        card.classList.add('slide-left');
    });

    const backButtons = document.querySelectorAll('#btn-back');
    backButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            const card = this.closest('.survey-card');
            if (card) {
                card.classList.remove('slide-left');
                card.classList.add('slide-right');
            }
        });
    });
});
