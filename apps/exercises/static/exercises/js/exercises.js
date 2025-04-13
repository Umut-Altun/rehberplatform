document.addEventListener('DOMContentLoaded', function() {
    // Initialize exercise start buttons
    const exerciseButtons = document.querySelectorAll('.exercise-button');
    
    exerciseButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const exerciseId = this.getAttribute('data-exercise-id');
            const exerciseType = this.getAttribute('data-exercise-type');
            
            // You can add specific behavior here when an exercise is started
            console.log(`Starting exercise: ${exerciseId} of type: ${exerciseType}`);
            
            // For now, we'll just follow the link normally
            // In the future, you might want to add animations or other effects
        });
    });
}); 