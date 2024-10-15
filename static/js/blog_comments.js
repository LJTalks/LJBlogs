document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded")

    const editButtons = document.getElementsByClassName("btn-edit");
    const blogCommentText = document.getElementById("id_body");
    const blogCommentForm = document.getElementById("blogCommentForm");
    const submitButton = document.getElementById("submitButton");
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("btn-delete");
    const deleteConfirm = document.getElementById("deleteConfirm");

    /**
     * Initializes edit functionality for the provided edit buttons.
     * 
     * For each button in the `editButtons` collection:
     * - Retrieves the associated comment's ID upon click.
     * - Fetches the content of the corresponding comment.
     * - Populates the `commentText` input/textarea with the comment's content for editing.
     * - Updates the submit button's text to "Update".
     * - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
     */
    for (let button of editButtons) {
        button.addEventListener("click", (e) => {
            let blogCommentId = e.target.getAttribute("blog_comment_id");
            let blogCommentContent = document.getElementById(
                `blog_comment${blogCommentId}`).innerText;
            // Populate the form's textarea with the comment content
            blogCommentText.value = blogCommentContent;
            // Change the submit button text to 'Update'
            submitButton.innerText = "Update";
            // Update the form's action URL to point to the edit view
            blogCommentForm.setAttribute("action", `edit_blog_comment/${blogCommentId}`);
        });
    }

    /**
     * Initializes deletion functionality for the provided delete buttons.
     * 
     * For each button in the `deleteButtons` collection:
     * - Retrieves the associated comment's ID upon click.
     * - Updates the `deleteConfirm` link's href to point to the 
     * deletion endpoint for the specific comment.
     * - Displays a confirmation modal (`deleteModal`) to prompt 
     * the user for confirmation before deletion.
     */
    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            let blogCommentId = e.target.getAttribute("blog_comment_id");
            // Update the confirmation modal's link href to point to Delete view
            deleteConfirm.href = `delete_blog_comment/${blogCommentId}`;
            // Show the delete confirmation modal
            deleteModal.show();
        });
    }

});