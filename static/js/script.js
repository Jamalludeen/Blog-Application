let elem = document.getElementById('my-nav');
let Selem = document.getElementById("scrollelem");
let searchInput = document.querySelector('.search-elem');


window.addEventListener('scroll', () => {
    let scrollTop = window.scrollY

    let documentHeight = document.body.clientHeight

    let windowHeight = window.innerHeight

    let scrollPercent = scrollTop / (documentHeight - windowHeight)

    let scrollPercentRounded = Math.round(scrollPercent * 100)

    Selem.style.width = scrollPercentRounded + '%'

    console.log(scrollPercentRounded);
})

searchInput.addEventListener('focus', () => {
    searchInput.style.border = '1px solid #0000ff'
})
searchInput.addEventListener('blur', () => {
    searchInput.style.border = '1px solid #a9c6ff'
})
