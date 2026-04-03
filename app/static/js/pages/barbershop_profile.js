import { renderUserPromo } from "../components/userPromo.js";
import { renderTimetable } from "../components/timetable.js";
import { initBarbershopGallery } from "../components/barberGallery.js";

export function initBarbershopProfile(config = {}) {
  const {
    barbershopId,
    barbers = [],
    shopData = {},
    openingHours = {},
    currentDay = 0,
    closingInfo = null
  } = config;

  // Render user promos for each barber
  if (barbers && barbers.length > 0) {
    barbers.forEach((barber, index) => {
      renderUserPromo(`#promo-${barber.user_id || index + 1}`, {
        name: barber.promo?.name || barber.username || "Unknown",
        role: barber.promo?.role || "barber",
        barbershop_name: barber.promo?.barbershop_name || shopData.name || "",
        profile_image_url: barber.promo?.profile_image_url || ""
      }, {
        avatarSize: 48
      });
    });
  }

  // Initialize gallery
  if (barbershopId) {
    initBarbershopGallery({
      mountEl: document.getElementById("barbershop-gallery-mount"),
      barbershopId: barbershopId
    });
  }

  // Initialize map if location exists
  if (shopData.location_lat !== null && shopData.location_lng !== null) {
    initMapWidget("#map-widget-mount", {
      center: [shopData.location_lat, shopData.location_lng],
      marker: [shopData.location_lat, shopData.location_lng],
      zoom: 14
    });
  }

  // Render timetable if opening hours exist
  if (openingHours && Object.keys(openingHours).length > 0) {
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    renderTimetable("#barbershop-hours-mount", {
      title: "Opening Hours",
      schedule: openingHours,
      dayLabels: daysOfWeek,
      currentDay: currentDay,
      closingInfo: closingInfo,
      cssPrefix: "barbershop__",
      scheduleType: "opening_hours"
    });
  }
}
