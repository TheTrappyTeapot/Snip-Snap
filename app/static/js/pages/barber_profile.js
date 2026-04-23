/* Script for app/static/js/pages/barber_profile.js. */

import { renderUserPromo } from "../components/userPromo.js";
import { renderTimetable } from "../components/timetable.js";
import { initBarberGallery } from "../components/barberGallery.js";

export async function initBarberProfile(config = {}) {
  const {
    userId,
    barbershopId,
    barberPromo = {},
    shifts = {},
    currentDay = 0,
    closingInfo = null,
    barberData = {}
  } = config;

  // Render user promo
  if (barberPromo && Object.keys(barberPromo).length > 0) {
    renderUserPromo("#user-promo-mount", {
      name: barberPromo.name || barberData.username || "Unknown",
      role: barberPromo.role || barberData.role || "barber",
      barbershop_name: barberPromo.barbershop_name || "",
      profile_image_url: barberPromo.profile_image_url || "",
      userId: userId,
      barbershopId: barbershopId
    }, {
      avatarSize: 56
    });
  }

  // Render timetable if shifts exist
  if (shifts && Object.keys(shifts).length > 0) {
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    renderTimetable("#barber-shifts-mount", {
      title: "Working Hours",
      schedule: shifts,
      dayLabels: daysOfWeek,
      currentDay: currentDay,
      closingInfo: closingInfo,
      cssPrefix: "barber-profile__",
      scheduleType: "shifts"
    });
  }

  // Initialize gallery - fetch barber_id from user_id first
  if (userId) {
    try {
      const response = await fetch(`/api/user/${userId}/barber-id`);
      if (response.ok) {
        const data = await response.json();
        const barberId = data.barber_id;
        initBarberGallery({
          mountEl: document.getElementById("barber-gallery-mount"),
          barberId: barberId
        });
      } else {
        console.error("Failed to fetch barber_id:", response.status);
        document.getElementById("barber-gallery-mount").innerHTML = "<p>Error loading gallery</p>";
      }
    } catch (error) {
      console.error("Error fetching barber_id:", error);
      document.getElementById("barber-gallery-mount").innerHTML = "<p>Error loading gallery</p>";
    }
  }

  // Initialize map if location exists
  if (barberData.location_lat !== null && barberData.location_lng !== null && barberData.shop_lat !== null && barberData.shop_lng !== null) {
    const shopLat = barberData.shop_lat || barberData.location_lat;
    const shopLng = barberData.shop_lng || barberData.location_lng;

    initMapWidget("#map-widget-mount", {
      center: [shopLat, shopLng],
      zoom: 14,
      shops: [{ lat: shopLat, lng: shopLng }]
    });

    // Fetch location name from Nominatim using shop location
    fetch(
      `https://nominatim.openstreetmap.org/reverse?lat=${shopLat}&lon=${shopLng}&format=json`
    )
      .then(r => r.json())
      .then(data => {
        const el = document.getElementById("location-display");
        if (!el || !data.address) return;
        const a = data.address;
        el.textContent = a.road
          ? (a.road + (a.city || a.town || a.village ? ", " + (a.city || a.town || a.village) : ""))
          : (a.city || a.town || a.village || a.county || data.display_name.split(",")[0]);
      })
      .catch(() => {
        const el = document.getElementById("location-display");
        if (el) el.textContent = "Location set";
      });

    // Setup Google Maps button
    const gmapsButton = document.getElementById("google-maps-button");
    if (gmapsButton) {
      gmapsButton.addEventListener("click", () => {
        const googlemapsUrl = `https://www.google.com/maps?q=${shopLat},${shopLng}`;
        window.open(googlemapsUrl, "_blank");
      });
    }
  }
}
