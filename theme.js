// Loaded in <head> before CSS paints: applies the saved light/dark choice (otherwise CSS follows prefers-color-scheme). ?embed always renders light so docs/speed-feel.gif stays stable.
(function(){var t=null;try{t=localStorage.getItem('theme')}catch(e){}
if(/[?&]embed\b/.test(location.search))t='light';
if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);})();
