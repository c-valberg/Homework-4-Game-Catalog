document.addEventListener('DOMContentLoaded', async () => {
    // find the modal element
    const modal = document.getElementById('form-modal');
    // if the modal exists and has the 'show' class, create a new Bootstrap modal instance and show it
    if (modal !== null && modal.classList.contains('show')) {
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }
});
