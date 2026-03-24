console.log("profile.js script loading");

// Prevent double-loading
if (window.__profileJsLoaded) {
  console.warn("profile.js already loaded, skipping");
} else {
  window.__profileJsLoaded = true;

  // Initialize form when DOM is ready
  function initializeForm() {
    console.log("Initializing profile form...");

    const profileForm = document.getElementById("profileForm");
    const submitBtn = document.getElementById("submitBtn");
    const usernameInput = document.getElementById("username");
    const locationInput = document.getElementById("location");
    const usernameError = document.getElementById("usernameError");
    const locationError = document.getElementById("locationError");
    const roleError = document.getElementById("roleError");
    const barbershopError = document.getElementById("barbershopError");
    const generalError = document.getElementById("generalError");
    const roleRadios = document.querySelectorAll('input[name="role"]');
    const barbershopField = document.getElementById("barbershopField");
    const barbershopSearchContainer = document.getElementById("barbershopSearchContainer");
    const sessionDataEl = document.getElementById("sessionData");

    if (!profileForm) {
      console.error("Profile form not found in the page");
      return;
    }

    console.log("DOM elements loaded:", {
      profileForm: !!profileForm,
      submitBtn: !!submitBtn,
      usernameInput: !!usernameInput,
      locationInput: !!locationInput,
    });

    // Get current user role from data attribute
    const currentRole = sessionDataEl?.getAttribute("data-current-role") || "customer";
    console.log("Current role:", currentRole);

    // Get current postcode from window.__userPostcode
    const currentPostcode = window.__userPostcode || "";
    console.log("window.__userPostcode:", window.__userPostcode);
    console.log("Current postcode from window.__userPostcode:", currentPostcode);

    // Set current postcode as both value and placeholder
    if (currentPostcode && currentPostcode !== "null") {
      locationInput.value = currentPostcode;
      locationInput.placeholder = currentPostcode;
      console.log("✓ Location input value set to:", locationInput.value);
      console.log("✓ Location input placeholder set to:", locationInput.placeholder);
    } else {
      console.log("✗ No postcode available (currentPostcode is:", currentPostcode, ")");
      locationInput.value = "";
      locationInput.placeholder = "Enter your postcode";
    }

    // Set current role in radio buttons
    const currentRoleRadio = document.querySelector(`input[name="role"][value="${currentRole}"]`);
    if (currentRoleRadio) {
      currentRoleRadio.checked = true;
      console.log("Current role set to:", currentRole);
    }

    // Autocomplete instance for barbershop
    let barbershopAutocomplete = null;
    let selectedBarbershopId = null;

    // Load barbershops for autocomplete
    async function loadBarbershops() {
      try {
        console.log("📦 Loading barbershops from API...");
        const response = await fetch("/api/user/barbershops");
        if (!response.ok) {
          console.error("✗ API request failed with status:", response.status);
          throw new Error("Failed to load barbershops");
        }
        const data = await response.json();
        console.log("✓ Barbershops loaded:", data.barbershops?.length || 0, "shops");
        return data.barbershops || [];
      } catch (error) {
        console.error("✗ Error loading barbershops:", error);
        return [];
      }
    }

    // Initialize barbershop autocomplete
    async function initializeBarbershopAutocomplete() {
      console.log("🏪 Initializing barbershop autocomplete...");
      const barbershops = await loadBarbershops();

      // Convert to autocomplete format
      const barbershopItems = barbershops.map((shop) => ({
        id: shop.barbershop_id,
        type: "barbershop",
        label: shop.name,
      }));

      console.log("🏪 Barbershop autocomplete items ready:", barbershopItems.length);

      barbershopAutocomplete = window.createSearchBarAutocomplete(
        barbershopSearchContainer,
        (selectedItem) => {
          console.log("🏪 Barbershop selected:", selectedItem);
          selectedBarbershopId = selectedItem.id;
        },
        barbershopItems,
        { placeholder: "Search barbershops…" }
      );
      console.log("✓ Barbershop autocomplete initialized");
    }

    // Load current barber's barbershop if applicable
    async function loadCurrentBarbershop() {
      try {
        console.log("🏪 Loading current barber's barbershop...");
        const response = await fetch("/api/user/current-barbershop");
        if (!response.ok) {
          console.log("⚠️ No current barbershop found (status:", response.status, ")");
          return;
        }
        const data = await response.json();
        console.log("🏪 Current barbershop:", data);

        if (data.barbershop && barbershopAutocomplete) {
          // Set the autocomplete value
          const input = barbershopSearchContainer.querySelector(".sa-input");
          if (input) {
            input.value = data.barbershop.name;
            selectedBarbershopId = data.barbershop.barbershop_id;
            console.log("✓ Barbershop input set to:", data.barbershop.name);
          }
        }
      } catch (error) {
        console.error("✗ Error loading current barbershop:", error);
      }
    }

    // Show/hide barbershop field based on role
    async function updateBarbershopFieldVisibility() {
      const selectedRole = document.querySelector('input[name="role"]:checked')?.value;
      console.log("🔄 updateBarbershopFieldVisibility called, selectedRole:", selectedRole);

      if (selectedRole === "barber") {
        console.log("👷 Barber role selected, showing barbershop field");
        barbershopField.style.display = "grid";
        
        // Initialize autocomplete if not already done
        if (!barbershopAutocomplete) {
          console.log("⚙️ Initializing barbershop autocomplete...");
          await initializeBarbershopAutocomplete();
          await loadCurrentBarbershop();
        } else {
          console.log("✓ Barbershop autocomplete already initialized");
        }
      } else {
        console.log("👤 Non-barber role selected, hiding barbershop field");
        barbershopField.style.display = "none";
        selectedBarbershopId = null;
      }
    }

    // Attach role change listeners
    roleRadios.forEach((radio) => {
      radio.addEventListener("change", updateBarbershopFieldVisibility);
    });

    // Form validation
    function clearErrors() {
      usernameError.textContent = "";
      locationError.textContent = "";
      roleError.textContent = "";
      barbershopError.textContent = "";
      generalError.textContent = "";
    }

    function validateForm(username, location, role) {
      console.log("🔍 Validating form:", { username, location, role });
      clearErrors();
      let isValid = true;

      // Username validation
      if (!username || username.trim().length === 0) {
        usernameError.textContent = "Username is required";
        console.log("✗ Username validation failed: empty");
        isValid = false;
      } else if (username.length < 2) {
        usernameError.textContent = "Username must be at least 2 characters";
        console.log("✗ Username validation failed: too short");
        isValid = false;
      } else if (username.length > 50) {
        usernameError.textContent = "Username must be less than 50 characters";
        console.log("✗ Username validation failed: too long");
        isValid = false;
      } else {
        console.log("✓ Username validation passed");
      }

      // Location validation (optional but if provided must be valid)
      if (location && location.length > 10) {
        locationError.textContent = "Location must be 10 characters or fewer";
        console.log("✗ Location validation failed: too long");
        isValid = false;
      } else if (location) {
        console.log("✓ Location validation passed");
      }

      // Role validation
      if (!role) {
        roleError.textContent = "Please select an account type";
        console.log("✗ Role validation failed: empty");
        isValid = false;
      } else {
        console.log("✓ Role validation passed");
      }

      // Barbershop validation for barbers
      if (role === "barber" && !selectedBarbershopId) {
        barbershopError.textContent = "Please select a barbershop";
        console.log("✗ Barbershop validation failed: required for barber");
        isValid = false;
      } else if (role === "barber") {
        console.log("✓ Barbershop validation passed");
      }

      console.log("Validation result:", isValid ? "✓ VALID" : "✗ INVALID");
      return isValid;
    }

    // Geocode postcode helper
    async function geocodePostcode(postcode) {
      if (!postcode || postcode.trim().length === 0) {
        console.log("geocodePostcode called with empty postcode");
        return { lat: null, lng: null };
      }

      try {
        console.log("🌐 Geocoding postcode:", postcode);
        // Using postcodes.io for UK postcode geocoding (free, no API key required)
        const url = `https://api.postcodes.io/postcodes/${encodeURIComponent(postcode)}`;
        console.log("🌐 Request URL:", url);
        
        const response = await fetch(url);
        console.log("🌐 Postcodes.io response status:", response.status, response.statusText);
        
        if (!response.ok) {
          console.warn("⚠️ Postcode not found or invalid:", postcode, "Status:", response.status);
          locationError.textContent = "Postcode not found. Please enter a valid UK postcode.";
          return { lat: null, lng: null };
        }

        const data = await response.json();
        console.log("🌐 Postcodes.io data:", data);
        
        if (data.result) {
          console.log("✓ Postcode geocoded successfully:", {
            postcode: postcode,
            lat: data.result.latitude,
            lng: data.result.longitude,
          });
          return {
            lat: data.result.latitude,
            lng: data.result.longitude
          };
        } else {
          console.error("✗ No result in postcodes.io response:", data);
          locationError.textContent = "Postcode not found. Please enter a valid UK postcode.";
          return { lat: null, lng: null };
        }
      } catch (error) {
        console.error("✗ Geocoding error:", error);
        console.error("Error details:", error.message, error.stack);
        locationError.textContent = "Error validating postcode. Please try again.";
        return { lat: null, lng: null };
      }
    }

    // Form submission
    profileForm.addEventListener("submit", async (e) => {
      console.log("=== FORM SUBMIT START ===");
      console.log("Form submit event triggered");
      e.preventDefault();

      const username = usernameInput.value.trim();
      const postcode = locationInput.value.trim();
      const role = document.querySelector('input[name="role"]:checked')?.value || "";

      console.log("Form values collected:", {
        username: username,
        postcode: postcode,
        postcodeLength: postcode.length,
        role: role,
        barbershopId: selectedBarbershopId,
      });
      console.log("locationInput.value:", locationInput.value);
      console.log("locationInput DOM element:", locationInput);

      if (!validateForm(username, postcode, role)) {
        console.log("✗ Form validation failed");
        console.log("=== FORM SUBMIT END (VALIDATION FAILED) ===");
        return;
      }

      console.log("✓ Form validation passed");

      // Disable submit button during request
      submitBtn.disabled = true;
      submitBtn.textContent = "Saving…";

      try {
        // Geocode postcode if provided and get latitude/longitude coordinates
        let lat = null;
        let lng = null;

        if (postcode) {
          console.log("📍 Geocoding postcode:", postcode);
          const coords = await geocodePostcode(postcode);
          lat = coords.lat;
          lng = coords.lng;
          console.log("📍 Geocoding result:", { lat, lng });

          // If geocoding failed, don't proceed
          if (lat === null || lng === null) {
            console.log("✗ Geocoding failed, aborting submission");
            submitBtn.disabled = false;
            submitBtn.textContent = "Save changes";
            console.log("=== FORM SUBMIT END (GEOCODING FAILED) ===");
            return;
          }
          console.log("✓ Postcode geocoded successfully:", { postcode, lat, lng });
        } else {
          console.log("⚠️ No postcode provided, lat/lng will be null");
        }

        // Build payload with postcode and coordinates
        const payload = {
          username,
          location: postcode || null,
          role,
          lat,
          lng,
        };

        // Add barbershop_id for barbers
        if (role === "barber") {
          payload.barbershop_id = selectedBarbershopId;
        }

        console.log("📤 Payload to send:", payload);
        console.log("=== SENDING REQUEST TO /api/user/profile ===");

        const response = await fetch("/api/user/profile", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        console.log("📥 Response received:", {
          status: response.status,
          ok: response.ok,
          data: data,
        });

        if (!response.ok || !data.ok) {
          const errorMsg = data.error || "Failed to update profile";
          console.log("✗ Profile update failed:", errorMsg);
          generalError.textContent = errorMsg;
          submitBtn.disabled = false;
          submitBtn.textContent = "Save changes";
          console.log("=== FORM SUBMIT END (API ERROR) ===");
          return;
        }

        console.log("✓ Profile updated successfully");
        console.log("Saved data:", { postcode, lat, lng });
        generalError.textContent = "";
        generalError.textContent = "Profile saved successfully!";
        generalError.style.color = "#10b981"; // Green color for success

        // Reset button
        submitBtn.disabled = false;
        submitBtn.textContent = "Save changes";

        console.log("⏱️ Reloading page in 1500ms...");
        // Optional: reload page or update session after a delay
        setTimeout(() => {
          console.log("🔄 Reloading page...");
          window.location.reload();
        }, 1500);
      } catch (error) {
        console.error("✗ Profile update error:", error);
        console.error("Error stack:", error.stack);
        generalError.textContent = "Network error: " + error.message;
        submitBtn.disabled = false;
        submitBtn.textContent = "Save changes";
        console.log("=== FORM SUBMIT END (EXCEPTION) ===");
      }
    });

    // Initialize barbershop field visibility on page load
    console.log("📋 Profile form initialization complete");
    console.log("Final state:", {
      username: usernameInput.value,
      location: locationInput.value,
      role: document.querySelector('input[name="role"]:checked')?.value,
      locationElementFound: !!locationInput,
      locationInputValue: locationInput.value,
      locationInputPlaceholder: locationInput.placeholder,
    });
    updateBarbershopFieldVisibility();
    console.log("✓ profile.js fully initialized");
  }

  // Wait for DOM to be ready
  if (document.readyState === "loading") {
    console.log("⏳ DOM still loading, waiting for DOMContentLoaded event");
    document.addEventListener("DOMContentLoaded", initializeForm);
  } else {
    console.log("✓ DOM already loaded, initializing form immediately");
    initializeForm();
  }
  console.log("✓ profile.js setup complete");
} // End of if (!window.__profileJsLoaded) block
