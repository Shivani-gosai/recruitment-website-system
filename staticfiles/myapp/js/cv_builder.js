// Summary editing functions
function enableEdit1() {
    const editableDiv1 = document.getElementById('editableText1');
    const textField1 = document.getElementById('textField1');

    // Set textarea value to current div text
    textField1.value = editableDiv1.textContent;
    editableDiv1.style.display = 'none'; // Hide div
    textField1.classList.remove('hidden'); // Show textarea
    textField1.focus();
}

function updateText1() {
    const editableDiv1 = document.getElementById('editableText1');
    const textField1 = document.getElementById('textField1');

    // Set div text to textarea value
    editableDiv1.textContent = textField1.value;
    textField1.classList.add('hidden'); // Hide textarea
    editableDiv1.style.display = 'block'; // Show div
}

// Experience editing functions
function enableEdit2() {
    const editableDiv2 = document.getElementById('editableText2');
    const textField2 = document.getElementById('textField2');

    // Set textarea value to current div text
    textField2.value = editableDiv2.textContent;
    editableDiv2.style.display = 'none'; // Hide div
    textField2.classList.remove('hidden1'); // Show textarea
    textField2.focus();
}

function updateText2() {
    const editableDiv2 = document.getElementById('editableText2');
    const textField2 = document.getElementById('textField2');

    // Split lines and add bullet points
    const lines = textField2.value.split('\n').filter(line => line.trim() !== '');
    const bulletPoints = lines.map(line => `<li> ${line}</li>`).join('');

    // Update div with bullet-pointed HTML
    editableDiv2.innerHTML = `<ul>${bulletPoints}</ul>`;
    textField2.classList.add('hidden1'); // Hide textarea
    editableDiv2.style.display = 'block'; // Show div
}

//add field (experience)
function addField1() {
    const experienceContainer = document.getElementById('experienceContainer');

    // Create a new section div
    const newSection = document.createElement('div');
    newSection.classList.add('experience-section');

    // Create input for title
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.placeholder = 'Enter field name here...';
    titleInput.className = 'title-input';

    // Create editable div for text display
    const textDisplayDiv = document.createElement('div');
    textDisplayDiv.classList.add('editable1');
    textDisplayDiv.placeholder = 'Click to add details...';
    textDisplayDiv.onclick = function() {
        enableEdit(textDisplayDiv);
    };

    // Create hidden textarea for editing
    const newTextArea = document.createElement('textarea');
    newTextArea.classList.add('hidden1');
    newTextArea.placeholder = 'Enter your details here...';
    newTextArea.onblur = function() {
        updateText(newTextArea, textDisplayDiv);
    };

    // Append title input, text display div, and textarea to the new section
    newSection.appendChild(titleInput);
    newSection.appendChild(textDisplayDiv);
    newSection.appendChild(newTextArea);

    // Append the new section to the container
    experienceContainer.appendChild(newSection);
}

// Function to enable editing by showing the textarea and hiding the div
function enableEdit(div) {
    const textArea = div.nextElementSibling;
    textArea.value = div.innerText;
    div.style.display = 'none';
    textArea.classList.remove('hidden1');
    textArea.focus();
}

// Function to update the div with the textarea content and hide the textarea
function updateText(textArea, div) {
    //div.innerText = textArea.value || 'Click to add details...';   //Show placeholder text if empty
    div.placeholder="add your details..."
    textArea.classList.add('hidden1');
    div.style.display = 'block';
}

// Event listener for the "Add Field" button
document.getElementById('addFieldBtn1').addEventListener('click', addField1);

// Education editing functions
function enableEdit3() {
    const editableDiv3 = document.getElementById('editableText3');
    const textField3 = document.getElementById('textField3');

    // Set textarea value to current div text
    textField3.value = editableDiv3.textContent;
    editableDiv3.style.display = 'none'; // Hide div
    textField3.classList.remove('hidden2'); // Show textarea
    textField3.focus();
}

