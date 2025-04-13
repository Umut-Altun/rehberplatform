document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let valid = true;
            const inputs = form.querySelectorAll('input[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('error');
                    
                    // Add error styling
                    input.style.borderColor = '#ff3860';
                    
                    // Remove error styling on input
                    input.addEventListener('input', function() {
                        if (input.value.trim()) {
                            input.classList.remove('error');
                            input.style.borderColor = '';
                        }
                    });
                }
            });
            
            // Password validation for register form
            const password1 = form.querySelector('input[name="password1"]');
            const password2 = form.querySelector('input[name="password2"]');
            
            if (password1 && password2 && password1.value !== password2.value) {
                valid = false;
                password2.classList.add('error');
                password2.style.borderColor = '#ff3860';
                
                // Create error message if it doesn't exist
                let errorMsg = form.querySelector('.password-error');
                if (!errorMsg) {
                    errorMsg = document.createElement('div');
                    errorMsg.className = 'password-error';
                    errorMsg.style.color = '#ff3860';
                    errorMsg.style.fontSize = '12px';
                    errorMsg.style.marginTop = '5px';
                    errorMsg.textContent = 'Şifreler eşleşmiyor';
                    password2.parentNode.appendChild(errorMsg);
                }
            }
            
            if (!valid) {
                event.preventDefault();
            }
        });
    });
    
    // Social login buttons
    const socialButtons = document.querySelectorAll('.social-login-button');
    
    socialButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            // Here you would normally implement the social login logic
            // For demonstration purposes, we'll just add a simple animation
            
            button.style.transform = 'scale(0.95)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
                
                // Placeholder for actual social login implementation
                console.log('Social login clicked:', button.textContent.trim());
                
                // For demo only - show a message that this is not implemented
                alert('Social login not implemented yet. This would redirect to the OAuth provider.');
            }, 150);
        });
    });
    
    // Password visibility toggle
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(field => {
        // Create toggle button
        const toggleBtn = document.createElement('i');
        toggleBtn.className = 'fas fa-eye password-toggle';
        
        field.parentNode.appendChild(toggleBtn);
        
        toggleBtn.addEventListener('click', function() {
            if (field.type === 'password') {
                field.type = 'text';
                toggleBtn.className = 'fas fa-eye-slash password-toggle';
            } else {
                field.type = 'password';
                toggleBtn.className = 'fas fa-eye password-toggle';
            }
        });
    });
});
