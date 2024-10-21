odoo.define("backend_theme_v14.sidebar-toggle", function (require) {
  "use strict";

  var session = require("web.session");
  var rpc = require("web.rpc");
  var id = session.uid;

  rpc
    .query({
      model: "res.users",
      method: "read",
      args: [[id], ["sidebar_visible"]],
    })
    .then(function (res) {
      var dbfield = res[0];
      // Si la base de datos no tiene el valor sidebar_visible, la barra estará cerrada por defecto
      var toggle = dbfield.sidebar_visible !== undefined ? dbfield.sidebar_visible : false;

      if (toggle === false) {
        $("#app-sidebar").removeClass("toggle-sidebar");
      } else {
        $("#app-sidebar").addClass("toggle-sidebar"); // Esto asegurará que esté cerrada por defecto
      }
    });
});
