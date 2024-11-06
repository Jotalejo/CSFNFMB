document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('form').onsubmit = function () {
        document.querySelector('#username').type='reset';
    };
});