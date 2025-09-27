let dataToInsert = null;
let selectedData = [];
let defaultCellDelimiter = " ";
let defaultRowDelimiter = ", "
let chosenDelimiter = null;

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


function generateDilogBoxForDelimiter(elementToInsert) {
    // generates a dilog box element
    function submitDelimiter(ev) {
        ev.stopPropagation();
        let inputElement = ev.target.previousElementSibling;
        chosenDelimiter = inputElement.value;
        insertCellData(elementToInsert);
        dialogBox.close();
    }

    function closeModal(ev) {
        ev.stopPropagation();
        dialogBox.close();
    }

    let dialogBox = document.createElement("dialog");
    let dialogInputLabel = document.createElement("label");
    dialogInputLabel.setAttribute("for", "delimiter");
    dialogInputLabel.innerText = "Delimiter";
    dialogBox.appendChild(dialogInputLabel);

    let dialogInput = document.createElement("select");
    dialogInput.required = true;
    dialogInput.name = "delimiter";
    const spaceOption = document.createElement("option");
    spaceOption.value = " ";
    spaceOption.innerText = "SPACE";
    dialogInput.appendChild(spaceOption);
    const commaOption = document.createElement("option");
    commaOption.value = ", ";
    commaOption.innerText = "COMMA";
    dialogInput.appendChild(commaOption);
    dialogBox.appendChild(dialogInput);

    let submitButton = document.createElement("button");
    submitButton.innerText = "select";
    submitButton.addEventListener("click", submitDelimiter);
    dialogBox.appendChild(submitButton);

    let closeButton = document.createElement("button");
    closeButton.innerText = "close";
    closeButton.addEventListener("click", closeModal);
    dialogBox.appendChild(closeButton);
    return dialogBox;
}

const insertCellData = function (elementToInsert) {
    // inserts selected cell data into input field
    elementToInsert.value = selectedData.filter(data => data.type === 'td').map((data) => data.cellValue).join(chosenDelimiter || defaultCellDelimiter);
    elementToInsert.dataset.type = 'td';
    elementToInsert.dataset.cells = JSON.stringify([]);
    cleanAfterInsert();
}

const insertRowData = function (elementToInsert) {
    // inserts selected row data into input field
    elementToInsert.value = selectedData.filter(data => data.type === 'tr').map((data) => "" + data.recModel + "#" + data.recId).join(defaultRowDelimiter);
    elementToInsert.dataset.type = 'tr';
    const selectedTh = document.querySelectorAll('th.table-header-selected');
    elementToInsert.dataset.cells = JSON.stringify([...selectedTh].map(th => th.dataset.recFieldName));
    selectedTh.forEach(th => th.classList.remove('table-header-selected'))
    if (selectedTh.length > 0) {
        selectedTh[0].parentElement.classList.remove("table-header-highlight");
    }
    cleanAfterInsert();
}

function cleanAfterInsert() {
    dataToInsert = null;
    selectedData = [];
    removeButtonsFromContextList();
    resetSelectedCell();
}

function insertInto(ev) {
    // inserts selected data into input fields
    ev.stopPropagation();

    const elementToInsert = ev.target.previousElementSibling;
    if (selectedData[0].type === 'td') {
        if (selectedData.length > 1) {
            const dialogBox = generateDilogBoxForDelimiter(elementToInsert);
            document.querySelector("main").appendChild(dialogBox);
            dialogBox.showModal();
            return;
        } else {
            insertCellData(elementToInsert);
        }
    } else {
        insertRowData(elementToInsert);
    }
}


function addDataToSelection(dataElement) {
    // adds to the selectedData
    dataElement.classList.add("selected");
    dataElement.dataset.selectedDataIndex = selectedData.length;
    selectedData.push({...dataElement.dataset, type: dataElement.tagName.toLowerCase()})
}

function removeDataFromSelection(dataElement) {
    // removes from the selectedData
    dataElement.classList.remove("selected");
    const dataElementIndex = parseInt(dataElement.dataset.selectedDataIndex);
    selectedData.splice(dataElementIndex, 1);
}


function addHeaderSelection(element) {
    element.classList.add("table-header-selected");
}

function removeHeaderSelection(element) {
    element.classList.remove("table-header-selected")
}

function removeAllHeaderSelection(dataElement) {
    const selectedTdSelector = "#record-list-" + dataElement.dataset.recModel + " .table-header-selected";
    const allSelectedHeadElements = document.querySelectorAll(selectedTdSelector);
    allSelectedHeadElements.forEach(headElement => headElement.classList.remove("table-header-selected"))

}

function toggleHeaderSelection(ev) {
    ev.stopPropagation();
    if (ev.target.tagName.toLowerCase() === "th" && ev.target.parentElement.classList.contains("table-header-highlight")) {
        if (ev.target.classList.contains("table-header-selected")) {
            removeHeaderSelection(ev.target);
        } else {
            addHeaderSelection(ev.target);
        }
    }
}

function addHeightLightTableHeader(theadElement) {
    theadElement.classList.add("table-header-highlight");
}

function removeHeightLightTableHeader(theadElement) {
    theadElement.classList.remove("table-header-highlight");
}

function toggleHeightLightTableHeader(dataElement) {
    if (dataElement.tagName.toLowerCase() === 'tr') {
        const theadSelector = "#record-list-" + dataElement.dataset.recModel + " thead > tr";
        let theadElement = document.querySelector(theadSelector);
        const selectedDataLen = selectedData.length;
        if (selectedDataLen > 0) {
            addHeightLightTableHeader(theadElement);
        } else {
            removeAllHeaderSelection(dataElement);
            removeHeightLightTableHeader(theadElement);
        }
    }
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

    toggleHeightLightTableHeader(dataTarget);

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

    inputs.forEach(input => {
        ev.detail.parameters[input.name] = {
            'value': input.value,
            'type': input.dataset.type,
            "cells": input.dataset.cells,
        };
    });
}