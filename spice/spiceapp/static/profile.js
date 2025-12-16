// Tab Navigation
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Form Submissions
    const accountForm = document.getElementById('accountForm');
    const securityForm = document.getElementById('securityForm');

    accountForm.addEventListener('submit', function(e) {
        e.preventDefault();
        showNotification('Saving changes...', 'info');
        
        // Simulate API call
        setTimeout(() => {
            showNotification('Changes saved successfully!', 'success');
        }, 1500);
    });

    securityForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (newPassword !== confirmPassword) {
            showNotification('Passwords do not match!', 'error');
            return;
        }

        showNotification('Updating security settings...', 'info');
        
        // Simulate API call
        setTimeout(() => {
            showNotification('Security settings updated successfully!', 'success');
            securityForm.reset();
        }, 1500);
    });
});

// Image Upload Handling
function triggerFileInput(inputId) {
    document.getElementById(inputId).click();
}

function handleImageUpload(event, type) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            if (type === 'cover') {
                document.querySelector('.cover-photo').style.backgroundImage = `url(${e.target.result})`;
            } else {
                document.getElementById('profilePic').src = e.target.result;
            }
        };
        reader.readAsDataURL(file);
        showNotification('Image uploaded successfully!', 'success');
    }
}

// Payment Method Management
function deletePaymentMethod(button) {
    if (confirm('Are you sure you want to remove this payment method?')) {
        const card = button.closest('.payment-card');
        card.style.animation = 'fadeOut 0.3s ease forwards';
        setTimeout(() => {
            card.remove();
            showNotification('Payment method removed successfully!', 'success');
        }, 300);
    }
}

// Notification System
function showNotification(message, type = 'success') {
    // Remove existing notification if any
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 2rem',
        borderRadius: '5px',
        backgroundColor: type === 'success' ? '#4caf50' : 
                        type === 'error' ? '#f44336' : '#2196f3',
        color: 'white',
        boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
        zIndex: '1000',
        animation: 'slideIn 0.3s ease forwards'
    });

    // Add to document
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add necessary animations to stylesheet
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    @keyframes fadeOut {
        to {
            opacity: 0;
            transform: scale(0.9);
        }
    }
`;
document.head.appendChild(style);