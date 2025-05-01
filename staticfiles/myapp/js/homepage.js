let currentIndex = 0;
let likeCount = 0;
let liked = false;
function openPopup(popupId) {
    document.getElementById(popupId).style.display = "flex";
    document.querySelector(".overlay").style.display = "block"; // Show overlay
}

function closePopup(popupId) {
    document.getElementById(popupId).style.display = "none";
    document.querySelector(".overlay").style.display = "none"; // Hide overlay
}

// Like Button Toggle
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".heart").forEach(heartIcon => {
        let likeCountElem = heartIcon.closest(".nav-buttons").querySelector(".like-count");
        let likeCount = parseInt(heartIcon.getAttribute("data-likes")) || 0;

        // Ensure initial count is displayed
        likeCountElem.textContent = likeCount;

        heartIcon.addEventListener("click", function () {
            let isLiked = this.getAttribute("data-liked") === "true";

            if (isLiked) {
                likeCount--; // Unlike
                this.setAttribute("data-liked", "false");
                this.classList.remove("fa-solid");
                this.classList.add("fa-regular");
                this.style.color = "#000000";
            } else {
                likeCount++; // Like
                this.setAttribute("data-liked", "true");
                this.classList.remove("fa-regular");
                this.classList.add("fa-solid");
                this.style.color = "#f21707";
            }

            // Update attributes and UI
            this.setAttribute("data-likes", likeCount);
            likeCountElem.textContent = likeCount;
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".addCommentBtn").forEach(button => {
        button.addEventListener("click", function () {
            let popup = this.closest(".popup");  // Get the parent popup
            let commentInput = popup.querySelector(".comment-input textarea");
            let commentsSection = popup.querySelector(".comments");

            let commentText = commentInput.value.trim();
            if (commentText) {
                const comment = document.createElement("div");
                comment.classList.add("comment");

                const profilePic = document.createElement("img");
                profilePic.classList.add("profile-pic");
                profilePic.src = "C:/Users/gosai/OneDrive/Documents/OneDrive/Desktop/SDP Project/Developing/extra/im1.jpg";  
                profilePic.alt = "Profile";

                const commentDetails = document.createElement("div");
                commentDetails.classList.add("comment-details");

                const username = document.createElement("span");
                username.classList.add("username");
                username.textContent = "Username";

                const commentTextElement = document.createElement("p");
                commentTextElement.textContent = commentText;
                //let paragraph = document.querySelector("p"); // Select the first <p> tag
                commentTextElement.classList.add("pcomment"); // Add class "myClass"


                commentDetails.appendChild(username);
                commentDetails.appendChild(commentTextElement);
                comment.appendChild(profilePic);
                comment.appendChild(commentDetails);

                commentsSection.appendChild(comment);
                commentInput.value = "";  // Clear input field
            }
        });
    });
});


/*three button popup*/
document.addEventListener("DOMContentLoaded", function () {
    let menuButton = document.querySelector(".menu-btn");
    let menuPopup = document.querySelector(".menu-popup");

    menuButton.addEventListener("click", function (event) {
        menuPopup.style.display = menuPopup.style.display === "block" ? "none" : "block";
        event.stopPropagation();
    });

    // Close menu when clicking outside
    document.addEventListener("click", function () {
        menuPopup.style.display = "none";
    });

    // Prevent closing when clicking inside menu
    menuPopup.addEventListener("click", function (event) {
        event.stopPropagation();
    });
});
/*search user*/
function searchUser() {
    let searchInput = document.getElementById("search2").value.toLowerCase();
    let users = document.querySelectorAll(".user");
    let userList = document.getElementById("userList");
    let foundUser = null;

    users.forEach(user => {
        let username = user.textContent.toLowerCase();
        user.classList.remove("highlight");

        if (username.includes(searchInput) && searchInput !== "") {
            user.classList.add("highlight"); // Highlight found user
            foundUser = user;
        }
    });

    if (foundUser) {
        userList.prepend(foundUser); // Move found user to the top
        document.getElementById("result").textContent = ""; // Clear "Not Found" message
    } else {
        document.getElementById("result").textContent = " - Not Found.";
    }
}

