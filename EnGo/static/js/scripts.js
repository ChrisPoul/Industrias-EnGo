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
    if (element.className == "dropbtn") {
        displayDropdown(element)
    }
    else {
        dropdowns = document.getElementsByClassName("dropdown-content")
        for(i = 0; i < dropdowns.length; i++){
            hideElement(dropdowns[i])
        }
    }
}


function displayDropdown (dropdownButton) {
    dropdown = dropdownButton.parentElement
    dropdownContent = dropdown.children[1]
    displayElement(dropdownContent)
}


function displayElement (element) {
    element.style.display = "block" 
}


function hideElement (element) {
    element.style.display = "none"
}
