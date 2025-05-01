// Summary editing functions
function enableEdit1() {
    const editableDiv1 = document.getElementById('editableText1');
    const textField1 = document.getElementById('textField1');

    // Set textarea value to current div text
    textField1.value = editableDiv1.textContent;
    editableDiv1.style.display = 'none'; // Hide div
    textField1.classList.remove('hidden1'); // Show textarea
    textField1.focus();
}

function updateText1() {
    const editableDiv1 = document.getElementById('editableText1');
    const textField1 = document.getElementById('textField1');

    // Set div text to textarea value
    editableDiv1.textContent = textField1.value;
    textField1.classList.add('hidden1'); // Hide textarea
    editableDiv1.style.display = 'block'; // Show div
}

document.addEventListener('DOMContentLoaded', function() {
    // Retrieve and display data from localStorage
    const experienceHTML = localStorage.getItem('cvExperience') || '<p>No experience added.</p>';
    const educationHTML = localStorage.getItem('cvEducation') || '<p>No education details added.</p>';
    const skillsHTML = localStorage.getItem('cvSkills') || '<p>No skills added.</p>';
    const languagesHTML = localStorage.getItem('cvLanguages') || '<p>No languages added.</p>';
    const linksHTML = localStorage.getItem('cvLinks') || '<p>No links added.</p>';

    // Insert content into the appropriate sections
    document.querySelector('.Experience .editable3').innerHTML = experienceHTML;
    document.querySelector('.Education .editable4').innerHTML = educationHTML;
    document.querySelector('.Skills .editable5').innerHTML = skillsHTML;
    document.querySelector('.Languages .editable7').innerHTML = languagesHTML;
    document.querySelector('.Links .editable6').innerHTML = linksHTML; // Update links section
});
/post pop-up/
// Function to open the modal
function openModal() {
    document.getElementById("createPostModal").style.display = "flex"; // Show the modal
}

// Function to close the modal
function closeModal() {
    document.getElementById("createPostModal").style.display = "none"; // Hide the modal
}

// Function to handle media preview
function previewMedia() {
    const fileInput = document.getElementById('fileInput');
    const mediaPreview = document.getElementById('mediaPreview');
    const fileError = document.getElementById('fileError');
    
    // Clear previous media
    mediaPreview.innerHTML = '';
    fileError.style.display = 'none';

    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            const mediaType = file.type.split('/')[0];
            
            if (mediaType === 'image') {
                const img = document.createElement('img');
                img.src = e.target.result;
                mediaPreview.appendChild(img);
            } else if (mediaType === 'video') {
                const video = document.createElement('video');
                video.src = e.target.result;
                video.controls = true;
                mediaPreview.appendChild(video);
            } else {
                fileError.style.display = 'block'; // Show error if not a valid image/video
            }
        }
        reader.readAsDataURL(file);
    }
}
/display post/
// Function to handle post submission and display the new post
let postCount = 0; // Initialize post count
const maxPosts = 3; // Maximum number of posts to display

function submitPost() {
    const postCaption = document.getElementById('postCaption').value;
    const fileInput = document.getElementById('fileInput').files[0];
    const postsContainer = document.getElementById('postsContainer');

    if (!fileInput && !postCaption.trim()) {
        alert('Please add either a caption or an image/video.');
        return;
    }

    // If the number of posts is already at the limit, display "See More Posts"
    if (postCount >= maxPosts) {
        const seeMoreLink = document.getElementById('seeMoreLink');
        if (!seeMoreLink) {
            const seeMore = document.createElement('div');
            seeMore.id = 'seeMoreLink';
            seeMore.innerHTML = '<a href="see_all_posts.html" onclick="showAllPosts()">See All Posts</a>';
            postsContainer.appendChild(seeMore);
            closeModal();
        }
        // alert('You have reached the maximum number of visible posts. See More Posts to view additional posts.');
        return;
    }

    // Create a new post element
    const postItem = document.createElement('div');
    postItem.classList.add('post-item');

    // Add media preview to the post
    const mediaPreview = document.createElement('div');
    mediaPreview.classList.add('media-preview');

    if (fileInput) {
        const fileReader = new FileReader();

        fileReader.onload = function (e) {
            const mediaType = fileInput.type.split('/')[0];

            if (mediaType === 'image') {
                const img = document.createElement('img');
                img.src = e.target.result;
                mediaPreview.appendChild(img);
            } else if (mediaType === 'video') {
                const video = document.createElement('video');
                video.src = e.target.result;
                video.controls = true;
                mediaPreview.appendChild(video);
            } else {
                alert('Unsupported file type');
            }

            postItem.appendChild(mediaPreview);

            // Add caption to the post
            const caption = document.createElement('div');
            caption.classList.add('caption');
            caption.textContent = postCaption;
            postItem.appendChild(caption);

            // Append the post to the posts container
            postsContainer.prepend(postItem);

            // Increment post count
            postCount++;

            // Clear the modal and reset the fields
            document.getElementById('postCaption').value = '';
            document.getElementById('fileInput').value = '';
            document.getElementById('mediaPreview').innerHTML = '';
            closeModal(); // Close the modal
        };
        fileReader.readAsDataURL(fileInput);
    }
}
// Function to display all posts when "See More Posts" is clicked
function showAllPosts() {
    const postsContainer = document.getElementById('postsContainer');
    const seeMoreLink = document.getElementById('seeMoreLink');
    if (seeMoreLink) {
        seeMoreLink.remove(); // Remove "See More Posts" link
    }
    // Display all posts (if hidden logic is implemented for extra posts)
    // For now, it only removes the restriction to add more posts
    window.location.href = 'see_all_posts.html';
}