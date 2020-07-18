> ## How to start server ?
> First Database should be live, well before helios is ON, else daphne will not work. Will need to restart **helios**, specially a daphne problem.  
**`Start DB VM ---> Start Helio VM`**

> ## How to enable notification ?
> This is totally browser settings, if user deny on first attempts, user will need to allow from settings

> ## Notifications Changes in code not visible ?
> Notification are fetched through **`sw.js`**, service worker register only once when user click allow from notification prompt
solution user need to.   
**`Make Notificaion to Ask(Default) --> Removed Cookies --> Refresh Page`**

> ## How to convert Django models to png ?
> Run command on linux like enviroment, `python3 manage.py graph_models -a > helios.dot`
> Then paste content from .dot file in https://dreampuf.github.io/GraphvizOnline/.It generated PNG, save to local computer

>   