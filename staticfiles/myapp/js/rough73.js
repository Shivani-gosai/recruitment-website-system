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

// function submitPost() {
//   const author = document.getElementById('postAuthor').value;
//   const content = document.getElementById('postContent').value;
//   const fileInput = document.getElementById('postFile').files[0];
//   const postsContainer = document.getElementById('postsContainer');
//   const noPostsMessage = document.getElementById('noPostsMessage');

//   if (author && content) {
//     const postCard = document.createElement('div');
//     postCard.className = 'post-card';

//     postCard.innerHTML = `
//     {% for post in posts %}
//       <div class="post-header">
//         <img src="https://via.placeholder.com/60" alt="Post Logo" class="post-logo">
//         <div>
//           <p class="auth">{{ post.posttitle }}</p>
//           <span>Just now</span>
//         </div>
//       </div>
//       <p>{{ post.postdesc }}</p>
//       {% if post.postcontent %}
//       <img src="{{ post.postcontent.url }}" alt="Post Image" class="post-image" style="display: none;">
//       <div class="post-stats">
//         <button onclick="toggleLike(this)" class="heart"><i class="fa-regular fa-heart" style="color: #000000;"></i></button> <span class="like-count">0</span>
//       </div>
//       {% endif %}
//       {% empty %}
//           <p>No posts available.</p>
//           {% endfor %}
//       <div class="comment-section">
//         <input type="text" class="comment-input" placeholder="Add a comment (username: comment)" onkeydown="addComment(event, this, '${author}')">
//         <ul class="comment-list"></ul>
//       </div>
     
//       // <div class="post-cards">
//       //   {% for post in posts %}
//       //     <div class="post-card">
//       //       <h3>{{ post.posttitle }}</h3>
//       //       <p>{{ post.postdesc }}</p>
//       //       {% if post.postcontent %}
//       //       <img src="{{ post.postcontent.url }}" alt="Post Image">
//       //       {% endif %}
//       //     </div>
//       //     {% empty %}
//       //     <p>No posts available.</p>
//       //     {% endfor %}
//       // </div>
//     `;

//     if (fileInput) {
//       const reader = new FileReader();
//       reader.onload = function (e) {
//         const postImage = postCard.querySelector('.post-image');
//         postImage.src = e.target.result;
//         postImage.style.display = 'block';
//       };
//       reader.readAsDataURL(fileInput);
//     }

//     postsContainer.prepend(postCard);
//     if (noPostsMessage) {
//       noPostsMessage.style.display = 'none';
//     }
//     document.getElementById('addPostForm').reset();
//     closePopup();
//   } else {
//     alert('Please fill in all required fields.');
//   }
// }
//follow button
const button = document.querySelector(".follow-button");
let isFollowing = false;

button.addEventListener("click", () => {
    isFollowing = !isFollowing;
    button.textContent = isFollowing ? "Following" : "Follow";
    button.style.backgroundColor = isFollowing ? " #0a66c2" : " #0a66c2";
});

//new
/*document.addEventListener("DOMContentLoaded", function () {
  fetchAndRenderPosts();
});

function fetchAndRenderPosts() {
  fetch('/get_posts/')
      .then(response => response.json())
      .then(posts => {
          console.log("📢 API Response:", posts); // 🔍 Debugging API Response
          let postContainer = document.getElementById("postsContainer");
          let postTemplate = document.getElementById("postTemplate");

          postContainer.innerHTML = ""; // Clear previous content

          if (!posts.length) {
              postContainer.innerHTML = "<p>No posts available.</p>";
              return;
          }

          posts.forEach(post => {
              let newPost = postTemplate.cloneNode(true);
              newPost.style.display = "block";  // Make visible
              newPost.classList.remove("template"); // Remove template class
              newPost.removeAttribute("id");  // Prevent duplicate IDs

              // ✅ Set post details
              newPost.querySelector(".auth").textContent = post.username || "Unknown User";
              newPost.querySelector(".post-desc").textContent = post.postdesc || "";

              // ✅ Handle post image
              let imgElement = newPost.querySelector(".post-image");
              if (post.postcontent) {
                  imgElement.src = `/media/${post.postcontent}`;
                  imgElement.style.display = "block";
              }

              // ✅ Handle likes
              let likeButton = newPost.querySelector(".heart");
              let likeCount = newPost.querySelector(".like-count");

              likeButton.addEventListener("click", function () {
                  let count = parseInt(likeCount.textContent);
                  if (likeButton.classList.contains("liked")) {
                      likeCount.textContent = count - 1;
                      likeButton.classList.remove("liked");
                  } else {
                      likeCount.textContent = count + 1;
                      likeButton.classList.add("liked");
                  }
              });

              // ✅ Handle delete button
              let deleteButton = newPost.querySelector(".delete-btn");
              deleteButton.addEventListener("click", function () {
                  deletePost(post.id, newPost);
              });

              // ✅ Append new post
              postContainer.appendChild(newPost);
          });
      })
      .catch(error => console.error("❌ Error loading posts:", error));
}

// ✅ Delete post function
function deletePost(postId, postElement) {
  if (confirm("Are you sure you want to delete this post?")) {
      fetch(`/delete_post/${postId}/`, {
          method: "DELETE",
          headers: {
              "X-CSRFToken": getCSRFToken() // Security token for Django
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.message) {
              console.log("✅ Post deleted:", data.message);
              postElement.remove();  // Remove from UI
          } else {
              console.error("❌ Delete failed:", data.error);
          }
      })
      .catch(error => console.error("❌ Delete error:", error));
  }
}

// ✅ Function to get CSRF token (for security)
function getCSRFToken() {
  let cookieValue = null;
  let cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.startsWith("csrftoken=")) {
          cookieValue = cookie.substring("csrftoken=".length, cookie.length);
          break;
      }
  }
  return cookieValue;
}*/

document.addEventListener("DOMContentLoaded", function () {
    fetchPosts();
});

function fetchPosts() {
    fetch('/get_posts/')
        .then(response => {
            if (!response.ok) throw new Error("Server error");
            return response.json();
        })
        .then(posts => {
            const postContainer = document.getElementById("postsContainer");
            const postTemplate = document.getElementById("postTemplate");

            if (!postContainer || !postTemplate) {
                console.error("Template or container not found.");
                return;
            }

            postContainer.innerHTML = ""; // Clear existing

            posts.forEach(post => {
                const newPost = postTemplate.cloneNode(true);
                newPost.style.display = "block";
                newPost.classList.remove("template");

                newPost.querySelector(".auth").textContent = post.username;
                newPost.querySelector(".post-time").textContent = post.postdttime;
                newPost.querySelector(".post-desc").textContent = post.postdesc;

                if (post.postcontent) {
                    const img = newPost.querySelector(".post-image");
                    img.src = `/media/${post.postcontent}`;
                    img.style.display = "block";
                }

                postContainer.appendChild(newPost);
            });
        })
        .catch(error => console.error("Failed to load posts:", error));
}

  function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.startsWith("csrftoken=")) {
        cookieValue = cookie.substring("csrftoken=".length, cookie.length);
        break;
      }
    }
    return cookieValue;
  }