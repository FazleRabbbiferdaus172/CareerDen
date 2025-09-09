let dataToInsert = null;
function dragstartHandler(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function dragoverHandler(ev) {
  ev.preventDefault();
}

function dropHandler(ev) {
  ev.preventDefault();
  const data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}

function addTo(ev) {
    ev.stopPropagation();
    dataToInsert = ev.target.previousSibling.innerText;
    let context_children = document.getElementById("context-list").children;
    const button_to_add = document.createElement("button");
    button_to_add.textContent = "Insert";
    button_to_add.addEventListener("click", insertInto);
    button_to_add.className = "context-insert";
    // button_to_add.addEventListener()
    for (const child of context_children) {
        // debugger;
        child.appendChild(button_to_add);
    }
}


function insertInto(ev) {
    ev.target.previousElementSibling.value = dataToInsert;
    dataToInsert = null;
    let insert_buttons = document.getElementsByClassName("context-insert");
    for (let insert_button of insert_buttons) {
        insert_button.remove();
    }
}

function toggleCellSelection(ev) {
    ev.stopPropagation();
    let td = ev.target;
    if (!td.classList.contains("selectable-cell")) {
        td = ev.target.parentElement;
    }
    if (!td.classList.contains("selected-cell")) {td.classList.add("selected-cell")}
    else {td.classList.remove("selected-cell")}

}