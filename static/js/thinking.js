

function stopThinking() {
    // Hide the thinking dots
    document.getElementById("think-container").remove();
}

export function createThinkingAnimation() {
    const thinkContainer = document.createElement("div");
    thinkContainer.id = "think-container";
    thinkContainer.innerHTML = '<link rel="stylesheet" href="../static/css/thinking.css"><div id="thinkingDots" class="thinking-dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
    return thinkContainer
}

export function deleteThinkingAnimation() {
    const thinkContainer = document.getElementById("think-container");
    if(thinkContainer) {
        thinkContainer.remove();
    }
}