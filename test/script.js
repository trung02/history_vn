const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const contentElement = document.getElementById('content');

searchButton.addEventListener('click', () => {
    const searchTerm = searchInput.value.toLowerCase();
    const contentText = contentElement.textContent.toLowerCase();

    if (searchTerm.trim()) {
        const highlightedContent = contentText.replace(new RegExp(`(${searchTerm})`, 'g'), `<span class="highlight">$1</span>`);
        contentElement.innerHTML = highlightedContent;
    } else {
        contentElement.innerHTML = contentText;
    }
});
