const container1 = document.querySelector('#slider-container-1');
document.querySelector('#slider-1').addEventListener('input', (e) => {
    container1.style.setProperty('--position', `${e.target.value}%`);
});

const container2 = document.querySelector('#slider-container-2');
document.querySelector('#slider-2').addEventListener('input', (e) => {
    container2.style.setProperty('--position', `${e.target.value}%`);
});

const container3 = document.querySelector('#slider-container-3');
document.querySelector('#slider-3').addEventListener('input', (e) => {
    container3.style.setProperty('--position', `${e.target.value}%`);
});