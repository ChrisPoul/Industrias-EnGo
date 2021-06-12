function on() {
    document.getElementById("product-inventory").style.display = "block";
    document.getElementById("overlay").style.display = "block" 
}
  
function off() {
    document.getElementById("product-inventory").style.display = "none";
    document.getElementById("overlay").style.display = "none" 
}

window.onclick = event => {
    element = event.target
    elementClass = element.className
    if (elementClass == "dropbtn") {
        dropdown = element.parentElement
        dropdown_content = dropdown.children[1]
        dropdown_content.style.display = "block" 
    }
    else {
        dropdowns = document.getElementsByClassName("dropdown-content")
        for(i = 0; i < dropdowns.length; i++){
            dropdowns[i].style.display = "none" 
        }
    }
}
