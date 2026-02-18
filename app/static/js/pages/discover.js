(function () {
  const mount = document.getElementById("searchBarMount");
  const out = document.getElementById("discoverSelection");

  // Hardcoded test data (NOT fruit), with table names as types and PK-like IDs.
  // Replace later with real DB/API results.
  const all_items = [
    // tags
    { id: 101, type: "tag", label: "Fade" },
    { id: 102, type: "tag", label: "Skin fade" },
    { id: 103, type: "tag", label: "Beard trim" },
    { id: 104, type: "tag", label: "Hot towel" },
    { id: 105, type: "tag", label: "Scissor cut" },

    // barbers
    { id: 201, type: "barber", label: "George Hart" },
    { id: 202, type: "barber", label: "Sam Patel" },
    { id: 203, type: "barber", label: "Ayesha Khan" },

    // barbershops
    { id: 301, type: "barbershop", label: "Kingsclere Cuts" },
    { id: 302, type: "barbershop", label: "Basingstoke Barbers" },
    { id: 303, type: "barbershop", label: "Reading Groom Room" },

    // Deliberate disambiguation collision example
    { id: 204, type: "barber", label: "Fade King" },
    { id: 304, type: "barbershop", label: "Fade King" },
  ];

  function send_selected_item_here(item) {
    // This is the contract: you get the FULL object.
    // Later you’ll likely trigger fetch/navigation based on item.type & item.id.
    out.textContent = `Selected: ${item.label}  (type: ${item.type}, id: ${item.id})`;
  }

  // Mount the shared autocomplete component
  window.createSearchBarAutocomplete(mount, send_selected_item_here, all_items, {
    placeholder: "Search tags, barbers, or shops…",
  });
})();
