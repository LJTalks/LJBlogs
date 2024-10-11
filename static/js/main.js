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




// Script for sorting youtube checker app
// function sortBy(field, order) {
//     const url = new URL(window.location.href);
//     url.searchParams.set('sort_by', field);
//     url.searchParams.set('order', order);
//     window.location.href = url.href; // Trigger the page reload with the sorting parameters
// }