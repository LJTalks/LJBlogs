document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded");

    const listTypeCheckboxes = document.querySelectorAll("input[name='list_type']");
    const unsubscribeModal = new bootstrap.Modal(document.getElementById("unsubscribeModal"));
    const confirmUnsubscribeButton = document.getElementById("confirmUnsubscribe");
    const unsubscribedCheckbox = document.getElementById("unsubscribedCheckbox");  // Unsubscribed hidden checkbox
    const form = document.querySelector("form");
    let isUnsubscribing = false;  // To track whether user confirmed unsubscribing

    /**
     * Function to check if all checkboxes are unchecked
     */
    function checkAllUnchecked() {
        return Array.from(listTypeCheckboxes).every(checkbox => !checkbox.checked);
    }

    /**
     * Event listener for the form submit event
     * If all checkboxes are unchecked, trigger the confirmation modal.
     */
    form.addEventListener("submit", function (e) {
        if (checkAllUnchecked() && !isUnsubscribing) {
            e.preventDefault();  // Prevent form submission
            unsubscribeModal.show();  // Show the confirmation modal
        }
    });

    /**
     * Event listener for the unsubscribe confirmation button
     * If confirmed, allow form submission.
     */
    confirmUnsubscribeButton.addEventListener("click", function () {
        isUnsubscribing = true;
        console.log("Form submit triggered!");

        if (checkAllUnchecked()) {
            console.log("No list selected. Adding 'Unsubscribed'.");
            unsubscribedCheckbox.checked = true;  // Check the hidden Unsubscribed box
        }

        console.log("Unsubscribing: submitting form...");
        unsubscribeModal.hide();  // Hide the modal
        form.submit();  // Submit the form
        console.log("Form submit completed!");
    });
});
