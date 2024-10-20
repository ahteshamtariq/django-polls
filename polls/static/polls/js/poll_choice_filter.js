// This script dynamically updates the available choices for a poll based on the poll selected by the user. 
// It ensures that when a user picks a different poll from a dropdown, only the relevant choices for that poll are shown.
{
    // Wait until the entire HTML content of the page has loaded.
    document.addEventListener('DOMContentLoaded', function() {
        
        // Get the dropdown field elements for selecting a poll and displaying choices.
        var pollField = document.getElementById('id_poll');  // Dropdown for selecting a poll.
        var choiceField = document.getElementById('id_choice');  // Dropdown for displaying choices related to the selected poll.

        // Function that fetches and updates the choices for a selected poll.
        function updateChoices() {
            // Get the currently selected poll's ID from the dropdown.
            var pollId = pollField.value;

            // Check if a poll has been selected (pollId is not empty).
            if (pollId) {
                // Use Django's jQuery to make an AJAX request to fetch choices for the selected poll.
                django.jQuery.ajax({
                    url: window.location.origin + '/polls/get_choices',  // API endpoint to retrieve choices.
                    data: { 'poll': pollId },  // Send the selected poll ID as part of the request.
                    success: function(data) {
                        // On successful retrieval, update the choice dropdown with the new options.
                        updateChoicesFields(choiceField, data);
                    }
                });
            } else {
                // If no poll is selected, clear the choice dropdown.
                choiceField.value = '';
            }
        }

        // Function to update the options in the choice dropdown.
        function updateChoicesFields(choiceField, data) {
            // Clear any existing options in the choice dropdown.
            choiceField.innerHTML = '';

            // Add a default empty option to the dropdown (e.g., for "Select a choice").
            var defaultOption = new Option('---------', '');
            choiceField.appendChild(defaultOption);

            // Loop through each choice returned from the AJAX request.
            data.choices.forEach(function(choice) {
                // Create a new option element for each choice.
                var newOption = new Option(choice.text, choice.id);
                // Add the new choice option to the dropdown.
                choiceField.appendChild(newOption);
            });
        }

        // Attach an event listener to the poll dropdown.
        // Whenever the user selects a new poll, updateChoices() will be called to refresh the choices.
        pollField.addEventListener('change', updateChoices);
    });
}
