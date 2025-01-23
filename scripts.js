// Add any interactivity you want in JavaScript. 
// For example, you could add click events for each project for a modal preview or detailed info.
document.querySelectorAll('.project').forEach(project => {
  project.addEventListener('click', function() {
    alert('Redirecting to full project details!');
    // You can replace alert with actual redirection or opening of detailed view in your portfolio.
  });
});
