// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'New Notification';
    const body = data.body || 'This is default content';
    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: data.icon,
            badge: data.icon,
            url: data.url,
            data : data        
        })
    );
});

self.addEventListener('notificationclick', function(event) {
    const clickedNotification = event.notification;
    clickedNotification.close();
  
    // Do something as the result of the notification click
    const promiseChain = do_things_on_click(clickedNotification.data)
    event.waitUntil(promiseChain);
  });

function do_things_on_click(data){
    // console.log("did the so much job ")
    clients.openWindow(data.url);        
};