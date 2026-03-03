function createEl(tag, className, attrs = {}) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  Object.entries(attrs).forEach(([key, value]) => {
    if (value === null || value === undefined) return;
    el.setAttribute(key, String(value));
  });
  return el;
}

function createDefaultAvatarSvg(size) {
  const svgNs = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgNs, "svg");
  svg.setAttribute("viewBox", "0 0 24 24");
  svg.setAttribute("width", String(size));
  svg.setAttribute("height", String(size));
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("focusable", "false");

  const circle = document.createElementNS(svgNs, "circle");
  circle.setAttribute("cx", "12");
  circle.setAttribute("cy", "8");
  circle.setAttribute("r", "4");
  circle.setAttribute("fill", "currentColor");

  const path = document.createElementNS(svgNs, "path");
  path.setAttribute("d", "M4 20a8 8 0 0 1 16 0");
  path.setAttribute("fill", "none");
  path.setAttribute("stroke", "currentColor");
  path.setAttribute("stroke-width", "2");
  path.setAttribute("stroke-linecap", "round");

  svg.appendChild(circle);
  svg.appendChild(path);
  return svg;
}

function createAvatar(size, imageUrl, altText) {
  const avatar = createEl("div", "userPromo__avatar");
  avatar.style.width = `${size}px`;
  avatar.style.height = `${size}px`;
  avatar.style.borderRadius = "50%";
  avatar.style.overflow = "hidden";
  avatar.style.display = "grid";
  avatar.style.placeItems = "center";
  avatar.style.background = "#e9ecef";
  avatar.style.flexShrink = "0";

  const cleanUrl = typeof imageUrl === "string" ? imageUrl.trim() : "";
  if (cleanUrl) {
    const img = document.createElement("img");
    img.src = cleanUrl;
    img.alt = altText;
    img.loading = "lazy";
    img.style.width = "100%";
    img.style.height = "100%";
    img.style.objectFit = "cover";
    img.addEventListener("error", () => {
      avatar.textContent = "";
      const fallback = createDefaultAvatarSvg(Math.max(20, Math.floor(size * 0.6)));
      fallback.style.color = "#9aa1a9";
      avatar.appendChild(fallback);
    });
    avatar.appendChild(img);
  } else {
    const fallback = createDefaultAvatarSvg(Math.max(20, Math.floor(size * 0.6)));
    fallback.style.color = "#9aa1a9";
    avatar.appendChild(fallback);
  }

  return avatar;
}

function buildPromoRow(data, options = {}) {
  const size = Number(options.avatarSize) || 36;
  const safeSize = Math.min(40, Math.max(32, size));
  const name = typeof data?.name === "string" && data.name.trim() ? data.name.trim() : "Unknown";
  const role = typeof data?.role === "string" ? data.role.trim().toLowerCase() : "";
  const barbershopName =
    typeof data?.barbershop_name === "string" && data.barbershop_name.trim()
      ? data.barbershop_name.trim()
      : "";

  const row = createEl("div", "userPromo userPromo--ready");
  row.style.display = "flex";
  row.style.alignItems = "center";
  row.style.gap = "10px";
  row.style.minHeight = `${safeSize}px`;

  const avatar = createAvatar(safeSize, data?.profile_image_url, `${name} profile image`);

  const textWrap = createEl("div", "userPromo__text");
  const title = createEl("div", "userPromo__name");
  title.style.fontWeight = "700";
  title.textContent = name;
  textWrap.appendChild(title);

  if (role === "barber" && barbershopName) {
    const subtitle = createEl("div", "userPromo__shop");
    subtitle.style.fontSize = "0.875rem";
    subtitle.style.opacity = "0.85";
    subtitle.textContent = barbershopName;
    textWrap.appendChild(subtitle);
  }

  row.appendChild(avatar);
  row.appendChild(textWrap);
  return row;
}

function buildSkeleton(options = {}) {
  const size = Number(options.avatarSize) || 36;
  const safeSize = Math.min(40, Math.max(32, size));

  const row = createEl("div", "userPromo userPromo--loading", { "aria-busy": "true" });
  row.style.display = "flex";
  row.style.alignItems = "center";
  row.style.gap = "10px";

  const avatar = createEl("div", "userPromo__avatarSkeleton");
  avatar.style.width = `${safeSize}px`;
  avatar.style.height = `${safeSize}px`;
  avatar.style.borderRadius = "50%";
  avatar.style.background = "#e9ecef";
  avatar.style.flexShrink = "0";

  const textWrap = createEl("div", "userPromo__textSkeleton");
  textWrap.style.display = "grid";
  textWrap.style.gap = "6px";
  textWrap.style.minWidth = "120px";

  const line1 = createEl("div", "userPromo__line userPromo__line--name");
  line1.style.height = "10px";
  line1.style.width = "90px";
  line1.style.borderRadius = "6px";
  line1.style.background = "#eceff2";

  const line2 = createEl("div", "userPromo__line userPromo__line--sub");
  line2.style.height = "9px";
  line2.style.width = "130px";
  line2.style.borderRadius = "6px";
  line2.style.background = "#f2f4f6";

  textWrap.appendChild(line1);
  textWrap.appendChild(line2);
  row.appendChild(avatar);
  row.appendChild(textWrap);
  return row;
}

export async function mountUserPromo(containerEl, userId, options = {}) {
  const container = typeof containerEl === "string" ? document.querySelector(containerEl) : containerEl;
  if (!container) return null;

  container.textContent = "";
  container.appendChild(buildSkeleton(options));

  const defaultPayload = {
    name: "Unknown",
    role: "",
    barbershop_name: "",
    profile_image_url: "",
  };

  try {
    const response = await fetch(`/api/users/${encodeURIComponent(String(userId))}/promo`, {
      headers: { Accept: "application/json" },
      signal: options.signal,
    });

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    const payload = await response.json();
    container.textContent = "";
    const row = buildPromoRow({ ...defaultPayload, ...payload }, options);
    container.appendChild(row);
    return row;
  } catch (_error) {
    container.textContent = "";
    const row = buildPromoRow(defaultPayload, options);
    container.appendChild(row);
    return row;
  }
}

export function initUserPromos(root = document) {
  const host = root && typeof root.querySelectorAll === "function" ? root : document;
  const nodes = host.querySelectorAll(".js-user-promo[data-user-id]");
  const mounts = [];

  nodes.forEach((el) => {
    const userId = el.getAttribute("data-user-id");
    if (!userId) return;
    mounts.push(mountUserPromo(el, userId));
  });

  return Promise.allSettled(mounts);
}
