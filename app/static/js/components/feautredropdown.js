class FilterDropdown {
  constructor(mountElementId, tagListInstance) {
    // Store reference to TagList
    this.tagList = tagListInstance;

    // Define allowed filter options
    this.options = [
      "Most recent",
      "Closest",
      "Highest rated"
    ];

    // Get mount element
    this.mountElement = document.getElementById(mountElementId);

    if (!this.mountElement) {
      console.error(`FilterDropdown: Mount element '${mountElementId}' not found`);
      return;
    }

    if (!this.tagList || typeof this.tagList.add_item !== "function") {
      console.error("FilterDropdown: Invalid TagList instance provided");
      return;
    }

    // Render UI
    this.render();
  }

  render() {
    // Clear mount element (important rule)
    this.mountElement.innerHTML = "";

    // Create dropdown select element
    const select = document.createElement("select");
    select.className = "filter-dropdown-select";

    // Default placeholder option
    const placeholder = document.createElement("option");
    placeholder.textContent = "Select filter";
    placeholder.disabled = true;
    placeholder.selected = true;
    select.appendChild(placeholder);

    // Create options
    this.options.forEach(optionText => {
      const option = document.createElement("option");
      option.value = optionText.toLowerCase();
      option.textContent = optionText;
      select.appendChild(option);
    });

    // Add change event
    select.addEventListener("change", (event) => {
      const selectedValue = event.target.value;

      // Call TagList API exactly as required
      this.tagList.add_item({
        name: selectedValue,
        type: "filter"
      });

      // Reset dropdown to placeholder
      select.selectedIndex = 0;
    });

    // Mount into provided div
    this.mountElement.appendChild(select);
  }
}
