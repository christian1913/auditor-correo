function dropIconPress(num) {
    if (document.getElementById("drop-down-"+num).style.display != "none") {
        //display the dropdown
        document.getElementById("pc-options-box-"+num).style.display = "block";
        document.getElementById("drop-down-"+num).style.display = "none";
        document.getElementById("drop-up-"+num).style.display = "block";
    } else {
        //close the dropdown
        document.getElementById("pc-options-box-"+num).style.display = "none";
        document.getElementById("drop-down-"+num).style.display = "block";
        document.getElementById("drop-up-"+num).style.display = "none";
    }
}