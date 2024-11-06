document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('form').onsubmit = function () {
        const name = document.querySelector('#username').value;
        alert(`Hola, ${name}!`);
    };
});