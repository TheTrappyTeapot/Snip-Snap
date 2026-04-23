/* Script for /home/runner/work/Snip-Snap/Snip-Snap/app/static/js/pages/discover.js. */

import { TagList } from "../components/tagList.js";
import { initPostGallery } from "../features/postGallery.js";
import { initDiscoverSearch } from "../features/discoverSearch.js";

const tagListMount = document.getElementById("tagListMount");
const galleryMount = document.getElementById("postGalleryMount");
const sentinelEl = document.getElementById("postGallerySentinel");
const searchMount = document.getElementById("searchBarMount");
const out = document.getElementById("discoverSelection");
const discoverActionsEl = document.querySelector(".discover-actions");

async function initDiscoverPage() {
  // Fetch all available search items to get filter labels
  let filterItems = [];
  try {
    const res = await fetch("/api/discover/search_items");
    if (res.ok) {
      const data = await res.json();
      filterItems = (data.items || []).filter(item => item.type === "filter");
    }
  } catch (e) {
    console.error("[DISCOVER] Failed to fetch search items:", e);
  }

  // Create initial filter items with proper labels
  const initialFilters = [
    filterItems.find(f => f.id === 2) || { id: 2, type: "filter", label: "Most recent" },
    filterItems.find(f => f.id === 1) || { id: 1, type: "filter", label: "Highest rated" },
    filterItems.find(f => f.id === 0) || { id: 0, type: "filter", label: "Closest" },
  ];

  const tagList = new TagList({
    mountEl: tagListMount,
    initialItems: initialFilters,
  });

  // Create filter selector DDL inline with search bar
  const filterContainer = document.createElement("div");
  filterContainer.style.display = "flex";
  filterContainer.style.gap = "12px";
  filterContainer.style.alignItems = "center";

  const label = document.createElement("label");
  label.textContent = "Sort by: ";
  label.style.fontWeight = "500";
  label.style.fontSize = "14px";
  label.style.whiteSpace = "nowrap";

  const select = document.createElement("select");
  select.style.padding = "8px 12px";
  select.style.borderRadius = "4px";
  select.style.border = "1px solid #ddd";
  select.style.fontSize = "14px";
  select.style.cursor = "pointer";
  select.style.minWidth = "150px";

  // Add the three filter options
  const filterOptions = [
    { id: 2, label: "Most recent" },
    { id: 1, label: "Highest rated" },
    { id: 0, label: "Closest" },
  ];

  for (const filter of filterOptions) {
    const option = document.createElement("option");
    option.value = filter.id;
    option.textContent = filter.label;
    select.appendChild(option);
  }

  // Handle filter selection - toggle the filter on/off
  select.addEventListener("change", (e) => {
    const filterId = parseInt(e.target.value);
    const currentFilters = tagList.get_items();
    const isSelected = currentFilters.some(f => f.id === filterId && f.type === "filter");

    if (isSelected) {
      // Remove filter
      const idx = currentFilters.findIndex(f => f.id === filterId && f.type === "filter");
      if (idx >= 0) {
        tagList.remove_item_at(idx);
      }
    } else {
      // Add filter
      const filterItem = filterOptions.find(f => f.id === filterId);
      tagList.add_item({ id: filterItem.id, type: "filter", label: filterItem.label });
    }

    // Reset dropdown to show first option
    select.value = filterOptions[0].id;
  });

  filterContainer.appendChild(label);
  filterContainer.appendChild(select);
  discoverActionsEl.appendChild(filterContainer);

  initPostGallery({
    mountEl: galleryMount,
    sentinelEl,
    tagList,
    config: {
      endpoint: "/api/gallery/posts",
      columns: 3,
      limit: 18,
    },
  });

  initDiscoverSearch({
    mountEl: searchMount,
    outEl: out,
    tagList,
    config: {
      endpoint: "/api/discover/search_items",
    },
  });
}

// Initialize when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initDiscoverPage);
} else {
  initDiscoverPage();
}
