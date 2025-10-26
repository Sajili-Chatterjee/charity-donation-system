// Optional JS for small enhancements

// Smooth scroll for on-page anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const targetSelector = this.getAttribute('href');
    const targetElement = document.querySelector(targetSelector);

    // Prevent jump only if target exists
    if (targetElement) {
      e.preventDefault();
      targetElement.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Additional JS functions (custom interactivity, validations, etc.) can go here.
