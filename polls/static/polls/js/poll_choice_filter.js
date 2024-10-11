// 'use strict';
{
    document.addEventListener('DOMContentLoaded', function() {

        var pollField = document.getElementById('id_poll');  // Poll dropdown field
        var choiceField = document.getElementById('id_choice');  // Choice dropdown field

        function updateChoices() {
            var pollId = pollField.value;  // Get the selected poll ID

            if (pollId) {
                // Fetch filtered choices via AJAX based on selected poll
                django.jQuery.ajax({
                    url: window.location.origin + '/polls/get_choices',  // URL for retrieving choices
                    data: { 'poll': pollId },  // Pass poll ID as data
                    success: function(data) {
                        updateChoicesFields(choiceField, data);  // Update choice dropdown with new options
                    }
                });
            } else {
                choiceField.value = '';  // Clear choice field if no poll is selected
            }
        }

        // Updates the choice dropdown options
        function updateChoicesFields(choiceField, data) {
            choiceField.innerHTML = '';  // Clear current options

            var defaultOption = new Option('---------', '');  // Add default option
            choiceField.appendChild(defaultOption);

            // Add new choices returned by AJAX
            data.choices.forEach(function(choice) {
                var newOption = new Option(choice.text, choice.id);  // Create new option element
                choiceField.appendChild(newOption);  // Append new option to the dropdown
            });
        }

        pollField.addEventListener('change', updateChoices);  // Update choices on poll selection
    });
}
