importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging.js');

// Initialize Firebase
const firebaseConfig = {
    apiKey: "AIzaSyAib7ckYtLeGnv2euF9NDHH3DANZ1uSKIc",
    authDomain: "meditrack-cc802.firebaseapp.com",
    projectId: "meditrack-cc802",
    storageBucket: "meditrack-cc802.firebasestorage.app",
    messagingSenderId: "255572569619",
    appId: "1:255572569619:web:82aec518905f78c933d9e6",
    measurementId: "G-8553C8CDXL"
};

firebase.initializeApp(firebaseConfig);

// Retrieve an instance of Firebase Messaging
const messaging = firebase.messaging();

// Handle background messages
messaging.onBackgroundMessage(function(payload) {
  console.log('Received background message ', payload);

  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: payload.notification.icon,
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
