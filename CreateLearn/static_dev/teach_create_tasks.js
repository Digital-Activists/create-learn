

document.addEventListener('DOMContentLoaded', function() {

        const dropdownButtons = document.querySelectorAll('.dropdownBtn');

        dropdownButtons.forEach(button => {
            button.addEventListener('click', function(event) {
                dropdownButtons.forEach(otherButton => {
                    if (otherButton !== button) {
                        otherButton.nextElementSibling.classList.remove('active');
                    }
                });

                this.nextElementSibling.classList.toggle('active');
                event.stopPropagation(); 
            });
        });

        
        document.addEventListener('click', function(event) {
            dropdownButtons.forEach(button => {
                if (!button.nextElementSibling.contains(event.target) && button !== event.target) {
                    button.nextElementSibling.classList.remove('active');
                }
            });
        });
    });


    document.querySelectorAll('.dropdown-content').forEach(dropdown => {
        dropdown.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    });