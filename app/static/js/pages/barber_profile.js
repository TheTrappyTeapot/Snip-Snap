/* Script for app/static/js/pages/barber_profile.js. */

import { renderUserPromo } from "../components/userPromo.js";
import { renderTimetable } from "../components/timetable.js";
import { initBarberGallery } from "../components/barberGallery.js";

async function renderRatingInfo(mountSelector, barberId) {
  const mountEl = document.querySelector(mountSelector);
  if (!mountEl) return;

  try {
    // Fetch reviews to get rating data
    const response = await fetch(`/api/barber/${barberId}/reviews`);
    if (!response.ok) {
      mountEl.innerHTML = "";
      return;
    }

    const data = await response.json();
    const reviews = data.reviews || [];

    // Calculate average rating
    let totalRating = 0;
    let ratingCount = 0;
    reviews.forEach(review => {
      if (review.rating !== null && review.rating !== undefined) {
        totalRating += review.rating;
        ratingCount++;
      }
    });

    const avgRating = ratingCount > 0 ? (totalRating / ratingCount).toFixed(1) : null;

    // Render rating info
    mountEl.innerHTML = "";
    const container = document.createElement("div");
    container.className = "rating-info-widget";

    if (avgRating !== null) {
      container.innerHTML = `
        <div class="rating-info-widget__content">
          <div class="rating-info-widget__stars">
            <span class="rating-info-widget__rating">${avgRating}</span>
            <div class="rating-info-widget__stars-display">
              ${'⭐'.repeat(Math.round(avgRating))}
            </div>
          </div>
          <div class="rating-info-widget__stats">
            <div class="rating-info-widget__count">${ratingCount} review${ratingCount !== 1 ? 's' : ''}</div>
          </div>
        </div>
      `;
    } else {
      container.innerHTML = `
        <div class="rating-info-widget__content">
          <div class="rating-info-widget__no-reviews">No reviews yet</div>
        </div>
      `;
    }

    mountEl.appendChild(container);
  } catch (e) {
    console.error("Failed to render rating info:", e);
    mountEl.innerHTML = "";
  }
}

export async function initBarberProfile(config = {}) {
  const {
    userId,
    barberId: configBarberId,
    barbershopId,
    barberPromo = {},
    shifts = {},
    currentDay = 0,
    closingInfo = null,
    barberData = {}
  } = config;

  // Fetch barber_id from user_id first
  let barberId = null;
  if (userId) {
    try {
      const response = await fetch(`/api/user/${userId}/barber-id`);
      if (response.ok) {
        const data = await response.json();
        barberId = data.barber_id;
      }
    } catch (e) {
      console.error("Failed to fetch barber_id:", e);
    }
  }

  // Render user promo with following status
  if (barberPromo && Object.keys(barberPromo).length > 0) {
    // Fetch following status if barberId is provided
    let isFollowing = false;
    if (barberId) {
      try {
        const res = await fetch(`/api/barber/${barberId}/following-status`);
        if (res.ok) {
          const data = await res.json();
          isFollowing = data.is_following || false;
        }
      } catch (e) {
        console.error("Failed to fetch following status:", e);
      }
    }

    renderUserPromo("#user-promo-mount", {
      name: barberPromo.name || barberData.username || "Unknown",
      role: barberPromo.role || barberData.role || "barber",
      barbershop_name: barberPromo.barbershop_name || "",
      profile_image_url: barberPromo.profile_image_url || "",
      userId: userId,
      barberId: barberId,
      barbershopId: barbershopId
    }, {
      avatarSize: 56,
      isFollowing: isFollowing
    });
  }

  // Render average rating info
  if (barberId) {
    renderRatingInfo("#rating-info-mount", barberId);
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

  // Initialize gallery using the barber_id we already fetched
  if (barberId) {
    initBarberGallery({
      mountEl: document.getElementById("barber-gallery-mount"),
      barberId: barberId
    });
  } else if (userId) {
    // Fallback: try to fetch barber_id if not already available
    try {
      const response = await fetch(`/api/user/${userId}/barber-id`);
      if (response.ok) {
        const data = await response.json();
        barberId = data.barber_id;
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
