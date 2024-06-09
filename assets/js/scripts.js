function filterProjects() {
    const selectedTag = document.getElementById('tags').value;
    const projects = document.querySelectorAll('.project');

    projects.forEach(project => {
        if (selectedTag === 'all' || project.dataset.tags.includes(selectedTag)) {
            project.style.display = 'block';
        } else {
            project.style.display = 'none';
        }
    });
}
