
    function webpush(){
            return function(event) {
            // Retrieve the textual payload from event.data (a PushMessageData object).
            // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
            // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
            const eventInfo = event.data.text();
            const data = JSON.parse(eventInfo);
            const head = data.head || 'New Notification';
            const body = JSON.parse(data.body || '{}');
            var bodytext = ""            

            var db;
            var dbName = "mercury";
            
            var request = indexedDB.open(dbName, 2);

            request.onerror = function(event) {
                // Handle errors.
            };
            request.onsuccess = function(event){
                // Once the database is created, let's add our user to it...
                db = event.target.result;
                var store_name = "notifications"
                var transaction = db.transaction([store_name], "readwrite");

                // Do something when all the data is added to the database.
                transaction.oncomplete = function(event) {
                    // console.log("All done!");
                };

                transaction.onerror = function(event) {
                    // Don't forget to handle errors!
                };

                var objectStore = transaction.objectStore(store_name);
                var get_request = objectStore.get("notifications")
                get_request.onsuccess = function(event){
                    var notifications_str = get_request.result
                    var notifications = JSON.parse(notifications_str)                  
                    notifications.data.push(body)
                    var request = objectStore.put(JSON.stringify(notifications), "notifications" );
                    request.onsuccess = function(event) {
                        // Contains our user info.                            
                    };
                }
            }                    
            if(body.dtype == "signal"){
                if(body.product_type == "OPT"){
                    bodytext += `${body.signal.toUpperCase()} - ${body.ticker} @ ${body.price} with `+
                            `TP : ${body.target_price}, SL : ${body.stop_loss},`+
                            `  Risk $ : ${body.risk_reward} & Profit % : ${body.profit_percent}`
                }
                else {
                    bodytext += `${body.signal.toUpperCase()} - ${body.ticker} @ ${body.price} with `+
                            `TP : ${body.target_price}, SL : ${body.stop_loss},`+
                            `  Risk $ : ${body.risk_reward} & Profit % : ${body.profit_percent}`
                }
            }else{                
                bodytext += `${body.ticker} - ${body.signal}, ${body.status}`
            }
            // Keep the service worker alive until the notification is created.
            event.waitUntil(
                self.registration.showNotification(head, {
                    body: bodytext,
                    icon: data.icon,
                    badge: data.icon,
                    url: data.url,
                    data : data        
                })
            );
        }
    }

    // Register event listener for the 'push' event.
    self.addEventListener('push', webpush());

    self.addEventListener('notificationclick', function(event) {
        const clickedNotification = event.notification;
        clickedNotification.close();
    
        // Do something as the result of the notification click
        const promiseChain = do_things_on_click(clickedNotification.data)
        event.waitUntil(promiseChain);
    });

    function do_things_on_click(data){
        clients.openWindow(data.url);        
    };