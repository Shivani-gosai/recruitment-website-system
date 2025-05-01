/*function goBack() {
    //window.history.back(); // Go back to the previous page
    window.location.href='new_profile.html';
}*/
/*display posts from demo2.html*/
const modals = document.querySelectorAll(".modal");
const buttons = document.querySelectorAll(".open-modal");

buttons.forEach(button => {
  button.addEventListener("click", () => {
    const modalId = button.getAttribute("data-modal");
    document.getElementById(modalId).style.display = "block";
  });
});

modals.forEach(modal => {
  modal.querySelector(".close").addEventListener("click", () => {
    modal.style.display = "none";
  });

  modal.addEventListener("click", event => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });

  const likeBtn = modal.querySelector(".likeBtn");
  let liked = false;

  likeBtn.addEventListener("click", function () {
    const likeCount = this.querySelector(".likeCount");
    let count = parseInt(likeCount.textContent);

    if (!liked) {
      count++;
      likeCount.textContent = count;
      this.querySelector("i").classList.remove("fa-regular");
      this.querySelector("i").classList.add("fa-solid");
      this.querySelector("i").style.color = "red";
      liked = true;
    } else {
      count--;
      likeCount.textContent = count;
      this.querySelector("i").classList.remove("fa-solid");
      this.querySelector("i").classList.add("fa-regular");
      this.querySelector("i").style.color = "";
      liked = false;
    }
  });

  const addCommentBtn = modal.querySelector(".addCommentBtn");
  const commentInput = modal.querySelector("textarea");
  const commentsSection = modal.querySelector(".comments");

  addCommentBtn.addEventListener("click", () => {
    if (commentInput.value.trim()) {
      const comment = document.createElement("div");
      comment.classList.add("comment");
      comment.innerHTML = `
        <img class="profile-pic" src="C:/Users/gosai/OneDrive/Documents/OneDrive/Pictures/Saved Pictures/im2.jpg" alt="Profile">
        <div class="comment-details">
          <span class="username">Username</span>
          <p>${commentInput.value}</p>
        </div>
      `;
      commentsSection.appendChild(comment);
      commentInput.value = "";
    }
  });
});