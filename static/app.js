// Check if service workers are supported
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/firebase-messaging-sw.js')  // Path to the service worker file
    .then(function(registration) {
      console.log('Service Worker registered with scope:', registration.scope);
      // Request permission to send notifications
      requestPermission();
    })
    .catch(function(error) {
      console.log('Service Worker registration failed:', error);
    });
}

// Request permission to send notifications and get the Firebase device token
function requestPermission() {
  firebase.messaging().requestPermission()
    .then(function() {
      console.log('Notification permission granted.');
      return firebase.messaging().getToken();
    })
    .then(function(token) {
      console.log('Firebase Device Token:', token);
      // Send this token to your Django backend to store it
      saveDeviceToken(token);
    })
    .catch(function(err) {
      console.log('Notification permission denied or error occurred:', err);
    });
}

// Save the device token to your backend
function saveDeviceToken(token) {
  fetch('/api/save-device-token/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + YOUR_ACCESS_TOKEN // If using authentication
    },
    body: JSON.stringify({ token: token })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Device token saved:', data);
  })
  .catch(error => console.log('Error saving token:', error));
}
