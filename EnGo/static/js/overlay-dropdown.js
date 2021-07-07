function displayOverlayDropdown(event) {
    overlayDropdownButton = event.target
    if (!overlayDropdownButton.className.includes("overlay-dropdown-button")) {
        overlayDropdownButton = overlayDropdownButton.parentElement
    } 
    hideElement(overlayDropdownButton)
    overlayDropdown = overlayDropdownButton.parentElement
    overlayDropdownContent = overlayDropdown.children[1]
    displayElement(overlayDropdownContent)
    overlayDropdownBackground = overlayDropdown.children[2]
    displayElement(overlayDropdownBackground)
}


function hideOverlayDropdown(event) {
    overlayDropdownBackground = event.target
    hideElement(overlayDropdownBackground)
    overlayDropdownButtons = document.getElementsByClassName("overlay-dropdown-button")
    overlayDropdownContents = document.getElementsByClassName("overlay-dropdown-content")
    for (i = 0; i < overlayDropdownContents.length; i++) {
        hideElement(overlayDropdownContents[i])
        displayElement(overlayDropdownButtons[i])
    }
}


function displayElement (element) {
    element.style.display = "block" 
}


function hideElement (element) {
    element.style.display = "none"
}

