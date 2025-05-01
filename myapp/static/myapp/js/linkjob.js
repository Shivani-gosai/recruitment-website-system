document.addEventListener('DOMContentLoaded', () => {
    const removeButtons = document.querySelectorAll('.remove-job');

    removeButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const jobItem = event.target.closest('.job-item');
            jobItem.remove();
        });
    });
});

function goBack() {
    window.history.back(); // Takes the user to the previous page
}