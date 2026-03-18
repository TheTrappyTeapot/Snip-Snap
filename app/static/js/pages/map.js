(function () {
  "use strict";

  // ── Constants ────────────────────────────────────────────────────────────────
  const UK_CENTER = [54.5, -3.5];
  const UK_ZOOM = 6;
  const LOCATION_ZOOM = 14;
  const NOMINATIM_URL = "https://nominatim.openstreetmap.org/search";

  // ── State ────────────────────────────────────────────────────────────────────
  let userLat = null;
  let userLng = null;
  let userMarker = null;
  let allShops = [];

  // ── Search bar (always visible, items populated after shops load) ─────────────
  const searchBar = createSearchBarAutocomplete(
    "#map-search-bar",
    function (item) {
      const shop = allShops.find(function (s) {
        return s.barbershop_id === item.id;
      });
      if (shop) map.setView([shop.lat, shop.lng], LOCATION_ZOOM);
    },
    [],
    { placeholder: "Search barbershops..." }
  );

  // ── Map initialisation ───────────────────────────────────────────────────────
  const map = L.map("map", { zoomControl: true }).setView(UK_CENTER, UK_ZOOM);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(map);

  // ── DOM refs ─────────────────────────────────────────────────────────────────
  const locationModal = document.getElementById("location-modal");
  const locationInput = document.getElementById("location-input");
  const setLocationBtn = document.getElementById("set-location-btn");
  const useCurrentBtn = document.getElementById("use-current-location-btn");
  const myLocationBtn = document.getElementById("my-location-btn");
  const savePrompt = document.getElementById("save-location-prompt");
  const saveNoBtn = document.getElementById("save-location-no");
  const saveYesBtn = document.getElementById("save-location-yes");
  const locationModalClose = document.getElementById("location-modal-close");

  // ── User location marker (red circle) ───────────────────────────────────────
  function placeUserMarker(lat, lng) {
    if (userMarker) userMarker.remove();
    userMarker = L.circleMarker([lat, lng], {
      radius: 9,
      fillColor: "#e53e3e",
      color: "#fff",
      weight: 2,
      opacity: 1,
      fillOpacity: 0.9,
    })
      .addTo(map)
      .bindPopup("Your location");
  }

  // ── Location modal ───────────────────────────────────────────────────────────
  function showModal() {
    locationModal.classList.remove("hidden");
    locationInput.value = "";
    locationInput.focus();
  }

  function hideModal() {
    locationModal.classList.add("hidden");
  }

  // If arriving from barber profile widget, zoom straight to that location.
  // Otherwise use saved DB location, otherwise show modal.
  var _params = new URLSearchParams(window.location.search);
  var _pLat = parseFloat(_params.get("lat"));
  var _pLng = parseFloat(_params.get("lng"));
  if (!isNaN(_pLat) && !isNaN(_pLng)) {
    userLat = _pLat;
    userLng = _pLng;
    map.setView([userLat, userLng], LOCATION_ZOOM);
    placeUserMarker(userLat, userLng);
  } else if (window.__userLocation) {
    userLat = window.__userLocation.lat;
    userLng = window.__userLocation.lng;
    map.setView([userLat, userLng], LOCATION_ZOOM);
    placeUserMarker(userLat, userLng);
  } else {
    showModal();
  }

  myLocationBtn.addEventListener("click", showModal);
  locationModalClose.addEventListener("click", hideModal);

  // Set location by postcode / address (Nominatim geocoding)
  setLocationBtn.addEventListener("click", geocodeAndZoom);
  locationInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") geocodeAndZoom();
  });

  async function geocodeAndZoom() {
    const query = locationInput.value.trim();
    if (!query) return;

    setLocationBtn.textContent = "Searching\u2026";
    setLocationBtn.disabled = true;

    try {
      const res = await fetch(
        NOMINATIM_URL +
          "?q=" +
          encodeURIComponent(query) +
          "&format=json&limit=1&countrycodes=gb"
      );
      const data = await res.json();

      if (data.length === 0) {
        alert("Location not found. Try a different postcode or address.");
        return;
      }

      userLat = parseFloat(data[0].lat);
      userLng = parseFloat(data[0].lon);
      map.setView([userLat, userLng], LOCATION_ZOOM);
      placeUserMarker(userLat, userLng);
      hideModal();
      showSavePrompt();
    } catch (_) {
      alert("Could not search for location. Check your internet connection.");
    } finally {
      setLocationBtn.textContent = "Set Location";
      setLocationBtn.disabled = false;
    }
  }

  // Use browser geolocation
  useCurrentBtn.addEventListener("click", function () {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    useCurrentBtn.textContent = "Locating\u2026";
    useCurrentBtn.disabled = true;

    navigator.geolocation.getCurrentPosition(
      function (pos) {
        userLat = pos.coords.latitude;
        userLng = pos.coords.longitude;
        map.setView([userLat, userLng], LOCATION_ZOOM);
        placeUserMarker(userLat, userLng);
        hideModal();
        showSavePrompt();
        useCurrentBtn.textContent = "Use Current Location";
        useCurrentBtn.disabled = false;
      },
      function () {
        alert("Could not get your location. Please check your browser permissions.");
        useCurrentBtn.textContent = "Use Current Location";
        useCurrentBtn.disabled = false;
      }
    );
  });

  // ── Save location prompt ─────────────────────────────────────────────────────
  function showSavePrompt() {
    savePrompt.classList.remove("hidden");
  }

  function hideSavePrompt() {
    savePrompt.classList.add("hidden");
  }

  saveNoBtn.addEventListener("click", hideSavePrompt);

  saveYesBtn.addEventListener("click", function () {
    if (userLat !== null && userLng !== null) {
      fetch("/api/user/location", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lat: userLat, lng: userLng }),
      }).catch(function () {});
    }
    hideSavePrompt();
  });

  // ── Helpers ──────────────────────────────────────────────────────────────────
  function haversineKm(lat1, lng1, lat2, lng2) {
    const R = 6371;
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLng = ((lng2 - lng1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) ** 2 +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLng / 2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }

  function formatDistance(km) {
    return km < 1 ? Math.round(km * 1000) + "m" : km.toFixed(1) + "km";
  }

  // ── Barbershop popup (shows shop info, not individual barber) ────────────────
  function buildPopupHtml(shop) {
    const distHtml =
      userLat !== null
        ? '<div class="shop-popup-distance">\u25cf ' +
          formatDistance(haversineKm(userLat, userLng, shop.lat, shop.lng)) +
          "</div>"
        : "";

    const addressHtml = shop.postcode
      ? '<div class="shop-popup-meta">' + shop.postcode + "</div>"
      : "";

    const phoneHtml = shop.phone
      ? '<div class="shop-popup-meta"><a href="tel:' +
        shop.phone +
        '">' +
        shop.phone +
        "</a></div>"
      : "";

    const websiteHtml = shop.website
      ? '<div class="shop-popup-meta"><a href="' +
        shop.website +
        '" target="_blank" rel="noopener">Website</a></div>'
      : "";

    const barbersHtml =
      shop.barbers.length > 0
        ? '<div class="shop-popup-barbers">' +
          shop.barbers
            .map(function (b) {
              return (
                '<a class="shop-popup-barber-link" href="/barber/' +
                b.user_id +
                '">' +
                b.username +
                "</a>"
              );
            })
            .join("") +
          "</div>"
        : "";

    return (
      '<div class="shop-popup">' +
      '<div class="shop-popup-name">' +
      shop.name +
      "</div>" +
      distHtml +
      addressHtml +
      phoneHtml +
      websiteHtml +
      barbersHtml +
      "</div>"
    );
  }

  // Bind popup once at creation (function form so distance recalculates on open).
  // Leaflet handles click-to-open/close automatically.
  function addMarkers(shops) {
    shops.forEach(function (shop) {
      const marker = L.marker([shop.lat, shop.lng]).addTo(map);
      marker.bindPopup(function () {
        return buildPopupHtml(shop);
      }, { maxWidth: 240 });
    });
  }

  // ── Bootstrap ────────────────────────────────────────────────────────────────
  fetch("/api/barbershops")
    .then(function (res) {
      return res.json();
    })
    .then(function (shops) {
      allShops = shops;
      addMarkers(shops);

      const shopItems = shops.map(function (s) {
        return { id: s.barbershop_id, type: "barbershop", label: s.name };
      });
      searchBar.setItems(shopItems);
    })
    .catch(function () {
      console.error("Could not load barbershops from /api/barbershops");
    });
})();
