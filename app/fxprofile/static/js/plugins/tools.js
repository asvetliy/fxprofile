// types: 'primary', 'info', 'success', 'warning', 'danger'
let tools = {
  showNotification: function (from, align, message, type) {
    $.notify({
      icon: "add_alert",
      message: message
    }, {
      type: type,
      timer: 3000,
      placement: {
        from: from,
        align: align
      }
    });
  }
};