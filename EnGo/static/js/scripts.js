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


function displayWarehouseInventory (event, inventory) {
    hideInventoryContents()
    inventoryButton = event.target
    inventoryButton.style.backgroundColor = "lightgray"
    inventoryContent = document.getElementById("warehouse-" + inventory)
    displayElement(inventoryContent)
}


function hideInventoryContents () {
    inventoryContents = document.getElementsByClassName("warehouse-inventory-content")
    for (i = 0; i < inventoryContents.length; i++) {
        hideElement(inventoryContents[i])
    }
    inventoryButtonsDiv = document.getElementsByClassName("warehouse-inventory-buttons")[0]
    inventoryButtons = inventoryButtonsDiv.children
    for (i = 0; i < inventoryButtons.length; i++) {
        inventoryButtons[i].style.backgroundColor = "inherit"
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
