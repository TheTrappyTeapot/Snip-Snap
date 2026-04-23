/* Script for /home/runner/work/Snip-Snap/Snip-Snap/app/static/js/components/editableUserPromo.js. */

function createEditableUserPromo(mountElement, userData = {}, config = {}) {
  const onChange = config.onChange || function() {};
  const avatarSize = config.avatarSize || 80;

  let currentUsername = userData.username || "Unknown";
  let currentProfileImageUrl = userData.profile_image_url || "";
  let selectedPhotoFile = null;

  // Create the structure
  const html = `
    <div class="editable-user-promo">
      <!-- Avatar Section -->
      <div class="editable-user-promo__avatar-wrapper">
        <div class="editable-user-promo__avatar" id="avatarDisplay" style="width: ${avatarSize}px; height: ${avatarSize}px;">
          ${currentProfileImageUrl ? 
            `<img src="${currentProfileImageUrl}" alt="Profile" />` :
            `<svg viewBox="0 0 24 24" width="${Math.floor(avatarSize * 0.6)}" height="${Math.floor(avatarSize * 0.6)}"><circle cx="12" cy="8" r="4" fill="currentColor"/><path d="M4 20a8 8 0 0 1 16 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`
          }
        </div>
        <div class="editable-user-promo__edit-overlay" id="editAvatarOverlay">
          <div class="editable-user-promo__edit-icon">✏️</div>
        </div>

        <!-- Photo Upload Popup (initially hidden) -->
        <div class="photo-upload-popup hidden" id="photoUploadPopup">
          <input type="file" class="photo-upload-input" accept="image/png,image/jpeg,image/webp">
          <div class="photo-upload-preview"></div>
          <div class="photo-upload-limit-message"></div>
        </div>
      </div>

      <!-- Info Section -->
      <div class="editable-user-promo__info">
        <div class="editable-user-promo__username">
          <span class="editable-user-promo__username-text" id="usernameDisplay">${escapeHtml(currentUsername)}</span>
          <span class="editable-user-promo__edit-hint">✏️</span>
        </div>
        <div class="editable-user-promo__subtext" id="subtextDisplay"></div>
      </div>
    </div>
  `;

  mountElement.innerHTML = html;

  // Get elements
  const avatarDisplay = mountElement.querySelector("#avatarDisplay");
  const editAvatarOverlay = mountElement.querySelector("#editAvatarOverlay");
  const photoUploadPopup = mountElement.querySelector("#photoUploadPopup");
  const photoUploadInput = photoUploadPopup.querySelector(".photo-upload-input");
  const photoPreview = photoUploadPopup.querySelector(".photo-upload-preview");
  const photoLimitMessage = photoUploadPopup.querySelector(".photo-upload-limit-message");
  const usernameDisplay = mountElement.querySelector("#usernameDisplay");
  const subtextDisplay = mountElement.querySelector("#subtextDisplay");

  // Helper function to escape HTML
  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Set subtext if it's a barber
  if (userData.role === "barber" && userData.barbershop_name) {
    subtextDisplay.textContent = userData.barbershop_name;
  }

  // ========== Photo Upload Handler ==========
  editAvatarOverlay.addEventListener("click", (e) => {
    e.stopPropagation();
    console.log("🖼️ Opening photo upload popup");
    photoUploadPopup.classList.remove("hidden");
    photoUploadInput.click();
  });

  photoUploadInput.addEventListener("change", async (event) => {
    const files = Array.from(event.target.files);
    
    if (files.length === 0) return;

    selectedPhotoFile = files[0];
    console.log("🖼️ Photo selected:", selectedPhotoFile.name);

    // Show preview
    photoPreview.innerHTML = "";
    const reader = new FileReader();
    reader.onload = function (e) {
      const wrapper = document.createElement("div");
      wrapper.className = "preview-wrapper";

      const img = document.createElement("img");
      img.src = e.target.result;
      img.className = "preview-image";

      const removeBtn = document.createElement("button");
      removeBtn.className = "remove-btn";
      removeBtn.innerHTML = "×";
      removeBtn.addEventListener("click", () => {
        selectedPhotoFile = null;
        photoPreview.innerHTML = "";
        photoUploadInput.value = "";
        console.log("🖼️ Photo removed");
      });

      wrapper.appendChild(img);
      wrapper.appendChild(removeBtn);
      photoPreview.appendChild(wrapper);

      // Show action buttons
      if (!photoPreview.nextElementSibling || !photoPreview.nextElementSibling.classList.contains("photo-upload-actions")) {
        const actions = document.createElement("div");
        actions.className = "photo-upload-actions";
        actions.style.cssText = "display: flex; gap: 8px; margin-top: 8px;";
        actions.innerHTML = `
          <button type="button" class="photo-upload-cancel-btn" style="flex: 1; padding: 8px; border-radius: 6px; border: 1px solid var(--profile-border); background: var(--profile-surface-2); color: var(--profile-text); cursor: pointer; font-weight: 500; font-size: 0.85rem;">Cancel</button>
          <button type="button" class="photo-upload-submit-btn" style="flex: 1; padding: 8px; border-radius: 6px; border: none; background: var(--profile-accent); color: white; cursor: pointer; font-weight: 500; font-size: 0.85rem;">Upload</button>
        `;
        photoUploadPopup.appendChild(actions);

        actions.querySelector(".photo-upload-cancel-btn").addEventListener("click", () => {
          selectedPhotoFile = null;
          photoPreview.innerHTML = "";
          photoUploadInput.value = "";
          photoUploadPopup.classList.add("hidden");
          actions.remove();
        });

        actions.querySelector(".photo-upload-submit-btn").addEventListener("click", async () => {
          await uploadProfilePhoto(selectedPhotoFile);
          actions.remove();
        });
      }
    };
    reader.readAsDataURL(selectedPhotoFile);
  });

  // Close popup when clicking outside
  document.addEventListener("click", (e) => {
    if (!mountElement.contains(e.target)) {
      photoUploadPopup.classList.add("hidden");
      const actions = photoUploadPopup.querySelector(".photo-upload-actions");
      if (actions) actions.remove();
      selectedPhotoFile = null;
      photoPreview.innerHTML = "";
      photoUploadInput.value = "";
    }
  });

  // ========== Photo Upload to Server ==========
  async function uploadProfilePhoto(file) {
    if (!file) return;

    console.log("🖼️ Uploading profile photo:", file.name);

    const formData = new FormData();
    formData.append("photo", file);

    try {
      const response = await fetch("/api/user/profile-photo", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("🖼️ Upload response:", data);

      if (!response.ok || !data.ok) {
        const errorMsg = data.error || "Failed to upload photo";
        console.error("✗ Photo upload failed:", errorMsg);
        alert("Error uploading photo: " + errorMsg);
        return;
      }

      // Update avatar display
      console.log("✓ Photo uploaded successfully");
      currentProfileImageUrl = data.image_url;
      avatarDisplay.innerHTML = `<img src="${currentProfileImageUrl}" alt="Profile" />`;

      // Close popup and reset
      photoUploadPopup.classList.add("hidden");
      const actions = photoUploadPopup.querySelector(".photo-upload-actions");
      if (actions) actions.remove();
      selectedPhotoFile = null;
      photoPreview.innerHTML = "";
      photoUploadInput.value = "";

      onChange({ profile_image_url: currentProfileImageUrl });
    } catch (error) {
      console.error("✗ Photo upload error:", error);
      alert("Error uploading photo: " + error.message);
    }
  }

  // ========== Username Edit Handler ==========
  let isEditingUsername = false;

  usernameDisplay.addEventListener("click", () => {
    if (isEditingUsername) return;
    
    console.log("📝 Editing username");
    isEditingUsername = true;

    const originalUsername = currentUsername;
    const input = document.createElement("input");
    input.className = "editable-user-promo__username-input";
    input.type = "text";
    input.value = originalUsername;
    input.maxLength = 50;

    const parentDiv = usernameDisplay.parentElement;
    parentDiv.replaceChild(input, usernameDisplay);

    input.focus();
    input.select();

    async function saveUsername() {
      const newUsername = input.value.trim();

      if (newUsername === originalUsername) {
        // No change, just revert
        console.log("📝 No username change");
        parentDiv.replaceChild(usernameDisplay, input);
        isEditingUsername = false;
        return;
      }

      if (!newUsername) {
        alert("Username cannot be empty");
        input.focus();
        return;
      }

      if (newUsername.length < 2) {
        alert("Username must be at least 2 characters");
        input.focus();
        return;
      }

      console.log("📝 Saving username:", newUsername);
      input.disabled = true;

      try {
        const response = await fetch("/api/user/profile", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: newUsername }),
        });

        const data = await response.json();
        console.log("📝 Update response:", data);

        if (!response.ok || !data.ok) {
          const errorMsg = data.error || "Failed to update username";
          console.error("✗ Username update failed:", errorMsg);
          alert("Error updating username: " + errorMsg);
          input.disabled = false;
          input.focus();
          return;
        }

        // Update display
        console.log("✓ Username updated successfully");
        currentUsername = newUsername;
        usernameDisplay.textContent = escapeHtml(newUsername);
        parentDiv.replaceChild(usernameDisplay, input);
        isEditingUsername = false;

        onChange({ username: currentUsername });
      } catch (error) {
        console.error("✗ Username update error:", error);
        alert("Error updating username: " + error.message);
        input.disabled = false;
        input.focus();
      }
    }

    input.addEventListener("blur", saveUsername);
    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        saveUsername();
      }
    });
    input.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        console.log("📝 Username edit cancelled");
        parentDiv.replaceChild(usernameDisplay, input);
        isEditingUsername = false;
      }
    });
  });

  return {
    update: function(newData) {
      if (newData.username) {
        currentUsername = newData.username;
        usernameDisplay.textContent = escapeHtml(currentUsername);
      }
      if (newData.profile_image_url) {
        currentProfileImageUrl = newData.profile_image_url;
        avatarDisplay.innerHTML = `<img src="${newData.profile_image_url}" alt="Profile" />`;
      }
      if (newData.barbershop_name) {
        subtextDisplay.textContent = newData.barbershop_name;
      }
    },
  };
}
