let dataToInsert = null;
let selectedData = []

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

function generateButtonToAdd(buttonCallBack) {
    const button_to_add = document.createElement("button");
    button_to_add.textContent = "Insert";
    button_to_add.addEventListener("click", buttonCallBack);
    button_to_add.className = "context-insert";
    return button_to_add;
}

function appendButtonsToContextList(selectorToAdd = "context-list", buttonCallBack = insertInto) {
    let context_children = document.getElementById(selectorToAdd).children;
    let button_is_present = document.getElementsByClassName("context-insert");
    if (button_is_present.length === 0) {
        for (const child of context_children) {
            let another = generateButtonToAdd(buttonCallBack);
            child.appendChild(another);
        }
    }

}

function removeButtonsFromContextList() {
    let insert_buttons = document.getElementsByClassName("context-insert");
    while (insert_buttons.length > 0) {
        insert_buttons[0].remove();
    }
}

function resetSelectedCell()
{
    selectedCells = document.getElementsByClassName("selected-cell");
    while (selectedCells.length !== 0) {
        selectedCells[0].classList.remove("selected-cell");
    }
}

function addTo(ev) {
    ev.stopPropagation();
    dataToInsert = ev.target.previousSibling.innerText;
    appendButtonsToContextList();
}


function insertInto(ev) {
    ev.stopPropagation();
    ev.target.previousElementSibling.value = selectedData.map((data) => data.cellValue).join(" ");
    dataToInsert = null;
    selectedData = [];
    removeButtonsFromContextList();
    resetSelectedCell();
}

function toggleCellSelection(ev) {
    ev.stopPropagation();
    let td = ev.target;
    if (!td.classList.contains("selectable-cell")) {
        td = ev.target.parentElement;
    }

    if (!td.classList.contains("selected-cell")) {
        td.classList.add("selected-cell");
        selectedData.push({...td.dataset})
    } else {
        td.classList.remove("selected-cell");
        const to_remove = {...td.dataset};
        selectedData = selectedData.filter((data) => {
                return !(data.cellValue === to_remove.cellValue && data.recField_name === to_remove.recField_name
                    && data.recId === to_remove.recId && data.recModel === to_remove.recModel);
            }
        );
    }

    if (!isEmptySelectedData()) {
        appendButtonsToContextList();
    } else {
        removeButtonsFromContextList();
    }

}


function isEmptySelectedData() {
    return true ? selectedData.length === 0 : false;
}