function updateText3() {
    const editableDiv31 = document.getElementById('editableText3');
    const textField31 = document.getElementById('textField3');

    // Split lines and add bullet points
    const lines = textField31.value.split('\n').filter(line => line.trim() !== '');
    const bulletPoints = lines.map(line => `<li> ${line}</li>`).join('');

    // Update div with bullet-pointed HTML
    editableDiv31.innerHTML = `<ul>${bulletPoints}</ul>`;
    textField31.classList.add('hidden2'); // Hide textarea
    editableDiv31.style.display = 'block'; // Show div
}

//add field (education)
function addField2() {
    const experienceContainer = document.getElementById('educationContainer');

    // Create a new section div
    const newSection = document.createElement('div');
    newSection.classList.add('education-section');

    // Create input for title
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.placeholder = 'Enter field name here...';
    titleInput.className = 'title-input';

    // Create editable div for text display
    const textDisplayDiv = document.createElement('div');
    textDisplayDiv.classList.add('editable2');
    textDisplayDiv.placeholder = 'Click to add details...';
    textDisplayDiv.onclick = function() {
        enableEdit(textDisplayDiv);
    };

    // Create hidden textarea for editing
    const newTextArea = document.createElement('textarea');
    newTextArea.classList.add('hidden2');
    newTextArea.placeholder = 'Enter your details here...';
    newTextArea.onblur = function() {
        updateText(newTextArea, textDisplayDiv);
    };

    // Append title input, text display div, and textarea to the new section
    newSection.appendChild(titleInput);
    newSection.appendChild(textDisplayDiv);
    newSection.appendChild(newTextArea);

    // Append the new section to the container
    experienceContainer.appendChild(newSection);
}

// Function to enable editing by showing the textarea and hiding the div
function enableEdit(div) {
    const textArea = div.nextElementSibling;
    textArea.value = div.innerText;
    div.style.display = 'none';
    textArea.classList.remove('hidden2');
    textArea.focus();
}

// Function to update the div with the textarea content and hide the textarea
function updateText(textArea, div) {
    //div.innerText = textArea.value || 'Click to add details...';   Show placeholder text if empty
    div.placeholder="add your details..."
    textArea.classList.add('hidden');
    div.style.display = 'block';
}

// Event listener for the "Add Field" button
document.getElementById('addFieldBtn2').addEventListener('click', addField2);

// Add Skill Function with Validation
function addSkill() {
    const skillsList = document.getElementById('skillsList');

    // Check if the total skills are less than 5
    const skillItems = skillsList.getElementsByClassName('skill-item');
    if (skillItems.length >= 5) {
        alert('You already have 5 or more skills added. You can add additional skills as needed.');
    }

    // Create a new skill item
    const skillItem = document.createElement('div');
    skillItem.classList.add('skill-item');

    // Create input for skill name
    const skillNameInput = document.createElement('input');
    skillNameInput.type = 'text';
    skillNameInput.placeholder = 'Enter skill name';
    skillNameInput.className = 'skill-name';

    // Create skill rating div with clickable stars
    const skillRating = document.createElement('div');
    skillRating.classList.add('skill-rating');

    // Create stars for skill rating
    for (let i = 1; i <= 5; i++) {
        const star = document.createElement('i');
        star.classList.add('fa', 'fa-star');
        star.dataset.rating = i;
        star.onclick = function () {
            updateSkillRating(skillRating, i);
        };
        skillRating.appendChild(star);
    }

    // Append skill name and rating to skill item
    skillItem.appendChild(skillNameInput);
    skillItem.appendChild(skillRating);

    // Append the skill item to the skills list
    skillsList.appendChild(skillItem);

    // Display warning message if skills less than 5
    //showMessage();
}

// Update skill rating by highlighting the stars
function updateSkillRating(skillRatingDiv, rating) {
    const stars = skillRatingDiv.querySelectorAll('i');
    stars.forEach((star, index) => {
        star.classList.toggle('active', index < rating);
    });
}

