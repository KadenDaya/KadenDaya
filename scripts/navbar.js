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
  const subDropdowns = document.querySelectorAll('.sub-dropdown');
  
  dropdowns.forEach(dropdown => {
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');
    
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      
      dropdowns.forEach(other => {
        if (other !== dropdown) {
          other.classList.remove('active');
        }
      });
      
      dropdown.classList.toggle('active');
    });
  });
  
  subDropdowns.forEach(subDropdown => {
    const toggle = subDropdown.querySelector('.sub-dropdown-toggle');
    
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      subDropdowns.forEach(other => {
        if (other !== subDropdown) {
          other.classList.remove('active');
        }
      });
      
      subDropdown.classList.toggle('active');
    });
  });
  
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.dropdown')) {
      dropdowns.forEach(dropdown => {
        dropdown.classList.remove('active');
      });
    }
    if (!e.target.closest('.sub-dropdown')) {
      subDropdowns.forEach(subDropdown => {
        subDropdown.classList.remove('active');
      });
    }
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
  }
}
