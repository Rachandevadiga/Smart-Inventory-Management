// ==============================
// main.js
// ==============================

// Auto-dismiss flash alerts after 4 seconds
document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('hide');
        }, 4000); // 4 seconds
    });
});

// Highlight active sidebar/nav link based on current URL
const currentPath = window.location.pathname;
const navLinks = document.querySelectorAll('.nav-link');

navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
    }
});

// Optional: Confirm deletion pop-ups (already done inline in HTML, but extra safety)
const deleteButtons = document.querySelectorAll('.btn-danger');
deleteButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const confirmDelete = confirm("Are you sure you want to delete this item?");
        if (!confirmDelete) {
            e.preventDefault();
        }
    });
});

// Optional: Sidebar toggle for smaller screens
const sidebar = document.querySelector('.sidebar');
const navbarToggler = document.querySelector('.navbar-toggler');

if (navbarToggler) {
    navbarToggler.addEventListener('click', () => {
        sidebar.classList.toggle('d-none');
    });
});
