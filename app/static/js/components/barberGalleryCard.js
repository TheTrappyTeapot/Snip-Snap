/* Script for app/static/js/components/barberGalleryCard.js. */

import { renderUserPromo } from "./userPromo.js";

export function renderBarberGalleryCard(photo) {
  const card = document.createElement("div");
  card.className = "barber-gallery-card";

  // Image container
  const media = document.createElement("div");
  media.className = "barber-gallery-card__media";

  const img = document.createElement("img");
  img.className = "barber-gallery-card__img";
  img.src = photo.image_url;
  img.alt = "Haircut";
  img.loading = "lazy";

  media.appendChild(img);

  // Barber promo overlay (top)
  const promoMount = document.createElement("div");
  promoMount.className = "barber-gallery-card__promo";
  
  renderUserPromo(promoMount, {
    name: photo.promo_name || "Unknown",
    role: photo.promo_role || "barber",
    barbershop_name: photo.promo_barbershop_name || "",
    profile_image_url: photo.promo_profile_image_url || ""
  }, { avatarSize: 28 });

  media.appendChild(promoMount);

  // Tag label overlay (bottom)
  const tagEl = document.createElement("div");
  tagEl.className = "barber-gallery-card__tag";
  if (photo.main_tag_name) {
    tagEl.textContent = photo.main_tag_name;
  }

  media.appendChild(tagEl);

  card.appendChild(media);

  return card;
}
