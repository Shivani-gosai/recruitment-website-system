// Edit button functionality
const editButton = document.querySelector('.edit-button');
const editableElements = document.querySelectorAll('.editable');

editButton.addEventListener('click', () => {
  const isEditing = editableElements[0].getAttribute('contenteditable') === 'true';

  if (isEditing) {
    // Turn off editing
    editableElements.forEach(element => element.setAttribute('contenteditable', 'false'));
    editButton.textContent = '✏️ Edit'; // Change button text back to Edit
  } else {
    // Turn on editing
    editableElements.forEach(element => element.setAttribute('contenteditable', 'true'));
    editButton.textContent = '💾 Save'; // Change button text to Save
  }
});

// Move to Draft functionality
const moveToDraftButtons = document.querySelectorAll('.move-draft');
const draftContainer = document.getElementById('draft-applicants');
const appliedApplicantsContainer = document.getElementById('applied-applicants');

moveToDraftButtons.forEach(button => {
  button.addEventListener('click', (event) => {
    const applicantId = button.getAttribute('data-id');
    const applicantCard = document.getElementById(applicantId);

    // Move applicant card to the draft section
    draftContainer.appendChild(applicantCard);

    // Remove the "Move to Draft" button after moving the card to the draft section
    button.remove();

    // Update draft container message if no drafts existed before
    if (draftContainer.querySelector('p')) {
      draftContainer.querySelector('p').remove();
    }

    // You can add a confirmation message or visual feedback if needed
    console.log(`Applicant ${applicantId} moved to draft.`);
  });
});

// Schedule Interview functionality
const scheduleButtons = document.querySelectorAll('.schedule-interview');
const modal = document.getElementById('schedule-modal');
const closeModal = document.querySelector('.close');
const scheduleForm = document.getElementById('schedule-form');

// Open the modal when clicking the "Schedule Interview" button
scheduleButtons.forEach(button => {
  button.addEventListener('click', () => {
    modal.style.display = 'block'; // Show the modal
    const applicantId = button.getAttribute('data-id');
    scheduleForm.setAttribute('data-applicant-id', applicantId); // Store applicant ID in form for future use
  });
});

// Close the modal when clicking the "X" button
closeModal.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Close the modal when clicking outside of it
window.addEventListener('click', (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});

// Schedule form submission
scheduleForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const interviewDate = document.getElementById('interview-date').value;
  const interviewTime = document.getElementById('interview-time').value;
  const applicantId = scheduleForm.getAttribute('data-applicant-id'); // Retrieve applicant ID from the form

  // Find the applicant's profile card using the ID
  const applicantCard = document.getElementById(applicantId);
  const interviewDetails = applicantCard.querySelector('.interview-details');

  // Update the applicant card with the scheduled interview details
  interviewDetails.textContent = `Interview Scheduled on: ${interviewDate} at ${interviewTime}`;

  // Close the modal after scheduling
  modal.style.display = 'none';

  // You can also update the UI or send this information to a server if needed
  console.log(`Interview scheduled for applicant ${applicantId} on: ${interviewDate} at ${interviewTime}`);
});

// Toggle between 'All Applied' and 'Draft Applied'
const allAppliedButton = document.getElementById('all-applied');
const draftAppliedButton = document.getElementById('draft-applied');
const applicantCards = document.querySelectorAll('.applicant-card');
const draftContainer1= document.getElementById('draft-applicants');
const appliedApplicantsContainer1 = document.getElementById('applied-applicants');

allAppliedButton.addEventListener('click', () => {
  // Show all applicants
  applicantCards.forEach(card => {
    appliedApplicantsContainer.appendChild(card);
    card.style.display = 'flex'; // Make sure all cards are visible
  });
  allAppliedButton.classList.add('active');
  draftAppliedButton.classList.remove('active');
});

draftAppliedButton.addEventListener('click', () => {
  // Move draft applicants into draft container
  draftContainer.querySelectorAll('.applicant-card').forEach(card => card.style.display = 'flex');
  appliedApplicantsContainer.querySelectorAll('.applicant-card').forEach(card => {
    if (!draftContainer.contains(card)) {
      card.style.display = 'none'; // Hide non-draft cards
    }
  });
  draftAppliedButton.classList.add('active');
  allAppliedButton.classList.remove('active');
});

const scheduleInterviewButton = document.getElementById('schedule-interview');

// Toggle between 'Schedule Interview' view and other views
scheduleInterviewButton.addEventListener('click', () => {
  // Hide applicants without scheduled interviews
  applicantCards.forEach(card => {
    const interviewDetails = card.querySelector('.interview-details').textContent;
    if (interviewDetails.includes('Scheduled on')) {
      card.style.display = 'flex'; // Show card if interview is scheduled
    } else {
      card.style.display = 'none'; // Hide if no interview scheduled
    }
  });

  // Highlight the Schedule Interview tab as active
  scheduleInterviewButton.classList.add('active');
  allAppliedButton.classList.remove('active');
  draftAppliedButton.classList.remove('active');
});




  // You can also update the UI or send this information to a server if needed
