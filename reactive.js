document.addEventListener('DOMContentLoaded', function() {
  var vueApp = new Vue({
    el: '#nova-demo-component',
    data: {
      inboundMessage: 'waiting for reply...',
      buttons: {
        sendData: true,
        sendSMS: true,
      }
    }
  });
})
