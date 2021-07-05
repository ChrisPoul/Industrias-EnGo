function displayOverlayDropdown(event) {
    overlayDropdownButton = event.target
    hideElement(overlayDropdownButton)
    overlayDropdown = overlayDropdownButton.parentElement
    overlayDropdownContent = overlayDropdown.children[1]
    displayElement(overlayDropdownContent)
    overlayDropdownForeground = overlayDropdown.children[2]
    displayElement(overlayDropdownForeground)
}


function hideOverlayDropdown(event) {
    overlayDropdownForeground = event.target
    hideElement(overlayDropdownForeground)
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

