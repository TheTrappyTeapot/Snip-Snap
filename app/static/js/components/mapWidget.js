/**
 * mapWidget — small read-only map showing barbershop pins.
 * Clicking the widget navigates to /map.
 *
 * Usage:
 *   <div id="map-widget-mount"></div>
 *   <script src="...leaflet.js"></script>
 *   <script src="...mapWidget.js"></script>
 *   <script>initMapWidget("#map-widget-mount");</script>
 *
 * Requires Leaflet to be loaded on the page before this script runs.
 */
(function () {
  "use strict";

  function initMapWidget(mountEl, opts) {
    opts = opts || {};
    const mount =
      typeof mountEl === "string" ? document.querySelector(mountEl) : mountEl;
    if (!mount) return;

    // ── Build DOM ──────────────────────────────────────────────────────────────
    const wrapper = document.createElement("div");
    wrapper.className = "map-widget-wrapper";

    const mapDiv = document.createElement("div");
    mapDiv.className = "map-widget-map";

    // Clickable overlay with "View Map" label
    const overlay = document.createElement("div");
    overlay.className = "map-widget-overlay";
    overlay.innerHTML = "<span>View Map</span>";

    wrapper.appendChild(mapDiv);
    wrapper.appendChild(overlay);
    mount.innerHTML = "";
    mount.appendChild(wrapper);

    const center = opts.center || [54.5, -3.5];
    const zoom = opts.zoom || 6;

    // ── Leaflet mini-map (all interaction disabled) ────────────────────────────
    const miniMap = L.map(mapDiv, {
      zoomControl: false,
      dragging: false,
      touchZoom: false,
      doubleClickZoom: false,
      scrollWheelZoom: false,
      boxZoom: false,
      keyboard: false,
      attributionControl: false,
    }).setView(center, zoom);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
    }).addTo(miniMap);

    // ── Load barbershop pins ───────────────────────────────────────────────────
    fetch("/api/barbershops")
      .then(function (res) {
        return res.json();
      })
      .then(function (shops) {
        if (!Array.isArray(shops) || shops.length === 0) return;

        shops.forEach(function (shop) {
          L.marker([shop.lat, shop.lng]).addTo(miniMap);
        });

        // Only auto-fit if no explicit center was given
        if (!opts.center) {
          const bounds = L.latLngBounds(
            shops.map(function (s) {
              return [s.lat, s.lng];
            })
          );
          miniMap.fitBounds(bounds, { padding: [20, 20], maxZoom: 14 });
        }

        // Show a highlighted pin at the specific location if provided
        if (opts.marker) {
          L.marker(opts.marker).addTo(miniMap);
        }
      })
      .catch(function () {
        // Silently fail — widget still shows map tiles
      });

    // ── Click overlay → go to map page (with coords if available) ─────────────
    overlay.addEventListener("click", function () {
      if (opts.center) {
        window.location.href =
          "/map?lat=" + opts.center[0] + "&lng=" + opts.center[1];
      } else {
        window.location.href = "/map";
      }
    });
  }

  window.initMapWidget = initMapWidget;
})();
