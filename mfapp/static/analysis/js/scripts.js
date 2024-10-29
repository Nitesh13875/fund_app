// static/analysis/js/scripts.js

$(document).ready(function() {
    // Handle form submission for adding funds to the portfolio
    $('#add-fund-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const fundId = $('#fund-id').val(); // Get the fund ID from the input field

        // You can replace this alert with an AJAX call to your backend to add the fund
        alert(`Fund with ID ${fundId} has been added to your portfolio.`);

        // Clear the input field after submission
        $('#fund-id').val('');
    });

    // Example: Show a modal with more information when a card is clicked
    $('.card').on('click', function() {
        const fundName = $(this).data('fund-name'); // Get fund name from the data attribute
        $('#fund-name-modal').text(fundName); // Set the fund name in the modal
        $('#fund-modal').modal('show'); // Show the modal (you would need a modal structure in your HTML)
    });
});
