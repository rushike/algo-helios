// Register event listener for the 'push' event.
console.log("IN PUSH NOTIFICATION FILE")
self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    console.log("Notification Data : ", data)
    const head = data.head || 'New Notification';
    const body = data.body || 'This is default content';
    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: data.icon,
            badge: data.icon,
            url: data.url,
            action : data.url
        })
    );
});

// self.addEventListener('notificationclick', function(event) {
//     console.log("event : ", event)
//     const eventInfo = event.data.text();
//     const data = JSON.parse(eventInfo);
//     let url = 'https://dev.algonauts.in/worker/mercury';
//     console.log("Going to url : ", url)
//     event.notification.close(); // Android needs explicit close.
//     event.waitUntil(
//         clients.matchAll({type: 'window'}).then( windowClients => {
//             // Check if there is already a window/tab open with the target URL
//             for (var i = 0; i < windowClients.length; i++) {
//                 var client = windowClients[i];
//                 // If so, just focus it.
//                 if (client.url === url && 'focus' in client) {
//                     return client.focus();
//                 }
//             }
//             // If not, then open the target URL in a new window/tab.
//             if (clients.openWindow) {
//                 return clients.openWindow(url);
//             }
//         })
//     );
// });