odoo.define('tls_tollsync.gmaps', function(require) {
	"use strict";

	var core = require('web.core');
	var Widget = require('web.Widget');
	var widgetRegistry = require('web.widget_registry');

	var qweb = core.qweb;
	var _t = core._t;

	var GMapRoute = Widget.extend({
		template: "tls_widget_route",
		events: {
			'click .tls-route-warn': '_goToSettings'
		},
		init: function(view, record) {
			this._super(view, record);
			this.data = record.data;
			this.imgMapEl = null;
		},
		start: function() {
			var data = this.data;
			if (!data['hide_route_widget']) {
				var coords = data['entry_lat'] && data['entry_lng'] && data['exit_lat'] && data['exit_lng'];
				if (!coords) {
					this.shoWarn(_t('Both coordinates are required to show the map'));
				} else if (data['use_booster_widget']) {
					this.booInit();
				} else if (typeof google !== 'object') {
					var self = this;
					this._rpc({
						route: '/tls/google_maps_api_key'
					}).then(function(res) {
						var resJson = JSON.parse(res);
						var secret = resJson.google_maps_api_key;
						if (secret !== '') {
							window.ginit = self.gInit.bind(self);
							$.getScript('https://maps.googleapis.com/maps/api/js?key=' + secret + '&callback=ginit');
						} else {
							self.shoWarn();
						}
					});
				} else {
					this.gInit();
				}
			}
		},
		booInit: function() {
			if (this.data['route_image']) {
				this.booPutMap();
			} else {
				var self = this;
				this._rpc({
					model: 'tls.toll',
					method: 'get_booster_map',
					args: [self.data['id']]
				}).then(function(res) {
					if (res.success) {
						self.booPutMap();
					} else {
						self.shoWarn(res.message);
					}
				});
			}
		},
		gInit: function() {
			var self = this;
			var fromLatLng = new google.maps.LatLng(this.data['entry_lat'], this.data['entry_lng']);
			var toLatLng = new google.maps.LatLng(this.data['exit_lat'], this.data['exit_lng']);
			var request = {
				origin: fromLatLng,
				destination: toLatLng,
				travelMode: google.maps.TravelMode.DRIVING
			};
			this.map = new google.maps.Map(this.el, {
				zoom: 10,
				backgroundColor: '#e0e0e0'
			});
			this.directionsService = new google.maps.DirectionsService();
			this.directionsDisplay = new google.maps.DirectionsRenderer();
			this.directionsDisplay.setMap(self.map);
			this.directionsService.route(request, function(response, status) {
				if (status === google.maps.DirectionsStatus.OK) {
					self.directionsDisplay.setDirections(response);
				}
			});
		},
		booPutMap: function() {
			var self = this;
			this._rpc({
				model: 'tls.toll',
				method: 'get_base64_map',
				args: [self.data['id']]
			}).then(function(res) {
				if (res) {
					self.$el.html(qweb.render('tls_widget_img_route', { base64_map_data: res }));
					setTimeout(function() {
						self.booRender();
					}, 500);
				}
			});
		},
		booRender: function() {
			var self = this;
			var maxW = this.el.clientWidth;
			var maxH = this.el.clientHeight;
			var map = document.getElementById('tls_drag_map');
			if (maxW && maxH && map) {
				var ratio = maxW / map.width;
				if (map.height * ratio < maxH) ratio = maxH / map.height;
				var width = Math.floor(map.width * ratio);
				var height = Math.floor(map.height * ratio);
				map.style.cssText = 'width:' + width + 'px; height:' + height + 'px; opacity:1';

				map.addEventListener('mousedown', self.startDrag.bind(self));
				map.addEventListener('mousemove', self.whileDrag.bind(self));
				map.addEventListener('mouseup', self.stopDrag.bind(self));
				map.addEventListener('wheel', self.mapZoom.bind(self));
			} else {
				this.shoWarn();
			}
		},
		startDrag: function(e) {
			this.imgMapEl = e.target;
			this.imgMapX = e.clientX - this.imgMapEl.offsetLeft;
			this.imgMapY = e.clientY - this.imgMapEl.offsetTop;
			this.imgMapEl.style.cursor = 'grabbing';
		},
		whileDrag: function(e) {
			if (this.imgMapEl !== null) {
				var mapW = this.imgMapEl.width;
				var mapH = this.imgMapEl.height;
				var newLeft = e.clientX - this.imgMapX;
				var newTop = e.clientY - this.imgMapY;
				var halfW = Math.floor(mapW / 2);
				var halfH = Math.floor(mapH / 2);
				var halfWzoom = halfW - (mapW - this.el.clientWidth);
				var halfHzoom = halfH - (mapH - this.el.clientHeight);

				var left = newLeft > halfW && halfW || newLeft;
				if (newLeft < halfWzoom) left = halfWzoom;
				var top = newTop > halfH && halfH || newTop;
				if (newTop < halfHzoom) top = halfHzoom;

				this.imgMapEl.style.left = left + 'px';
				this.imgMapEl.style.top = top + 'px';
			}
		},
		stopDrag: function() {
			this.imgMapEl.style.cursor = 'grab';
			this.imgMapEl = null;
		},
		mapZoom: function(e) {
			e.preventDefault();
			e.stopPropagation();

			var mapEl = e.target;
			var deltaY = e.deltaY * -2;
			var origW = mapEl.naturalWidth;
			var origH = mapEl.naturalHeight;
			var widgetW = this.el.clientWidth;
			var widgetH = this.el.clientHeight;
			var newW = mapEl.width + deltaY;
			var newH = mapEl.height + (deltaY * (origH / origW));

			if (newW <= origW && newW >= widgetW && newH <= origH && newH >= widgetH) {
				mapEl.style.width = Math.floor(newW) + 'px';
				mapEl.style.height = Math.floor(newH) + 'px';
			}
		},
		shoWarn: function(msg) {
			setTimeout(function() {
				var warning = document.getElementById('tls_route_warn');
				if (warning) {
					if (msg) warning.innerHTML = msg;
					warning.style.opacity = 1;
				}
			}, 500);
		},
		_goToSettings: function(e) {
			e.preventDefault();
			this.do_action('tls_tollsync.tls_config_settings_action');
		}
	});
	widgetRegistry.add('tls_route', GMapRoute);
});