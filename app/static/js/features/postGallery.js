import { renderGalleryGrid } from "../components/galleryGrid.js";
import { renderPostImageCard } from "../components/postImageCard.js";

function normaliseTagListItems(items) {
  const filter_ids = [];
  const tag_ids = [];
  const barber_ids = [];
  const barbershop_ids = [];

  for (const it of items || []) {
    if (!it || typeof it.id !== "number" || typeof it.type !== "string") continue;

    if (it.type === "filter") filter_ids.push(it.id);
    if (it.type === "tag") tag_ids.push(it.id);
    if (it.type === "barber") barber_ids.push(it.id);
    if (it.type === "barbershop") barbershop_ids.push(it.id);
  }

  return {
    filter_ids,
    tag_ids,
    barber_ids,
    barbershop_ids
  };
}

function resolveEffectiveSort(filter_ids) {
  const set = new Set(filter_ids || []);
  if (set.has(2)) return "most_recent";
  if (set.has(1) && set.size === 1) return "highest_rated";
  if (set.has(0) && set.size === 1) return "closest";
  if (set.size > 1) return "most_recent";
  return "most_recent";
}

async function fetchPosts({ endpoint, payload }) {
  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed: ${res.status}`);
  }

  return await res.json();
}

export function initPostGallery({ mountEl, sentinelEl, tagList, config }) {
  const state = {
    items: [],
    cursor: null,
    has_more: true,
    loading: false,
    error: null,
    lastPayloadKey: ""
  };

  const endpoint = (config && config.endpoint) || "/api/gallery/posts";
  const columns = (config && config.columns) || 3;
  const limit = (config && config.limit) || 18;

  function render() {
    if (state.error) {
      mountEl.innerHTML = "";
      const p = document.createElement("p");
      p.textContent = "Could not load posts. Refresh or adjust filters.";
      mountEl.appendChild(p);
      return;
    }

    if (!state.loading && state.items.length === 0) {
      mountEl.innerHTML = "";
      const p = document.createElement("p");
      p.textContent = "No posts found.";
      mountEl.appendChild(p);
      return;
    }

    renderGalleryGrid({
      mountEl,
      items: state.items,
      columns,
      renderItem: renderPostImageCard
    });
  }

  function buildPayload({ cursor }) {
    const tagItems = tagList.get_items();
    const parts = normaliseTagListItems(tagItems);
    const effective_sort = resolveEffectiveSort(parts.filter_ids);

    return {
      filter_ids: parts.filter_ids,
      effective_sort,
      tag_ids: parts.tag_ids,
      barber_ids: parts.barber_ids,
      barbershop_ids: parts.barbershop_ids,
      cursor: cursor,
      limit: limit
    };
  }

  function payloadKey(payload) {
    const keyObj = {
      filter_ids: payload.filter_ids.slice().sort((a, b) => a - b),
      effective_sort: payload.effective_sort,
      tag_ids: payload.tag_ids.slice().sort((a, b) => a - b),
      barber_ids: payload.barber_ids.slice().sort((a, b) => a - b),
      barbershop_ids: payload.barbershop_ids.slice().sort((a, b) => a - b),
      limit: payload.limit
    };
    return JSON.stringify(keyObj);
  }

  async function loadFirstPage() {
    state.loading = true;
    state.error = null;
    state.items = [];
    state.cursor = null;
    state.has_more = true;

    const payload = buildPayload({ cursor: null });
    state.lastPayloadKey = payloadKey(payload);

    try {
      const data = await fetchPosts({ endpoint, payload });
      state.items = Array.isArray(data.items) ? data.items : [];
      state.cursor = data.next_cursor || null;
      state.has_more = !!data.has_more;
    } catch (e) {
      state.error = e;
    } finally {
      state.loading = false;
      render();
    }
  }

  async function loadNextPage() {
    if (state.loading || !state.has_more) return;

    const payload = buildPayload({ cursor: state.cursor });
    const key = payloadKey(payload);

    if (key !== state.lastPayloadKey) return;

    state.loading = true;
    state.error = null;

    try {
      const data = await fetchPosts({ endpoint, payload });
      const newItems = Array.isArray(data.items) ? data.items : [];
      state.items = state.items.concat(newItems);
      state.cursor = data.next_cursor || null;
      state.has_more = !!data.has_more;
    } catch (e) {
      state.error = e;
    } finally {
      state.loading = false;
      render();
    }
  }

  tagList.on_change(() => {
    loadFirstPage();
  });

  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) loadNextPage();
    }
  });

  io.observe(sentinelEl);

  loadFirstPage();

  return {
    reload: loadFirstPage
  };
}