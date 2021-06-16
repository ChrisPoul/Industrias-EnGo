function on() {
    displayElement(document.getElementById("product-inventory"))
    displayElement(document.getElementById("overlay"))
}
  

function off() {
    hideElement(document.getElementById("product-inventory"))
    hideElement(document.getElementById("overlay"))
}


window.onclick = event => {
    element = event.target
    if (element.className == "side-menu-button") {
        displaySideMenu(element)
    }
    else if (element.className == "dropdown-links-button") {
        displayDropdownLinks(element)
    }
    else if (element.className == "side-menu-background") {
        hideSideMenu(element)
    }
}


function displaySideMenu (menuButton) {
    sideMenu = menuButton.parentElement
    menuContent = sideMenu.children[1]
    menuContent.style.display = "flex"
    menuBackground = sideMenu.children[2]
    displayElement(menuBackground)
}


function displayDropdownLinks (dropdownLinksButton) {
    dropdownLinks = dropdownLinksButton.parentElement
    dropdownLinksContent = dropdownLinks.children[1]
    displayElement(dropdownLinksContent)
}


function hideSideMenu (menuBackground) {
    hideElement(menuBackground)
    menuContent = document.getElementsByClassName("side-menu-content")[0]
    hideElement(menuContent)
}


function displayElement (element) {
    element.style.display = "block" 
}


function hideElement (element) {
    element.style.display = "none"
}
