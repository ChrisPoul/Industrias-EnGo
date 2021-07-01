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


function displayElement (element) {
    element.style.display = "block" 
}


function hideElement (element) {
    element.style.display = "none"
}
