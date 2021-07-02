function displayProductInventory(event) {
    productInventoryButton = event.target
    hideElement(productInventoryButton)
    productInventory = productInventoryButton.parentElement
    productInventoryContent = productInventory.children[1]
    productInventoryOverlay = productInventory.children[2]
    displayElement(productInventoryContent)
    displayElement(productInventoryOverlay)
}


function hideProductInventories(event) {
    productInventoryOverlay = event.target
    hideElement(productInventoryOverlay)
    productInventoryButtons = document.getElementsByClassName("product-inventory-button")
    productInventoryContents = document.getElementsByClassName("product-inventory-content")
    for (i = 0; i < productInventoryContents.length; i++) {
        hideElement(productInventoryContents[i])
        displayElement(productInventoryButtons[i])
    }
}


function displayElement (element) {
    element.style.display = "block" 
}


function hideElement (element) {
    element.style.display = "none"
}

