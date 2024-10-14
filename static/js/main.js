// Script for footer email obfuscation
document.addEventListener('DOMContentLoaded', function () {
    // Handle dark version in the footer
    var emailLinkDark = document.getElementById('emailLinkDark');
    if (emailLinkDark) {
        emailLinkDark.addEventListener('click', function () {
            window.location.href = 'mailto:laura@ljtalks.com';
        });
    }

    // Handle light version (now a button) on other pages
    var emailLinkLight = document.getElementById('emailLinkLight');
    if (emailLinkLight) {
        emailLinkLight.addEventListener('click', function () {
            window.location.href = 'mailto:laura@ljtalks.com';
        });
    }
});




