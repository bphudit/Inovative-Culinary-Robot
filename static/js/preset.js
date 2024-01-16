let selectedPreset = null;

document.querySelectorAll('.preset-box').forEach(box => {
    box.addEventListener('click', function() {
        // Remove 'selected-preset' class and hide check icons from all boxes
        document.querySelectorAll('.preset-box').forEach(otherBox => {
            otherBox.classList.remove('selected-preset');
            otherBox.querySelector('.check-icon').style.display = 'none';
        });

        // Add 'selected-preset' class and show the check icon for the clicked box
        this.classList.add('selected-preset');
        this.querySelector('.check-icon').style.display = 'block';

        selectedPreset = this.getAttribute('data-preset');
    });
});

document.getElementById('startButton').addEventListener('click', function() {
    if (selectedPreset) {
        fetch(`/run_preset/${selectedPreset}`, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Handle response
            })
            .catch(error => console.error('Error:', error));
    } else {
        alert('Please select a preset first.');
    }
});


