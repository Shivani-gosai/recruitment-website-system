function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show the selected section
    const selectedSection = document.getElementById(sectionId);
    selectedSection.classList.add('active');

    // Add active class to the clicked tab
    const selectedTab = document.querySelector(`a[href="#${sectionId}"]`);
    selectedTab.classList.add('active');
}

// Redirect to the About section
function redirectToAbout() {
    showSection('about');
}

function redirectToPosts() {
    // Hide all sections
    document.querySelectorAll(".content-section").forEach(section => section.classList.remove("active"));

    // Show the "Posts" section
    document.getElementById("posts").classList.add("active");

    // Update active tab
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
    document.querySelector("[href='#posts']").classList.add("active");
}

function redirectToJobs() {
    // Hide all sections
    document.querySelectorAll(".content-section").forEach(section => section.classList.remove("active"));

    // Show the "Jobs" section
    document.getElementById("jobs").classList.add("active");

    // Update active tab
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
    document.querySelector("[href='#jobs']").classList.add("active");
}

//post page back to home button code
 //function goBack()
// {
  //  window.location.herf='C:\project\desgin\rough73.html';
 //}
 const tabs = document.querySelectorAll('.nav-tabs .tab');

 // Check for the current URL to set the active tab (useful for navigation)
 const currentPath = window.location.pathname;
 
 // Function to dynamically set active tab
 function setActiveTab() {
     tabs.forEach(tab => {
         const href = tab.getAttribute('href');
         if (currentPath.includes(href)) {
             tab.classList.add('active');
         } else {
             tab.classList.remove('active');
         }
     });
 }
 
 // Add click listener to update active class without relying on URL
 tabs.forEach(tab => {
     tab.addEventListener('click', function (e) {
         tabs.forEach(t => t.classList.remove('active')); // Remove active class from all tabs
         this.classList.add('active'); // Add active class to the clicked tab
     });
 });
 
 // Set active tab based on the current URL (important for page reloads)
 setActiveTab();

 //job page::
 // Example: Updating job count dynamically
const jobCountElement = document.getElementById('job-count');
const totalJobs = 9057;

document.addEventListener('DOMContentLoaded', () => {
    jobCountElement.textContent = totalJobs.toLocaleString();
});

function navigateToJob(jobTitle) {
    // Create a URL parameter to pass the job title (optional)
    const jobPageUrl = `linkjob.html?title=${encodeURIComponent(jobTitle)}`;
    window.location.href = jobPageUrl;
}

document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.nav-tabs .tab');

    tabs.forEach(tab => {
        tab.addEventListener('click', (event) => {
            event.preventDefault();
            const targetPage = tab.getAttribute('href');
            if (targetPage) {
                window.location.href = targetPage;
            }
        });
    });
});


//SEARCH FUNCTIONAKITY

document.addEventListener("DOMContentLoaded", function () {
  const searchButton = document.querySelector(".search-bar button");
  const searchInput = document.querySelector(".search-bar input");
  const jobCards = document.querySelectorAll(".job-card");

  searchButton.addEventListener("click", function () {
      const query = searchInput.value.toLowerCase();
      
      jobCards.forEach(job => {
          const jobTitle = job.querySelector("h4").textContent.toLowerCase();
          const jobLocation = job.querySelector("p:nth-child(4)").textContent.toLowerCase();
          
          if (jobTitle.includes(query) || jobLocation.includes(query)) {
              job.style.display = "block";
          } else {
              job.style.display = "none";
          }
      });
  });

  searchInput.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
          searchButton.click();
      }
  });
});

//LINKJOB PAGE

document.querySelectorAll(".job-card").forEach(card => {
  card.addEventListener("click", function() {
      window.location.href = this.getAttribute("data-url");
  });
});

// ADD POST POP-UP

