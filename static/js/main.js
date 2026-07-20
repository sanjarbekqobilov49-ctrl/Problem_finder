document.addEventListener('DOMContentLoaded', function() {
    const surveyForm = document.getElementById('surveyForm');
    if (surveyForm) {
        surveyForm.addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Yuklanmoqda...';
            }
        });
    }

    initOtherCheckboxes();
});

function initOtherCheckboxes() {
    const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');
    checkboxes.forEach(function(cb) {
        if (cb.value === '💭 Boshqa') {
            cb.addEventListener('change', function() {
                const parentDiv = this.closest('.form-check');
                if (!parentDiv) return;
                let otherInput = parentDiv.nextElementSibling;
                if (!otherInput || !otherInput.matches('.other-input')) {
                    otherInput = document.createElement('input');
                    otherInput.type = 'text';
                    otherInput.className = 'form-control mt-2 other-input';
                    otherInput.name = this.name + '_other';
                    otherInput.placeholder = '💭 Boshqa (yozing)';
                    otherInput.maxLength = 200;
                    parentDiv.after(otherInput);
                }
                otherInput.style.display = this.checked ? 'block' : 'none';
                if (this.checked) {
                    otherInput.focus();
                }
            });
        }
    });
}
