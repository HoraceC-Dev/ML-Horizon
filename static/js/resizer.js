// JavaScript for resizing functionality
const resizer = document.getElementById('resizer');
const leftPanel = document.getElementById('leftPanel');
const rightPanel = document.getElementById('rightPanel');

let isResizing = false;

resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    document.addEventListener('mousemove', resize);
    document.addEventListener('mouseup', stopResize);
});

function resize(e) {
if (isResizing) {
    // Calculate new width for the left panel based on mouse position
    const newLeftWidth = e.clientX / window.innerWidth * 100;
    leftPanel.style.width = `${newLeftWidth}%`;
    rightPanel.style.width = `${100 - newLeftWidth}%`;
}
}

function stopResize() {
    isResizing = false;
    document.removeEventListener('mousemove', resize);
    document.removeEventListener('mouseup', stopResize);
}