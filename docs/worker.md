# Worker - Mercury

This can subdivided into 2 frontend(Vue) and backend

## Frontend
Frontend structure is explained in [**`static.md`**][static].

It also uses [**`localForage`**][localforage] libray to store user notification came to view it later.

localForage used `IndexedDB` different from `localStorage`, the only reason to use is can acced from service worker, where notification are stored and easily retrived from in frontend useing localForage library.


## Backend
Performs 3 main functionaties
1. Web Socket -- for live updates
    - Three files performs, all websockets tasks need
        - ConsumerManager: 
            - It is like meta file, contain `ConsumerManger` instance which is `Singelton` class
        - DataConsumer :
            - Routes @ **`/datalink`**.
            - Recives the messages from **janus** backend to **helios**. So basically establishes connection between **janus** and **helios**
            - Also responsible for sending *Web Notification* through [**`WebPush`**][webpush]. Includes functionality in **`functions.py`**.
            - It is very losely coupled. It can easily replace with eventhub.py.
        - DataPublisher :
            - Routes @ **`/channel`**
            - Establises link between **`Client Browser`** and **`helios`**.
            - It fetches the user subscriptions and published **ltp** and **new calls** and **call update** to client browser
            - Uses daphne server in production, refer [Daphne][daphne] & [Django Channels][django-channels].
            - It also maintains redis channel instantace and assosciates users to redis groups on channel based on users subscriptions.
            - It is reponsible for user removal from redis group, in case of disconnetion.


## References
- Web Push : https://developers.google.com/web/fundamentals/push-notifications
- Django Webpush : https://github.com/safwanrahman/django-webpush
- Django Channels: https://channels.readthedocs.io/en/latest/
- Daphne: https://github.com/django/daphne
- LocalForage Page : https://localforage.github.io/localForage/
- LocalForage Git : https://github.com/localForage/localForage

[static]: ./static.md
[django-channels]: https://channels.readthedocs.io/en/latest/
[daphne]: https://github.com/django/daphne
[webpush]: https://developers.google.com/web/fundamentals/push-notifications
[django-webpush]: https://github.com/safwanrahman/django-webpush
[localforage]: https://localforage.github.io/localForage/