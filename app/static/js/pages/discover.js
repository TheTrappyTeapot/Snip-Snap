/* Script for app/static/js/pages/discover.js. */

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
  const initialFilters = [];  // Start with NO filters - only apply when user explicitly selects them

  const tagList = new TagList({
    mountEl: tagListMount,
    initialItems: initialFilters,
  });

  // Create filter selector DDL inline with search bar
  const filterContainer = document.createElement("div");
  filterContainer.className = "discover-filter-container";

  const label = document.createElement("label");
  label.textContent = "Sort by: ";
  label.className = "discover-filter-label";

  const select = document.createElement("select");
  select.className = "discover-filter-select";

  // Add the three filter options
  const filterOptions = [
    { id: 3, label: "Following" },
    { id: 2, label: "Most recent" },
    { id: 1, label: "Highest rated" },
    { id: 0, label: "Closest" }
  ];

  // Add a placeholder option
  const placeholderOption = document.createElement("option");
  placeholderOption.value = "";
  placeholderOption.textContent = "Add a filter...";
  placeholderOption.disabled = true;
  placeholderOption.selected = true;
  select.appendChild(placeholderOption);

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

    console.log(`[DISCOVER] Filter selection: filterId=${filterId}, isSelected=${isSelected}, currentFilters=`, currentFilters);

    if (isSelected) {
      // Remove filter
      const idx = currentFilters.findIndex(f => f.id === filterId && f.type === "filter");
      if (idx >= 0) {
        console.log(`[DISCOVER] Removing filter ${filterId} at index ${idx}`);
        tagList.remove_item_at(idx);
      }
    } else {
      // Add filter
      const filterItem = filterOptions.find(f => f.id === filterId);
      console.log(`[DISCOVER] Adding filter: filterId=${filterId}, filterItem=`, filterItem);
      if (filterItem) {
        tagList.add_item({ id: filterItem.id, type: "filter", label: filterItem.label });
        console.log(`[DISCOVER] Added filter, taglist now has:`, tagList.get_items());
      } else {
        console.error(`[DISCOVER] Filter not found in filterOptions: ${filterId}`);
      }
    }

    // Reset dropdown to placeholder
    select.value = "";
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
