// 'use strict';
{
    document.addEventListener('DOMContentLoaded', function() {

        var pollField = document.getElementById('id_poll');  // Poll dropdown field
        var choiceContainer = document.getElementById('id_choice');  // Choice dropdown field
        if (pollField.value == ''){
            choiceContainer.innerHTML = 'Please Select a Pool First';
        } else {
            updateChoices();
        }

        function updateChoices() {
            var pollId = pollField.value;  // Get the selected poll ID

            if (pollId) {
                // Fetch filtered choices via AJAX based on selected poll
                django.jQuery.ajax({
                    url: window.location.origin + '/polls/get_choices',  // URL for retrieving choices
                    data: { 'poll': pollId },  // Pass poll ID as data
                    success: function(data) {
                        updateChoicesFields(choiceContainer, data);  // Update choice dropdown with new options
                    }
                });
            } else {
                choiceContainer.value = '';  // Clear choice field if no poll is selected
            }
        }

        // Updates the choice dropdown options
        function updateChoicesFields(choiceContainer, data) {
            choiceContainer.innerHTML = '';  // Clear current options

            // Add new choices returned by AJAX
            data.choices.forEach(function(choice) {
                var checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'choices';
                checkbox.value = choice.id;
                checkbox.id = 'id_choice_' + choice.id;
                
                var label = document.createElement('label');
                label.for = 'id_choice_' + choice.id;
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(' ' + choice.text));
                
                choiceContainer.appendChild(label);
            });
        }

        pollField.addEventListener('change', updateChoices);  // Update choices on poll selection
    });
}