function openPopup() {
    document.getElementById('addPostPopup').style.display = 'flex';
  }

  function closePopup() {
    document.getElementById('addPostPopup').style.display = 'none';
  }

  function submitPost() {
    const author = document.getElementById('postAuthor').value;
    const content = document.getElementById('postContent').value;
    const fileInput = document.getElementById('postFile').files[0];
    const postsContainer = document.getElementById('postsContainer');
    const noPostsMessage = document.getElementById('noPostsMessage');

    if (author && content) {
      const postCard = document.createElement('div');
      postCard.className = 'post-card';

      postCard.innerHTML = `
        <div class="post-header">
          <img src="https://via.placeholder.com/60" alt="Post Logo" class="post-logo">
          <div>
            <p>${author}</p>
            <span>Just now</span>
          </div>
        </div>
        <p>${content}</p>
        <img src="" alt="Post Image" class="post-image" style="display: none;">
        <div class="post-stats">
          <button onclick="toggleLike(this)" class="heart">❤</button> <span class="like-count">0 likes</span>
        </div>
        <div class="comment-section">
          <input type="text" class="comment-input" placeholder="Add a comment (username: comment)" onkeydown="addComment(event, this, '${author}')">
          <ul class="comment-list"></ul>
        </div>
      `;

      if (fileInput) {
        const reader = new FileReader();
        reader.onload = function (e) {
          const postImage = postCard.querySelector('.post-image');
          postImage.src = e.target.result;
          postImage.style.display = 'block';
        };
        reader.readAsDataURL(fileInput);
      }

      postsContainer.prepend(postCard);
      if (noPostsMessage) {
        noPostsMessage.style.display = 'none';
      }
      document.getElementById('addPostForm').reset();
      closePopup();
    } else {
      alert('Please fill in all required fields.');
    }
  }
  function toggleLike(button) {
    button.classList.toggle('liked');
    const likeCount = button.nextElementSibling;
    let count = parseInt(likeCount.textContent);
    count = button.classList.contains('liked') ? count + 1 : count - 1;
    likeCount.textContent = count;
  }

  function addComment(event, input, postAuthor) {
    if (event.key === 'Enter' && input.value.trim()) {
      const commentList = input.nextElementSibling;
      const comment = document.createElement('li');

      // Assuming the user inputs in the format: "username: comment"
      const commentText = input.value.trim();
      const [username, commentContent] = commentText.split(':').map(s => s.trim());

      if (username && commentContent) {
        comment.innerHTML = `<strong>${username}:</strong> ${commentContent}`;
      } else {
        comment.innerHTML = `<strong>${postAuthor}:</strong> ${commentText}`;
      }

      commentList.appendChild(comment);
      input.value = '';
    }
  }

// Call this function to check and display the "No posts yet" message if there are no posts
function checkNoPosts() {
    const postsContainer = document.getElementById('postsContainer');
    const noPostsMessage = document.getElementById('noPostsMessage');
  
    if (!postsContainer || !noPostsMessage) {
      console.warn("Element not found: 'postsContainer' or 'noPostsMessage' is missing.");
      return;  // Stop execution if elements are missing
    }
  
    noPostsMessage.style.display = postsContainer.children.length === 0 ? 'block' : 'none';
  }
  
// Call checkNoPosts() on page load to initialize the message
document.addEventListener('DOMContentLoaded', checkNoPosts);
  
 


document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".nav ul li a");

  links.forEach(link => {
      link.addEventListener("click", () => {
          // Highlight the active link
          links.forEach(item => item.classList.remove("active"));
          link.classList.add("active");
      });
  });

  console.log("About page script loaded successfully!");
});


//company about page edit button
//logo edit 


//image edit

document.addEventListener("DOMContentLoaded", function () {
    // Load saved image from localStorage
    const savedImage = localStorage.getItem("savedImage");
    if (savedImage) {
        document.querySelector(".image-container img").src = savedImage;
    }
});

//footer edit
document.addEventListener("DOMContentLoaded", function () {
    const footerText = document.getElementById("footer-text");
    const footerEditBtn = document.getElementById("footer-edit-btn");

    document.addEventListener("DOMContentLoaded", function () {
        const someElement = document.getElementById('someElementID');
        if (someElement) {
          someElement.addEventListener("click", function () {
            console.log("Element clicked!");
          });
        } else {
          console.warn("Element with ID 'someElementID' not found.");
        }
      });
      
});

