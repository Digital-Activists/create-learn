const showSelection = document.querySelector('.add-button');
const selectionView = document.querySelector('.view-selection');
const selectionClose = document.querySelector('.close-view-selection');


showSelection.onclick = () => {
    selectionView.classList.add('active')
}

selectionClose.onclick = () => {
    selectionView.classList.remove('active')
}
