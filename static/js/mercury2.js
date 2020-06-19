// PUSH Notifications
async function tester(){
    console.log("tester to config localfoarage");    
    localforage.config({
        driver      : localforage.INDEXEDDB, // Force WebSQL; same as using setDriver()
        name        : 'mercury',
        version     : 2.0,
        size        : 4980736, // Size of database, in bytes. WebSQL-only for now.
        storeName   : 'notifications', // Should be alphanumeric, with underscores.
        description : 'notifications store'
    });
    console.log("config set.");
    var notifications = JSON.parse(await localforage.getItem("notifications") || "{}")
    if(!notifications || (notifications && notifications.constructor != Object)){
        notifications = {
            time : Date.now(),
            expiry : 86400000,
            data : []
        }
    }
    await localforage.setItem("notifications", JSON.stringify(notifications))
    console.log("demo created");
    
}
tester()
const registerSw = async () => {
    if ('serviceWorker' in navigator) {
        console.log("Will initialte sw.js NOTIFICATION")
        const reg = await navigator.serviceWorker.register('/static/js/sw.js');
        navigator.serviceWorker.addEventListener('message', event => {
            // event is a MessageEvent object
            console.log(`The service worker sent me a message: ${event.data}`);
        });
        initialiseState(reg)
        console.log("initialted sw.js with reg : ", reg)

    } else {
        console.log("Not eligible for push notifications!!")
    }
};

const initialiseState = (reg) => {
    if (!reg.showNotification) {
        console.log('Showing notifications isn\'t supported');
        return
    }
    if (Notification.permission === 'denied') {
        console.log('You prevented us from showing notifications');
        return
    }
    if (!'PushManager' in window) {
        console.log("Push isn't allowed in your browser");
        return
    }
    subscribe(reg);
}

function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    const outputData = outputArray.map((output, index) => rawData.charCodeAt(index));

    return outputData;
}

function request_permission(){
    return new Promise(function(resolve, reject) {
        const permissionResult = Notification.requestPermission(function(result) {
            resolve(result);
        });
    
        if (permissionResult) {
          permissionResult.then(resolve, reject);
        }
    }).then(function(permissionResult) {
            if (permissionResult !== 'granted') {                
                const sub = reg.pushManager.subscribe(options);
                sendSubData(sub)
            }
        });
}

const subscribe = async (reg) => {
    const subscription = await reg.pushManager.getSubscription();
    console.log("Subscribe : subscriptions : ", subscription)
    if (subscription) {
        sendSubData(subscription);
        return;
    }

    const vapidMeta = document.querySelector('meta[name="vapid-key"]');
    const key = vapidMeta.content;

    const options = {
        userVisibleOnly: true, 
        // ...(key && {applicationServerKey: urlB64ToUint8Array(key)})// if key exists, create applicationServerKey property 
    };
    if(key) {
        options.applicationServerKey = urlB64ToUint8Array(key)
    }

    // request_permission()
    const sub = await reg.pushManager.subscribe(options);
    sendSubData(sub)
    
};

// TODOs
// Get all products subscribed from backend
// You get the list of products
const sendSubData = async (subscription) => {
    const browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase();
    groups = await fetch('/worker/user_channel_groups/')
        .then(async (response) => {
            return await response.json();
        })


    console.log("Groups await from channels are : ", groups, groups.length)
    // Subscribe based on the groups eligible
    for(var i = 0; i < groups.length; i++){
        const data = {
            status_type: 'subscribe',
            subscription: subscription.toJSON(),
            browser: browser,
            group: groups[i],
        };
        console.log("Data to Webpush Save : ", data);
        const res = await fetch('/webpush/save_information', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'content-type': 'application/json'
            },
            credentials: "include"
        });

        console.log("sendSubData res : is :  ", res)

        handleResponse(res);
    }
};

const handleResponse = (res) => {
    console.log(res.status);
};

registerSw();
