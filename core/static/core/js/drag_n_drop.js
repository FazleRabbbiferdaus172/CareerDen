let dataToInsert = null;
let selectedData = []

function dragstartHandler(ev) {
    /* start the drag of selected data */
    ev.dataTransfer.setData("text", ev.target.id);
}

function dropHandler(ev) {
    // drops the selected data to conteiner
    ev.preventDefault();
    const data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}

function generateButtonToAdd(buttonCallBack) {
    // factory for creating insert button
    const button_to_add = document.createElement("button");
    button_to_add.textContent = "Insert";
    button_to_add.addEventListener("click", buttonCallBack);
    button_to_add.className = "context-insert";
    return button_to_add;
}

function appendButtonsToContextList(selectorToAdd = "context-list", buttonCallBack = insertInto) {
    // append button for inserting to the context list
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
    // removes button from context list
    let insert_buttons = document.getElementsByClassName("context-insert");
    while (insert_buttons.length > 0) {
        insert_buttons[0].remove();
    }
}

function resetSelectedCell() {
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

    const insertCellData = function () {
        ev.target.previousElementSibling.value = selectedData.filter(data => data.type === 'td').map((data) => data.cellValue).join(" ");
        ev.target.previousElementSibling.dataset.type = 'td'
    }
    const insertRowData = function () {
        ev.target.previousElementSibling.value = selectedData.filter(data => data.type === 'tr').map((data) => ""+data.recModel+"#"+data.recId ).join(", ");
        ev.target.previousElementSibling.dataset.type = 'tr'
    }
    if (selectedData[0].type === 'td') {
        insertCellData()
    }
    else {
        insertRowData()
    }
    dataToInsert = null;
    selectedData = [];
    removeButtonsFromContextList();
    resetSelectedCell();
}


function addDataToSelection(dataElement) {
    dataElement.classList.add("selected");
    dataElement.dataset.selectedDataIndex = selectedData.length + 1;
    selectedData.push({...dataElement.dataset, type: dataElement.tagName.toLowerCase()})
}

function removeDataFromSelection(dataElement) {
    dataElement.classList.remove("selected");
    const to_remove = {...dataElement.dataset, type: dataElement.tagName.toLowerCase()};
    selectedData = selectedData.filter((data) => {
            // if (data.type !== "cell") return true;
            return !(data.cellValue === to_remove.cellValue && data.recFieldName === to_remove.recFieldName
                && data.recId === to_remove.recId && data.recModel === to_remove.recModel && data.type === to_remove.type);
        }
    );
}

function toggleSelection(ev) {
    ev.stopPropagation();
    let dataTarget = ev.target;
    while (!dataTarget.classList.contains("selectable")) {
        dataTarget = dataTarget.parentElement;
    }

    if (!dataTarget.classList.contains("selected")) {
        addDataToSelection(dataTarget);
    } else {
        removeDataFromSelection(dataTarget);
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