//add job card
document.addEventListener("DOMContentLoaded", function () {
    const openFormBtn = document.getElementById("openJobForm");
    const closeFormBtn = document.getElementById("closeJobForm");
    const jobForm = document.getElementById("jobForm");
    const submitJobBtn = document.getElementById("submitJob");

    const jobTitleInput = document.getElementById("jobTitle");
    const companyNameInput = document.getElementById("companyName");
    const locationInput = document.getElementById("location");
    const datePostedInput = document.getElementById("datePosted");

    const recommendedJobs = document.querySelector(".job-cards");

    // Show the job form
    openFormBtn.addEventListener("click", function () {
        jobForm.style.display = "block";
    });

    // Hide the job form
    closeFormBtn.addEventListener("click", function () {
        jobForm.style.display = "none";
    });

    // Add job on form submit
    submitJobBtn.addEventListener("click", function () {
        const jobTitle = jobTitleInput.value.trim();
        const companyName = companyNameInput.value.trim();
        const location = locationInput.value.trim();
        const datePosted = datePostedInput.value.trim();

        if (!jobTitle || !companyName || !location || !datePosted) {
            alert("Please fill in all fields!");
            return;
        }

        // Create new job card
        const jobCard = document.createElement("div");
        jobCard.classList.add("job-card");

        jobCard.innerHTML = `
            <img src="https://cdn.iconscout.com/icon/free/png-256/microsoft-47-722716.png" alt="Company Logo">
            <h4>${jobTitle}</h4>
            <p>${companyName}</p>
            <p>${location}</p>
            <span class="date">${datePosted}</span>
            <button class="delete-job btn btn-danger">Delete</button>
        `;

        recommendedJobs.appendChild(jobCard);

        // Clear form inputs
        jobTitleInput.value = "";
        companyNameInput.value = "";
        locationInput.value = "";
        datePostedInput.value = "";

        // Close form
        jobForm.style.display = "none";

        // Add delete function to remove job card
        jobCard.querySelector(".delete-job").addEventListener("click", function () {
            recommendedJobs.removeChild(jobCard);
        });
    });
});
//follow button
const button = document.querySelector(".follow-button");
  let isFollowing = false;

  button.addEventListener("click", () => {
    isFollowing = !isFollowing;
    button.textContent = isFollowing ? "Following" : "Follow";
    button.style.backgroundColor = isFollowing ? " #0a66c2" : " #0a66c2";
  });

    function addItem() {
    var input = document.getElementById("listItemInput");
    var list = document.getElementById("modalItemList"); // Target modal's list

    if (input.value.trim() !== "") {
        var li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";
        li.innerHTML = `
            ${input.value}
            <button class="btn btn-danger btn-sm" onclick="removeItem(this)">Remove</button>
        `;
        list.appendChild(li);
        input.value = ""; // Clear input field after adding
    }
}

