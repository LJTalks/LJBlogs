// For blog post_detail admin
(function($) {
    $(document).ready(function() {
        // Function to auto-save the form every 60 seconds, only if status is draft
        setInterval(function() {
            // Check if the post is still in draft status
            const statusField = $('#id_status').val();
            // Draft status is usually 0, adjust as per your STATUS choices in models.py
            if (statusField === '0' && $('#id_title').val()) {
                $('#post_form').submit();
            }
        }, 60000);  // Save every 60,000 milliseconds (60 seconds)
    });
})(django.jQuery);
