fetch('navbar.html')
  .then(response => response.text())
  .then(html => {
    document.getElementById('navbar-container').innerHTML = html;
    initializeDropdowns();
    setActiveNavigation();
  })
  .catch(error => console.error('Error loading navbar:', error));


function initializeDropdowns() {
  const dropdowns = document.querySelectorAll('.dropdown');
  
  dropdowns.forEach(dropdown => {
    const toggle = dropdown.querySelector('.dropdown-toggle');
    
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      window.location.href = this.href;
    });
  });
}

function setActiveNavigation() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-links a');
  
  navLinks.forEach(link => {
    link.classList.remove('active');
  });
  
  if (currentPath === '/' || currentPath === '/index.html') {
    const homeLink = document.querySelector('.nav-links a[href="/"]');
    if (homeLink) homeLink.classList.add('active');
  } else if (currentPath === '/aboutme.html' || currentPath.endsWith('aboutme.html')) {
    const aboutLink = document.querySelector('.nav-links a[href="/aboutme.html"]');
    if (aboutLink) aboutLink.classList.add('active');
  } else if (currentPath === '/contact.html' || currentPath.endsWith('contact.html')) {
    const contactLink = document.querySelector('.nav-links a[href="/contact.html"]');
    if (contactLink) contactLink.classList.add('active');
  } else if (currentPath === '/donate.html' || currentPath.endsWith('donate.html')) {
    const donateLink = document.querySelector('.nav-links a[href="/donate.html"]');
    if (donateLink) donateLink.classList.add('active');
  } else if (currentPath === '/blog.html' || currentPath.endsWith('blog.html') || currentPath.startsWith('/blog/')) {
    const blogLink = document.querySelector('.nav-links a[href="/blog.html"]');
    if (blogLink) blogLink.classList.add('active');
  } else if (currentPath === '/projects.html' || currentPath.endsWith('projects.html') || currentPath.startsWith('/projects/')) {
    const projectsLink = document.querySelector('.nav-links a[href="/projects.html"]');
    if (projectsLink) projectsLink.classList.add('active');
  }
}
