let checkbox = document.querySelector('#checkbox');
let agents = document.querySelectorAll('.agent')

checkbox.addEventListener('click', () => {
    checkbox.checked ? 
    agents.forEach(e => {
        e.classList.add('visible')
    }) :
    agents.forEach(e => {
        e.classList.remove('visible')
    })
})