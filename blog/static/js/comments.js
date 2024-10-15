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
        let blogCommentContent = document.getElementById(`blog_comment${blogCommentId}`).innerText;
        blogCommentText.value = blogCommentContent;
        submitButton.innerText = "Update";
        blogCommentForm.setAttribute("action", `edit_blog_comment/${blog_commentId}`);
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
        deleteConfirm.href = `delete_blog_comment/${blog_commentId}`;
        deleteModal.show();
    });
}