function removeItem(button) {
    button.parentElement.remove();
}
//django
document.addEventListener("DOMContentLoaded", function () {
  let valuesListElement = document.getElementById("values-list");
  let newValueInput = document.getElementById("newValueInput");
  let addValueBtn = document.getElementById("addValueBtn");
  let saveValuesBtn = document.getElementById("saveValuesBtn");
  let editValuesBtn = document.getElementById("editValuesBtn");
  let valuesTextarea = document.getElementById("valuesTextarea");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  let valuesArray = [];

  // Load existing values
  if (valuesTextarea.value) {
      try {
          valuesArray = JSON.parse(valuesTextarea.value);
      } catch (e) {
          console.error("Error parsing JSON:", e);
      }
  }

  // Function to update the displayed values list
  function updateValuesList() {
      valuesListElement.innerHTML = ""; 
      valuesArray.forEach(value => {
          let li = document.createElement("li");
          li.textContent = value.trim();
          valuesListElement.appendChild(li);
      });
      valuesTextarea.value = JSON.stringify(valuesArray);
  }

  // Add new value to the list
  addValueBtn.addEventListener("click", function () {
      let newValue = newValueInput.value.trim();
      if (newValue) {
          valuesArray.push(newValue);
          updateValuesList();
          newValueInput.value = ""; 
          saveValuesBtn.style.display = "inline-block"; 
      }
  });

  // Save values to the backend
  saveValuesBtn.addEventListener("click", function () {
      fetch("/update_org_details/", {
          method: "POST",
          headers: {
              "X-CSRFToken": csrfToken,
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ values: valuesArray }) 
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert("Updated successfully!");
              saveValuesBtn.style.display = "none";
              editValuesBtn.style.display = "inline-block"; 
          } else {
              alert("Error updating: " + data.error);
          }
      })
      .catch(error => console.error("Error:", error));
  });

  // Enable editing after saving
  editValuesBtn.addEventListener("click", function () {
      editValuesBtn.style.display = "none";
      saveValuesBtn.style.display = "inline-block";
  });

  // Initialize values on page load
  updateValuesList();
});

document.addEventListener("DOMContentLoaded", function () {
  const missionText = document.getElementById("mission-text");
  const missionTextarea = document.getElementById("missionTextarea");
  const editMissionBtn = document.getElementById("editMissionBtn");
  const saveMissionBtn = document.getElementById("saveMissionBtn");

  const visionText = document.getElementById("vision-text");
  const visionTextarea = document.getElementById("visionTextarea");
  const editVisionBtn = document.getElementById("editVisionBtn");
  const saveVisionBtn = document.getElementById("saveVisionBtn");

  if (!missionText || !missionTextarea || !editMissionBtn || !saveMissionBtn ||
      !visionText || !visionTextarea || !editVisionBtn || !saveVisionBtn) {
      console.warn("❗ Some Mission/Vision DOM elements are missing.");
      return;
  }

  if (typeof csrfToken === "undefined" || typeof cmpaboutUrl === "undefined") {
      console.error("❌ csrfToken or cmpaboutUrl not defined in template.");
      return;
  }

  editMissionBtn.addEventListener("click", () => {
      missionTextarea.style.display = "block";
      saveMissionBtn.style.display = "inline-block";
      editMissionBtn.style.display = "none";
  });

  saveMissionBtn.addEventListener("click", () => {
      const newMission = missionTextarea.value;
      console.log("📤 Saving Mission:", newMission);

      fetch(cmpaboutUrl, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken
          },
          body: JSON.stringify({ mission: newMission })
      })
      .then(async res => {
          if (!res.ok) throw new Error("Request failed");
          const data = await res.json();
          if (data.success) {
              missionText.textContent = newMission;
              missionTextarea.style.display = "none";
              saveMissionBtn.style.display = "none";
              editMissionBtn.style.display = "inline-block";
          } else {
              alert("Failed to save mission.");
          }
      })
      .catch(err => console.error("Error saving mission:", err));
  });

  editVisionBtn.addEventListener("click", () => {
      visionTextarea.style.display = "block";
      saveVisionBtn.style.display = "inline-block";
      editVisionBtn.style.display = "none";
  });

  saveVisionBtn.addEventListener("click", () => {
      const newVision = visionTextarea.value;
      console.log("📤 Saving Vision:", newVision);

      fetch(cmpaboutUrl, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken
          },
          body: JSON.stringify({ vision: newVision })
      })
      .then(async res => {
          if (!res.ok) throw new Error("Request failed");
          const data = await res.json();
          if (data.success) {
              visionText.textContent = newVision;
              visionTextarea.style.display = "none";
              saveVisionBtn.style.display = "none";
              editVisionBtn.style.display = "inline-block";
          } else {
              alert("Failed to save vision.");
          }
      })
      .catch(err => console.error("Error saving vision:", err));
  });
});
