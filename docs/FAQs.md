> How to start server ?
First Database should be live, then helios should on, else daphne will not work.
**`Start DB VM ---> Start Helio VM`**

> How to enable notification ?
This is totally browser settings, if user deny on first attempts, user will need to allow from settings

> Notifications Changes not visible ?
Notification are fetched through **`sw.js`**, service worker regiester only once when user click allow from notification prompt
solution user need to 
**`Make Notificaion to Ask(Default) --> Removed Cookies --> Refresh Page`**