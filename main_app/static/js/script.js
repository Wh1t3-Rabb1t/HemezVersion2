//-- User generated zoom event detection. -----------------------------------------------//
let manualZoomEvent = false;

// Detect a user initiated zoom event with the cmd key and mouse scroll wheel.
window.addEventListener('wheel', function(event) {
    if (event.metaKey) { // If cmd is held down (metaKey is the cmd key on Mac).
        if (event.deltaY > 0) { // User has zoomed out.
            manualZoomEvent = true;
            // console.log('Scroll wheel zoom out event detected.');
        } else { // User has zoom in.
            manualZoomEvent = true;
            // console.log('Scroll wheel zoom in event detected.');
        };
    };
});

// Detect a user initiated zoom event using keyboard shortcuts.
window.addEventListener('keydown', function(event) {
    if (event.metaKey && event.code === 'Equal') { // User has pressed cmd +.
        manualZoomEvent = true;
        // const html = document.querySelector('html');
        // html.style = 'zoom: 1.10';
        // calculateZoomLevel();
        // console.log('"Cmd +" zoom in event detected.');
    } else if (event.metaKey && event.code === 'Minus') { // User has pressed cmd -.
        manualZoomEvent = true;
        // const html = document.querySelector('html');
        // html.style = 'zoom: 0.90';
        // calculateZoomLevel();
        // console.log('"Cmd -" zoom out event detected.');
    };
});

// Detect a user initiated zoom event using a touch screen.
window.addEventListener('touchmove', function(event) {
    if (event.scale < 1) { // User has zoomed out.
        manualZoomEvent = true;
    } else { // User has zoomed in.
        manualZoomEvent = true;
    };
});

// const element = document.querySelector('body');
// let previousWidth = element.offsetWidth;

// const observer = new ResizeObserver(entries => {
//     const currentWidth = element.offsetWidth;
//     const zoomIncrease = (currentWidth - previousWidth) / previousWidth;
//     // console.log(`Zoom increase: ${zoomIncrease * 100}%`);
//     previousWidth = currentWidth;
// });
// observer.observe(element);
// let scaleFactor = Math.round(zoomIncrease) * 10;

//-- Dynamic page scaling. --------------------------------------------------------------//
function smartResizing() {
    const signupMainContainer = document.getElementById('signup-main-container');
    const phoneBubbleContainer = document.getElementById('phone-bubble-container');
    const main = document.querySelector('main');
    const root = document.querySelector(':root');
    const baseWidth = 1432; // Container width.
    const baseHeight = 712; // Container height excluding the menu bar.
    let widthDifference, heightDifference, averageDifference = 0;
    let viewportWidth = window.innerWidth;
    let viewportHeight = window.innerHeight;
    let height = main.offsetHeight;
    let rootFontSize = 100;

    console.log('hello');

    // Handler for calculating the % difference in pixel ratios between different resolutions.
    function calculatePercentageDifference(oldValue, newValue) {
        return (newValue - oldValue) / oldValue * 100;
    };

    // If a zoom event is initiated manually, cancel out of smartResizing to enable zoom.
    if (manualZoomEvent == true) {
        manualZoomEvent = false;
    } else {
        // If the current viewport dimensions don't match the base value, calculate the % difference.
        if (viewportWidth != baseWidth || viewportHeight != baseHeight) {
            widthDifference = calculatePercentageDifference(baseWidth, viewportWidth);
            heightDifference = calculatePercentageDifference(baseHeight, height);
            averageDifference = Math.round((widthDifference + heightDifference) / 2);
        };

        // Update the :root font size to scale all elements using rem.
        rootFontSize += averageDifference;
        root.style.fontSize = rootFontSize + 'px';

        // Rearrange page layout if the screens height is > the width.
        if (viewportHeight > viewportWidth) {
            signupMainContainer.style.flexDirection = 'column';
            phoneBubbleContainer.style.marginLeft = '25%';
        } else if (viewportHeight < viewportWidth) {
            signupMainContainer.style.flexDirection = 'row';
            phoneBubbleContainer.style.marginLeft = '0%';
        };
    };
};
window.addEventListener('load', () => smartResizing());
window.addEventListener('resize', () => smartResizing());