// Event listener for "Add Skill" button
document.getElementById('addSkillBtn').addEventListener('click', addSkill);

// Add Link Function
function addLink() {
    const linksList = document.getElementById('linksList');

    // Create a new link item
    const linkItem = document.createElement('div');
    linkItem.classList.add('link-item');

    // Create input for link name
    const linkNameInput = document.createElement('input');
    linkNameInput.type = 'text';
    linkNameInput.placeholder = 'Link Name (e.g., Portfolio)';
    linkNameInput.className = 'link-name';

    // Create input for link URL
    const linkUrlInput = document.createElement('input');
    linkUrlInput.type = 'url';
    linkUrlInput.placeholder = 'https://example.com';
    linkUrlInput.className = 'link-url';

    // Create remove button
    const removeButton = document.createElement('button');
    removeButton.className = 'link-remove';
    removeButton.textContent = 'Remove';
    removeButton.onclick = function () {
        linksList.removeChild(linkItem);
    };

    // Append inputs and remove button to link item
    linkItem.appendChild(linkNameInput);
    linkItem.appendChild(linkUrlInput);
    linkItem.appendChild(removeButton);

    // Append the link item to the links list
    linksList.appendChild(linkItem);
}

// Event listener for "Add Link" button
document.getElementById('addLinkBtn').addEventListener('click', addLink);

// Add language Function
function addLanguage() {
    const skillsList = document.getElementById('languageList');

    // Create a new skill item
    const skillItem = document.createElement('div');
    skillItem.classList.add('language-item');

    // Create input for skill name
    const skillNameInput = document.createElement('input');
    skillNameInput.type = 'text';
    skillNameInput.placeholder = 'Enter language name';
    skillNameInput.className = 'skill-name';

    // Append skill name and rating to skill item
    skillItem.appendChild(skillNameInput);

    // Append the skill item to the skills list
    skillsList.appendChild(skillItem);
}
// Event listener for "Add Skill" button
document.getElementById('addLanguageBtn').addEventListener('click', addLanguage);

//sending information to another page 
function saveCV() {
    try {
        const experienceHTML = document.getElementById('editableText2').innerHTML;
        const educationHTML = document.getElementById('editableText3').innerHTML;

        // Collect skills data
        const skillItems = document.getElementsByClassName('skill-item');
        let skillsHTML = '';
        for (let skill of skillItems) {
            const skillInput = skill.querySelector('input');
            if (skillInput && skillInput.value.trim() !== '') {
                skillsHTML += `<p>${skillInput.value}</p>`; // Ensure formatted output
            }
        }

        // Collect language data
        const languageItems = document.getElementsByClassName('language-item');
        let languagesHTML = '';
        for (let language of languageItems) {
            const languageInput = language.querySelector('input');
            if (languageInput && languageInput.value.trim() !== '') {
                languagesHTML += `<p>${languageInput.value}</p>`;
            }
        }

        // Collect links data
        const linkItems = document.getElementsByClassName('link-item');
        let linksHTML = '';
        for (let link of linkItems) {
            const linkName = link.querySelector('.link-name').value.trim();
            const linkURL = link.querySelector('.link-url').value.trim();
            if (linkName && linkURL) {
                linksHTML += `<p><a href="${linkURL}" target="_blank">${linkName}</a></p>`;
            }
        }

        // Save to localStorage
        localStorage.setItem('cvExperience', experienceHTML);
        localStorage.setItem('cvEducation', educationHTML);
        localStorage.setItem('cvSkills', skillsHTML);
        localStorage.setItem('cvLanguages', languagesHTML);
        localStorage.setItem('cvLinks', linksHTML);

        console.log('CV saved successfully');
        // Redirect to the profile page
        window.location.href = 'new_profile.html';
    } catch (error) {
        console.error('Error saving CV:', error);
    }
}
