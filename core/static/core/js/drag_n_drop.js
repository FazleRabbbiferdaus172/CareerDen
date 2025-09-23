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
    // inserts selected data into input fields
    ev.stopPropagation();

    const insertCellData = function () {
        elementToInsert.value = selectedData.filter(data => data.type === 'td').map((data) => data.cellValue).join(" ");
        elementToInsert.dataset.type = 'td';
        elementToInsert.dataset.cells = JSON.stringify([]);
    }

    const insertRowData = function () {
        elementToInsert.value = selectedData.filter(data => data.type === 'tr').map((data) => "" + data.recModel + "#" + data.recId).join(", ");
        elementToInsert.dataset.type = 'tr';
        const selectedTh = document.querySelectorAll('th.table-header-selected');
        elementToInsert.dataset.cells = JSON.stringify([...selectedTh].map(th => th.dataset.recFieldName));
        selectedTh.forEach( th => th.classList.remove('table-header-selected'))
        if (selectedTh.length > 0) {
            selectedTh[0].parentElement.classList.remove("table-header-highlight");
        }
    }

    const elementToInsert = ev.target.previousElementSibling;
    if (selectedData[0].type === 'td') {
        insertCellData()
    } else {
        insertRowData()
    }
    dataToInsert = null;
    selectedData = [];
    removeButtonsFromContextList();
    resetSelectedCell();
}


function addDataToSelection(dataElement) {
    dataElement.classList.add("selected");
    dataElement.dataset.selectedDataIndex = selectedData.length;
    selectedData.push({...dataElement.dataset, type: dataElement.tagName.toLowerCase()})
}

function removeDataFromSelection(dataElement) {
    dataElement.classList.remove("selected");
    const dataElementIndex = parseInt(dataElement.dataset.selectedDataIndex);
    selectedData.splice(dataElementIndex, 1);
}

function toggleHeaderSelection(ev) {
    ev.stopPropagation();
    if (ev.target.tagName.toLowerCase() === "th" && ev.target.parentElement.classList.contains("table-header-highlight")) {
        ev.target.classList.add("table-header-selected");
    }
}

function heightLightTableHeader(dataElement) {
    if (dataElement.tagName.toLowerCase() === 'tr') {
        const theadSelector = "#record-list-" + dataElement.dataset.recModel + " thead > tr";
        let theadElement = document.querySelector(theadSelector);
        theadElement.classList.add("table-header-highlight");
    }
}

function toggleSelection(ev) {
    ev.stopPropagation();
    let dataTarget = ev.target;
    while (!dataTarget.classList.contains("selectable")) {
        dataTarget = dataTarget.parentElement;
    }
    heightLightTableHeader(dataTarget);
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


function generatePostParams(ev) {
    const inputs = document.querySelectorAll('#context-list input[type="text"]');

    const structuredData = {};

    inputs.forEach(input => {
        ev.detail.parameters[input.name] = {
            'value': input.value,
            'type': input.dataset.type,
            "cells": input.dataset.cells,
        };
    });
}