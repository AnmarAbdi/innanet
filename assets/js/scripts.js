// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    fetchProjects();
});

let allProjects = [];

function fetchProjects() {
    fetch('data/projects.json')
        .then(response => response.json())
        .then(data => {
            allProjects = data;
            populateProjects(allProjects);
            populateTags(allProjects);
        })
        .catch(error => console.error('Error fetching projects:', error));
}

function populateProjects(projects) {
    const projectsContainer = document.getElementById('projects');
    projectsContainer.innerHTML = ''; // Clear previous content

    projects.forEach(project => {
        const projectDiv = document.createElement('div');
        projectDiv.classList.add('project');
        projectDiv.dataset.tags = project.tags.join(',');

        const projectTitle = document.createElement('h3');
        projectTitle.textContent = project.id;

        const projectDescription = document.createElement('p');
        projectDescription.textContent = project.title;

        const projectLink = document.createElement('a');
        projectLink.href = project.link;
        projectLink.target = '_blank';
        projectLink.textContent = 'View Document';

        projectDiv.appendChild(projectTitle);
        projectDiv.appendChild(projectDescription);
        projectDiv.appendChild(projectLink);

        projectsContainer.appendChild(projectDiv);
    });
}

function populateTags(projects) {
    const tagSet = new Set();
    projects.forEach(project => {
        project.tags.forEach(tag => tagSet.add(tag));
    });

    const tagsSelect = document.getElementById('tags');
    tagsSelect.innerHTML = '<option value="all">All</option>'; // Reset options

    const sortedTags = Array.from(tagSet).sort();

    sortedTags.forEach(tag => {
        const option = document.createElement('option');
        option.value = tag;
        option.textContent = tag;
        tagsSelect.appendChild(option);
    });
}

function filterProjects() {
    const selectedTag = document.getElementById('tags').value;
    const projects = document.querySelectorAll('.project');

    projects.forEach(project => {
        const projectTags = project.dataset.tags.split(',');
        if (selectedTag === 'all' || projectTags.includes(selectedTag)) {
            project.style.display = 'block';
        } else {
            project.style.display = 'none';
        }
    });
}
