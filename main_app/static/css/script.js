
// const darkMode = document.getElementsByClassName('moon');
// const lightMode = document.getElementsByClassName('sun');
// const body = document.body;

// // const ph = document.getElementsByClassName('sun');

// darkMode.onClick = () => {

// };

// lightMode.onClick = () => {
//     body.classList.replace('test', 'test1');
//     // h1.classList.remove('test');
//     // body.classList.add('test1');
//     // body.style.color = 'red';
// };


let darkMode = localStorage.getItem('darkMode');
const darkModeToggle = document.querySelector('#dark-mode-toggle');

const enableDarkMode = () => {
    document.body.classList.add('darkmode');
    localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
    document.body.classList.remove('darkmode');
    localStorage.setItem('darkMode', null);
}
 
if (darkMode === 'enabled') {
    enableDarkMode();
}

darkModeToggle.addEventListener('click', () => {
    darkMode = localStorage.getItem('darkMode'); 
  
  if (darkMode !== 'enabled') {
        enableDarkMode();
    } else {  
        disableDarkMode(); 
    }
});

