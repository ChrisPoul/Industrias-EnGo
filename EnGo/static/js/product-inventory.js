window.onclick = event => {
    element = event.target
    if (element.className == "product-inventory-button") {
        displayProductInventory(element)
    }
    else if (element.className == "product-inventory-overlay") {
        hideElement(element)
        hideProductInventories()
    }
}


function displayProductInventory(productInventoryButton) {
    productInventory = productInventoryButton.parentElement
    productInventoryContent = productInventory.children[1]
    productInventoryOverlay = productInventory.children[2]
    displayElement(productInventoryContent)
    displayElement(productInventoryOverlay)
}


function hideProductInventories() {
    productInventoryContents = document.getElementsByClassName("product-inventory-content")
    console.log(productInventoryContents)
    for (i = 0; i < productInventoryContents.length; i++) {
        hideElement(productInventoryContents[i])
    }
}


function displayElement (element) {
    element.style.display = "block" 
}


function hideElement (element) {
    element.style.display = "none"
}