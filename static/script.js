let selectedFiles = []; // Array to store the selected files
let selectedSocialMedia = []; // Array to store the selected social media platforms

document.getElementById('photoInput').addEventListener('change', function (event) {
    const files = Array.from(event.target.files); // Convert the FileList to an array
    
    selectedFiles = selectedFiles.concat(files); // Append the new files to the existing array
    updateFileInput(selectedFiles);
    const photoContainer = document.getElementById('photoContainer');
    photoContainer.innerHTML = ''; // Clear previous images

    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();


        reader.onload = function (e) {
            const photoWrapper = document.createElement('div'); // Create a new div for photo and delete button
            photoWrapper.classList.add('photo-wrapper'); // Add a class for styling
            photoWrapper.style.position = 'relative';
            photoWrapper.style.display = 'inline-block';
            photoWrapper.style.margin = '10px';

            const photoPreview = document.createElement('img'); // Create a new img element
            photoPreview.src = e.target.result;
            // photoPreview.style.maxWidth = '500px'; // Set the width of the image
            // photoPreview.style.maxHeight = '500px'; // Set the height of the image
            photoPreview.style.display = 'block';

            const deleteButton = document.createElement('button'); // Create a delete button
            deleteButton.textContent = 'X';
            deleteButton.style.position = 'absolute';
            deleteButton.style.top = '0';
            deleteButton.style.right = '0';
            deleteButton.style.color = 'red';
            // deleteButton.style.color = 'white';
            deleteButton.style.border = 'none';
            deleteButton.style.borderRadius = '50%';
            deleteButton.style.cursor = 'pointer';
            deleteButton.addEventListener('click', function () {
                selectedFiles.splice(selectedFiles.indexOf(file), 1); // Remove the file from the selected files array
                updateFileInput(selectedFiles); // Update the file input with the new file list
                photoWrapper.remove(); // Remove the photo and button
                console.log(selectedFiles); // Debug: log the current selected files

                if (selectedFiles.length === 0) {
                    document.getElementById('photoInput').value = ''; // Clear the file input value
                }
            });

            photoWrapper.appendChild(photoPreview);
            photoWrapper.appendChild(deleteButton);
            photoContainer.appendChild(photoWrapper);
        };

        reader.readAsDataURL(file);
    });
});

function updateFileInput(files) {
    if (files.length === 0) {
        document.getElementById('photoInput').value = '';
        return;
    }
    const dataTransfer = new DataTransfer();
    files.forEach(file => dataTransfer.items.add(file));
    document.getElementById('photoInput').files = dataTransfer.files;
}

document.getElementById('postButton').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    const photos = document.querySelectorAll('#photoContainer img');
    const caption = document.getElementById('caption').value;

    // Validation to check if photos are uploaded
    if (photos.length === 0) {
        alert('Please upload a photo.');
        return;
    }

    // Validation to check if caption is entered
    if (!caption) {
        alert('Please enter a caption.');
        return;
    }


    // Gather selected social media platforms
    selectedSocialMedia = [];
    if (document.getElementById('linkedinCheckbox').checked) {
        selectedSocialMedia.push('LinkedIn');
    }
    if (document.getElementById('twitterCheckbox').checked) {
        selectedSocialMedia.push('Twitter');
    }

    // Validation to check if at least one social media platform is selected
    if (selectedSocialMedia.length === 0) {
        alert('Please select at least one social media platform.');
        return;
    }


    // Prepare FormData to send via fetch
    const input = document.getElementById('photoInput');
    let formData = new FormData();
    for (const file of input.files) {
        formData.append('images', file); // Append each selected file
    }
    formData.append('context', caption);
    formData.append('socialMedia', selectedSocialMedia); // Add selected social media to form data

    const uploadStatus = document.getElementById('uploadStatus');
    uploadStatus.style.display = 'block';

    console.log(`${window.location.origin}/upload`)
    // Make the POST request to the server
    fetch(`${window.location.origin}/upload`, {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            console.log(formData)
            console.log("Response received");
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json(); // Parse JSON response body
        })
        .then(data => {
            console.log("Upload successful");
            console.log(data);

            
            // Hide the uploading status before showing the alert
            uploadStatus.style.display = 'none';

            // Remove any previous links
            const previousLinks = document.querySelectorAll('.uploadedLink');
            previousLinks.forEach(link => link.remove());

            // Create a container for the new links and messages
            const linkContainer = document.getElementById('linkContainer');
            linkContainer.innerHTML = "<h1>Links</h1>"

            // Iterate over the data array and create links or messages
            data.forEach(item => {

                console.log(item)
                if (item.success) {
                    // Create a link if success is true
                    const link = document.createElement('a');
                    link.className = 'uploadedLink';  // Assign a class to the new link
                    link.href = item.message || item.url;  // Set the URL as the link target
                    link.textContent = item.method;  // Text of the link (method name)
                    link.style.display = 'block'; // Make sure it's on a new line if needed
                    link.target = '_blank'; // Optional: opens the link in a new tab
                    linkContainer.appendChild(link); // Append the link to the container
                    console.log(linkContainer)
                } else {
                    // Create a message if success is false
                    const message = document.createElement('p');
                    message.className = 'uploadedLink';
                    message.textContent = `${item.method}: ${item.message}`;
                    message.style.color = 'red'; // Optional: make the text red for visibility
                    linkContainer.appendChild(message); // Append the message to the container
                }
            });

            selectedFiles = []; // Clear the selected files array
            document.getElementById('photoInput').value = ''; // Clear the file input
            document.getElementById('photoContainer').innerHTML = ''; // Clear the photo container
            document.getElementById('caption').value = ''; // Clear the caption input
            // link.remove(); // Remove the new link after successful post

            selectedSocialMedia = []; // Clear the selected social media
            document.querySelectorAll('.social-media-selection input[type="checkbox"]').forEach(checkbox => checkbox.checked = false); // Uncheck all checkboxes

            // Use setTimeout to ensure the DOM is updated before showing the alert
            setTimeout(() => {
                alert(`Post submitted successfully! Click the link below.`);
            }, 3);
        })
        .catch(error => {
            console.error('Error:', error);
            setTimeout(() => {
                alert('Failed to submit the post.');
            }, 3);
            // Hide the uploading status before showing the alert
            uploadStatus.style.display = 'none';
        });
});