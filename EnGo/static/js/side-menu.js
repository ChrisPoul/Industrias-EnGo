window.onclick = event => {
    element = event.target
    if (element.className == "side-menu-button") {
        displaySideMenu(element)
    }
    else if (element.parentElement.className == "side-menu-button") {
        sideMenuButton = element.parentElement
        displaySideMenu(sideMenuButton)
    }
    else if (element.className == "links-dropdown-button") {
        toggleDropdownLinks(element)
    }
    else if (element.parentElement.className == "links-dropdown-button") {
        linksDropdownButton = element.parentElement
        toggleDropdownLinks(linksDropdownButton)
    }
    else if (element.className == "side-menu-background") {
        hideSideMenu(element)
    }
}


function displaySideMenu (sideMenuButton) {
    sideMenu = sideMenuButton.parentElement
    sideMenuContent = sideMenu.children[1]
    sideMenuContent.style.display = "flex"
    sideMenuBackground = sideMenu.children[2]
    displayElement(sideMenuBackground)
}


function toggleDropdownLinks (dropdownLinksButton) {
    dropdownLinks = dropdownLinksButton.parentElement
    dropdownLinksContent = dropdownLinks.children[1]
    if (dropdownLinksContent.style.display != "block") {
        displayElement(dropdownLinksContent)
    }
    else {
        hideElement(dropdownLinksContent)
    }
}


function hideSideMenu (sideMenuBackground) {
    hideElement(sideMenuBackground)
    sideMenuContent = document.getElementsByClassName("side-menu-content")[0]
    hideElement(sideMenuContent)
}


function displayElement (element) {
    element.style.display = "block" 
}


function hideElement (element) {
    element.style.display = "none"
}