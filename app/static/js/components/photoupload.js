console.log('[PHOTO UPLOAD] photoupload.js loaded');

function createPhotoUploadComponent(mountElement, config = {}) {

    const maxPhotos = config.maxPhotos || 2;
    const onChange = config.onChange || function() {};

    let selectedFiles = [];

    // Create structure inside mount
    const html = `
        <div class="photo-upload">
            <button type="button" class="photo-upload-btn">Upload photo</button>

            <div class="photo-upload-popup hidden">
                <input type="file" class="photo-upload-input" accept="image/*" ${maxPhotos > 1 ? "multiple" : ""}>
                <div class="photo-upload-preview"></div>
                <div class="photo-upload-limit-message"></div>
            </div>
        </div>
    `;
    
    console.log('[PHOTO UPLOAD] Mount element:', mountElement);
    console.log('[PHOTO UPLOAD] Mount element innerHTML before:', mountElement.innerHTML);
    
    mountElement.innerHTML = html;
    
    console.log('[PHOTO UPLOAD] Component created, html:', html);
    console.log('[PHOTO UPLOAD] Mount element innerHTML after:', mountElement.innerHTML);

    const button = mountElement.querySelector(".photo-upload-btn");
    const popup = mountElement.querySelector(".photo-upload-popup");
    const input = mountElement.querySelector(".photo-upload-input");
    const preview = mountElement.querySelector(".photo-upload-preview");
    const limitMessage = mountElement.querySelector(".photo-upload-limit-message");

    console.log('[PHOTO UPLOAD] Elements found:', {button: !!button, popup: !!popup, input: !!input});
    if (button) {
      console.log('[PHOTO UPLOAD] Button found! innerHTML:', button.innerHTML);
    } else {
      console.error('[PHOTO UPLOAD] Button NOT found after innerHTML assignment!');
      console.error('[PHOTO UPLOAD] Mount element children:', Array.from(mountElement.children).map(c => c.outerHTML));
    }

    if (!button || !popup || !input || !preview || !limitMessage) {
      console.error('[PHOTO UPLOAD] Missing required elements, aborting component initialization');
      return { getFiles: () => [], clearFiles: () => {} };
    }

    button.addEventListener("click", (e) => {
        e.preventDefault();
        console.log('[PHOTO UPLOAD] Upload button clicked');
        button.style.display = "none";
        popup.classList.remove("hidden");
    });

    input.addEventListener("change", (event) => {
        let files = Array.from(event.target.files);

        if (selectedFiles.length + files.length > maxPhotos) {
            files = files.slice(0, maxPhotos - selectedFiles.length);
        }

        selectedFiles = selectedFiles.concat(files);

        renderPreview();
        onChange(selectedFiles);

        if (selectedFiles.length >= maxPhotos) {
            input.disabled = true;
            limitMessage.textContent = "Maximum number of photos reached.";
        }
    });

    function renderPreview() {
    preview.innerHTML = "";

    selectedFiles.forEach((file, index) => {

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

            removeBtn.addEventListener("click", function () {
                selectedFiles.splice(index, 1);
                input.disabled = false;
                limitMessage.textContent = "";
                renderPreview();
                onChange(selectedFiles);
            });

            wrapper.appendChild(img);
            wrapper.appendChild(removeBtn);
            preview.appendChild(wrapper);
        };

        reader.readAsDataURL(file);
    }
    }

    return {
        getFiles: function() { return selectedFiles; },
        clearFiles: function() { selectedFiles = []; renderPreview(); input.disabled = false; limitMessage.textContent = ""; }
    };
}

console.log('[PHOTO UPLOAD] About to expose createPhotoUploadComponent on window');
// Explicitly expose on window to ensure it's available globally
window.createPhotoUploadComponent = createPhotoUploadComponent;
console.log('[PHOTO UPLOAD] Successfully exposed createPhotoUploadComponent:', typeof window.createPhotoUploadComponent);