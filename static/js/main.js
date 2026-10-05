// main.js — students will add JavaScript here as features are built

// Modal functionality
document.addEventListener('DOMContentLoaded', function() {
    const seeHowItWorksBtn = document.getElementById('seeHowItWorksBtn');
    const howItWorksModal = document.getElementById('howItWorksModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const youtubeVideo = document.getElementById('youtubeVideo');

    // Store the original YouTube URL
    const videoUrl = youtubeVideo ? youtubeVideo.src : '';

    // Open modal when button is clicked
    if (seeHowItWorksBtn) {
        seeHowItWorksBtn.addEventListener('click', function() {
            howItWorksModal.style.display = 'block';
            // Restore video source when opening modal
            if (youtubeVideo && videoUrl) {
                youtubeVideo.src = videoUrl;
            }
        });
    }

    // Close modal when close button is clicked
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', function() {
            howItWorksModal.style.display = 'none';
            // Clear video source when closing modal to stop playback
            if (youtubeVideo) {
                youtubeVideo.src = '';
            }
        });
    }

    // Close modal when clicking outside of modal content
    window.addEventListener('click', function(event) {
        if (event.target === howItWorksModal) {
            howItWorksModal.style.display = 'none';
            // Clear video source when closing modal to stop playback
            if (youtubeVideo) {
                youtubeVideo.src = '';
            }
        }
    });
});
