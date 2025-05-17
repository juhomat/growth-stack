// Glory Tools Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile menu toggle
    initMobileMenu();
    
    // Initialize tooltips
    initTooltips();
    
    // Add hover animations to cards
    initCardAnimations();
    
    // Add skeleton loading effect simulation
    simulateLoading();
});

/**
 * Initialize mobile menu toggle functionality
 */
function initMobileMenu() {
    const mobileMenuButton = document.querySelector('button.md\\:hidden');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            mobileMenu.classList.toggle('visible');
        });
    }
}

/**
 * Initialize tooltip functionality for elements with data-tooltip attribute
 */
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');
        
        // Create tooltip container
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-text';
        tooltip.textContent = tooltipText;
        
        // Add tooltip to element
        element.classList.add('tooltip');
        element.appendChild(tooltip);
    });
}

/**
 * Add hover animations to card elements
 */
function initCardAnimations() {
    const cards = document.querySelectorAll('.bg-white.rounded-xl');
    
    cards.forEach(card => {
        card.classList.add('hover-lift');
    });
}

/**
 * Simulate loading states with skeleton loaders
 */
function simulateLoading() {
    // This is a placeholder for real data loading
    // In a real application, this would be replaced with actual API calls
    
    // Example usage:
    // showLoadingState('performanceChart');
    // fetchData().then(data => {
    //     hideLoadingState('performanceChart');
    //     renderChart(data);
    // });
}

/**
 * Show loading state for an element
 * @param {string} elementId - The ID of the element to show loading state for
 */
function showLoadingState(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('skeleton');
        element.setAttribute('aria-busy', 'true');
    }
}

/**
 * Hide loading state for an element
 * @param {string} elementId - The ID of the element to hide loading state for
 */
function hideLoadingState(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('skeleton');
        element.removeAttribute('aria-busy');
    }
}

/**
 * Format date to a human-readable string
 * @param {Date} date - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    const isToday = date >= today && date < new Date(today.getTime() + 86400000);
    const isYesterday = date >= yesterday && date < today;
    
    if (isToday) {
        return `Today at ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
    } else if (isYesterday) {
        return `Yesterday at ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
    } else {
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    }
}

/**
 * Handle form submissions
 * @param {Event} event - The submit event
 */
function handleFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const formObject = {};
    
    formData.forEach((value, key) => {
        formObject[key] = value;
    });
    
    // This is where you would typically send the data to an API
    console.log('Form submitted with data:', formObject);
    
    // Show success message
    showNotification('Success! Your request has been submitted.', 'success');
    
    // Reset form
    form.reset();
}

/**
 * Show a notification message
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, warning, error)
 */
function showNotification(message, type = 'info') {
    // Check if notification container exists, create if not
    let notificationContainer = document.getElementById('notification-container');
    
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.className = 'fixed top-4 right-4 z-50 flex flex-col space-y-2';
        document.body.appendChild(notificationContainer);
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `p-4 rounded-lg shadow-lg flex items-center justify-between transition-all transform translate-x-0 opacity-100 ${getNotificationClass(type)}`;
    
    // Add notification content
    notification.innerHTML = `
        <span>${message}</span>
        <button class="ml-4 text-sm opacity-70 hover:opacity-100 focus:outline-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
        </button>
    `;
    
    // Add notification to container
    notificationContainer.appendChild(notification);
    
    // Add close button event listener
    notification.querySelector('button').addEventListener('click', () => {
        hideNotification(notification);
    });
    
    // Auto-hide after delay
    setTimeout(() => {
        hideNotification(notification);
    }, 5000);
}

/**
 * Hide a notification
 * @param {HTMLElement} notification - The notification element to hide
 */
function hideNotification(notification) {
    notification.classList.add('translate-x-full', 'opacity-0');
    
    setTimeout(() => {
        notification.remove();
    }, 300);
}

/**
 * Get notification class based on type
 * @param {string} type - The notification type
 * @returns {string} CSS class for the notification
 */
function getNotificationClass(type) {
    switch (type) {
        case 'success':
            return 'bg-green-100 text-green-800 border-l-4 border-green-500';
        case 'warning':
            return 'bg-yellow-100 text-yellow-800 border-l-4 border-yellow-500';
        case 'error':
            return 'bg-red-100 text-red-800 border-l-4 border-red-500';
        default:
            return 'bg-blue-100 text-blue-800 border-l-4 border-blue-500';
    }
} 