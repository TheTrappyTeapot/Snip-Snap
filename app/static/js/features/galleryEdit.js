// Gallery Edit Feature

let galleryEdits = new Map(); // photo_id -> { main_tag_id }
let currentEditingPhoto = null;
let editPhotoTagAutocomplete = null;
let editPhotoTagSelection = null;
let editPhotoNewFile = null;
let editPhotoTagListComponent = null;

// Add gallery photo feature
let addGalleryPhotoTag = null;
let addGalleryPhotoTagAutocomplete = null;
let addGalleryPhotoTagListComponent = null;

export function initGalleryEditFeature() {
  console.log('[GALLERY EDIT] Starting feature initialization');
  
  const editPhotoModal = document.getElementById('editPhotoModal');
  const closeEditPhotoBtn = document.getElementById('closeEditPhotoBtn');
  const cancelEditPhotoBtn = document.getElementById('cancelEditPhotoBtn');
  const editPhotoForm = document.getElementById('editPhotoForm');

  console.log('[GALLERY EDIT] Elements found:', {
    editPhotoModal: !!editPhotoModal,
    closeEditPhotoBtn: !!closeEditPhotoBtn,
    cancelEditPhotoBtn: !!cancelEditPhotoBtn,
    editPhotoForm: !!editPhotoForm
  });

  if (!editPhotoModal || !editPhotoForm) {
    console.error('[GALLERY EDIT] Required elements not found');
    return;
  }

  console.log('[GALLERY EDIT] Initializing gallery edit feature');

  // Close/Cancel buttons
  closeEditPhotoBtn.addEventListener('click', () => {
    console.log('[GALLERY EDIT] Close button clicked');
    editPhotoModal.classList.remove('open');
    resetEditPhotoForm();
  });

  cancelEditPhotoBtn.addEventListener('click', () => {
    console.log('[GALLERY EDIT] Cancel button clicked');
    editPhotoModal.classList.remove('open');
    resetEditPhotoForm();
  });

  // Click outside modal
  editPhotoModal.addEventListener('click', (e) => {
    if (e.target === editPhotoModal) {
      console.log('[GALLERY EDIT] Clicked outside modal');
      editPhotoModal.classList.remove('open');
      resetEditPhotoForm();
    }
  });

  // Form submission
  editPhotoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('[GALLERY EDIT] Form submitted');
    
    if (!currentEditingPhoto) {
      showEditPhotoError('No photo selected');
      return;
    }

    if (!editPhotoTagSelection) {
      showEditPhotoError('Please select a main tag');
      return;
    }

    try {
      showEditPhotoLoading(true);
      hideEditPhotoMessages();
      
      // Check if user selected a new photo
      const photoInput = document.getElementById('editPhotoInput');
      if (photoInput && photoInput.files.length > 0) {
        editPhotoNewFile = photoInput.files[0];
      }
      
      // If user selected a new photo, upload it first
      if (editPhotoNewFile) {
        console.log('[GALLERY EDIT] New photo file selected, uploading...');
        
        const img = new Image();
        img.onload = async () => {
          const formData = new FormData();
          formData.append('photo', editPhotoNewFile);
          formData.append('width', img.width);
          formData.append('height', img.height);
          formData.append('photo_id', currentEditingPhoto.photo_id);
          
          const uploadResponse = await fetch('/api/photos/replace', {
            method: 'POST',
            body: formData
          });
          
          const uploadData = await uploadResponse.json();
          
          if (!uploadResponse.ok) {
            showEditPhotoError(uploadData.error || 'Failed to upload new photo');
            showEditPhotoLoading(false);
            return;
          }
          
          console.log('[GALLERY EDIT] Photo uploaded successfully');
          await updatePhotoMainTag();
        };
        
        img.onerror = () => {
          showEditPhotoError('Invalid image file');
          showEditPhotoLoading(false);
        };
        
        img.src = URL.createObjectURL(editPhotoNewFile);
      } else {
        // Just update the main tag
        await updatePhotoMainTag();
      }
      
    } catch (error) {
      console.error('[GALLERY EDIT] Error:', error);
      showEditPhotoError('An error occurred');
      showEditPhotoLoading(false);
    }
  });

  // Initialize add gallery photo form
  initAddGalleryPhotoForm();

  // Load gallery on page load
  console.log('[GALLERY EDIT] Calling loadEditableGallery');
  loadEditableGallery();
  
  console.log('[GALLERY EDIT] Feature initialization complete');
}

function initAddGalleryPhotoForm() {
  console.log('[GALLERY EDIT] Initializing add gallery photo form');
  
  const addGalleryPhotoModal = document.getElementById('addGalleryPhotoModal');
  const closeAddGalleryPhotoBtn = document.getElementById('closeAddGalleryPhotoBtn');
  const cancelAddGalleryPhotoBtn = document.getElementById('cancelAddGalleryPhotoBtn');
  const addGalleryPhotoForm = document.getElementById('addGalleryPhotoForm');
  const photoInput = document.getElementById('addGalleryPhotoInput');
  const preview = document.getElementById('addGalleryPhotoPreview');

  if (!addGalleryPhotoModal || !addGalleryPhotoForm) {
    console.error('[GALLERY EDIT] Add gallery photo elements not found');
    return;
  }

  // Close/Cancel buttons
  closeAddGalleryPhotoBtn.addEventListener('click', () => {
    console.log('[GALLERY EDIT] Close add gallery photo button clicked');
    addGalleryPhotoModal.classList.remove('open');
    resetAddGalleryPhotoForm();
  });

  cancelAddGalleryPhotoBtn.addEventListener('click', () => {
    console.log('[GALLERY EDIT] Cancel add gallery photo button clicked');
    addGalleryPhotoModal.classList.remove('open');
    resetAddGalleryPhotoForm();
  });

  // Click outside modal
  addGalleryPhotoModal.addEventListener('click', (e) => {
    if (e.target === addGalleryPhotoModal) {
      console.log('[GALLERY EDIT] Clicked outside add gallery photo modal');
      addGalleryPhotoModal.classList.remove('open');
      resetAddGalleryPhotoForm();
    }
  });

  // File input handling
  photoInput.addEventListener('change', function() {
    preview.innerHTML = '';
    
    const file = this.files[0];
    console.log('[GALLERY EDIT] File selected:', {
      name: file?.name,
      type: file?.type,
      size: file?.size
    });
    
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const box = document.createElement('div');
        box.className = 'image-box';
        
        const img = document.createElement('img');
        img.src = e.target.result;
        
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'remove-btn';
        removeBtn.innerHTML = '×';
        removeBtn.onclick = (evt) => {
          evt.preventDefault();
          photoInput.value = '';
          preview.innerHTML = '';
        };
        
        box.appendChild(img);
        box.appendChild(removeBtn);
        preview.appendChild(box);
      };
      reader.readAsDataURL(file);
    }
  });

  // Form submission
  addGalleryPhotoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('[GALLERY EDIT] Add gallery photo form submission started');
    
    if (!photoInput.files.length) {
      showAddGalleryPhotoError('Please select a photo');
      return;
    }
    
    const file = photoInput.files[0];
    
    if (!addGalleryPhotoTag) {
      showAddGalleryPhotoError('Please select a tag');
      return;
    }
    
    // Get image dimensions
    const img = new Image();
    img.onload = () => {
      submitAddGalleryPhoto(file, addGalleryPhotoTag.id, img.width, img.height);
    };
    img.onerror = () => {
      showAddGalleryPhotoError('Invalid image file');
    };
    img.src = URL.createObjectURL(file);
  });

  console.log('[GALLERY EDIT] Add gallery photo form initialization complete');
}

async function submitAddGalleryPhoto(file, tagId, width, height) {
  try {
    showAddGalleryPhotoLoading(true);
    hideAddGalleryPhotoMessages();
    
    const formData = new FormData();
    formData.append('photo', file);
    formData.append('width', width);
    formData.append('height', height);
    formData.append('tag_ids', tagId);
    formData.append('is_post', 'false');
    
    const response = await fetch('/api/photos/upload', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      showAddGalleryPhotoError(data.error || 'Upload failed');
      return;
    }
    
    showAddGalleryPhotoSuccess('Photo added to gallery successfully!');
    resetAddGalleryPhotoForm();
    
    const modal = document.getElementById('addGalleryPhotoModal');
    setTimeout(() => {
      modal.classList.remove('open');
      loadEditableGallery();
    }, 1500);
    
  } catch (error) {
    console.error('[GALLERY EDIT] Add gallery photo error:', error);
    showAddGalleryPhotoError('An error occurred during upload');
  } finally {
    showAddGalleryPhotoLoading(false);
  }
}

export async function loadEditableGallery() {
  console.log('[GALLERY EDIT] Loading editable gallery');
  const mountEl = document.getElementById('editable-gallery-mount');
  const loadingEl = document.getElementById('galleryLoading');
  
  if (!mountEl) {
    console.error('[GALLERY EDIT] Mount element not found!');
    return;
  }
  
  console.log('[GALLERY EDIT] Mount element found:', mountEl);
  
  try {
    // Show loading indicator
    if (loadingEl) {
      loadingEl.classList.add('show');
    }
    mountEl.innerHTML = '';
    
    console.log('[GALLERY EDIT] Fetching photos from /api/my-photos');
    const response = await fetch('/api/my-photos');
    console.log('[GALLERY EDIT] Response status:', response.status);
    
    if (!response.ok) {
      console.warn('[GALLERY EDIT] Failed to fetch photos:', response.status);
      mountEl.innerHTML = "<p>No gallery photos yet</p>";
      if (loadingEl) loadingEl.classList.remove('show');
      return;
    }

    const photos = await response.json();
    console.log('[GALLERY EDIT] Loaded', photos.length, 'photos:', photos);

    if (!photos || photos.length === 0) {
      console.log('[GALLERY EDIT] No photos returned');
      const emptyContainer = document.createElement('div');
      emptyContainer.className = 'gallery-empty-state';
      
      const message = document.createElement('p');
      message.textContent = 'No gallery photos yet. Upload a photo to add it to your gallery!';
      
      const addButton = document.createElement('button');
      addButton.type = 'button';
      addButton.className = 'btn btn-primary add-photos-btn';
      addButton.textContent = 'Add Photo';
      addButton.addEventListener('click', () => {
        loadAddGalleryPhotoTags();
        document.getElementById('addGalleryPhotoModal').classList.add('open');
      });
      
      emptyContainer.appendChild(message);
      emptyContainer.appendChild(addButton);
      mountEl.innerHTML = '';
      mountEl.appendChild(emptyContainer);
      
      if (loadingEl) loadingEl.classList.remove('show');
      return;
    }

    console.log('[GALLERY EDIT] Importing gallery components');
    // Render gallery grid  
    const { renderGalleryGrid } = await import('../components/galleryGrid.js');
    const { renderEditableGalleryCard } = await import('../components/editableGalleryCard.js');
    
    console.log('[GALLERY EDIT] Components imported, rendering gallery');

    // Create container for gallery and button
    const galleryContainer = document.createElement('div');
    galleryContainer.className = 'gallery-with-action';
    
    const gridContainer = document.createElement('div');
    galleryContainer.appendChild(gridContainer);

    renderGalleryGrid({
      mountEl: gridContainer,
      items: photos,
      columns: 3,
      renderItem: (photo) => renderEditableGalleryCard(photo, openEditPhotoModal)
    });
    
    // Show "Add More Photos" button if fewer than 8 photos
    if (photos.length < 8) {
      console.log('[GALLERY EDIT] Fewer than 8 photos, showing add more button');
      const buttonContainer = document.createElement('div');
      buttonContainer.className = 'gallery-action-container';
      
      const addMoreButton = document.createElement('button');
      addMoreButton.type = 'button';
      addMoreButton.className = 'btn btn-primary add-photos-btn';
      addMoreButton.textContent = `Add More Photos (${photos.length}/8)`;
      addMoreButton.addEventListener('click', () => {
        loadAddGalleryPhotoTags();
        document.getElementById('addGalleryPhotoModal').classList.add('open');
      });
      
      buttonContainer.appendChild(addMoreButton);
      galleryContainer.appendChild(buttonContainer);
    }
    
    mountEl.innerHTML = '';
    mountEl.appendChild(galleryContainer);
    
    // Hide loading indicator
    if (loadingEl) loadingEl.classList.remove('show');
    
    console.log('[GALLERY EDIT] Gallery rendered successfully');
  } catch (error) {
    console.error('[GALLERY EDIT] Error loading gallery:', error);
    console.error('[GALLERY EDIT] Stack:', error.stack);
    mountEl.innerHTML = "<p>Error loading photos</p>";
    if (loadingEl) loadingEl.classList.remove('show');
  }
}

export function openEditPhotoModal(photo) {
  console.log('[GALLERY EDIT] Opening modal for photo:', photo.photo_id);
  currentEditingPhoto = photo;
  editPhotoTagSelection = null;
  editPhotoNewFile = null;

  // Show current photo preview
  const previewEl = document.getElementById('editPhotoPreview');
  previewEl.innerHTML = `<img src="${photo.image_url}" style="max-width: 100%; max-height: 300px; border-radius: 8px;">`;

  // Set up file input for changing the photo
  const photoInput = document.getElementById('editPhotoInput');
  const previewNewEl = document.getElementById('editPhotoPreviewNew');
  
  if (photoInput) {
    photoInput.value = ''; // Clear any previous selection
    previewNewEl.innerHTML = ''; // Clear preview
    
    // File input change handler
    photoInput.onchange = function() {
      const file = this.files[0];
      console.log('[GALLERY EDIT] New file selected:', file?.name);
      
      previewNewEl.innerHTML = '';
      
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
          const box = document.createElement('div');
          box.className = 'image-box';
          
          const img = document.createElement('img');
          img.src = e.target.result;
          
          const removeBtn = document.createElement('button');
          removeBtn.type = 'button';
          removeBtn.className = 'remove-btn';
          removeBtn.innerHTML = '×';
          removeBtn.onclick = (evt) => {
            evt.preventDefault();
            photoInput.value = '';
            previewNewEl.innerHTML = '';
            editPhotoNewFile = null;
          };
          
          box.appendChild(img);
          box.appendChild(removeBtn);
          previewNewEl.appendChild(box);
        };
        reader.readAsDataURL(file);
        editPhotoNewFile = file;
      }
    };
  } else {
    console.error('[GALLERY EDIT] editPhotoInput element not found');
  }

  // Load tags and initialize autocomplete
  loadEditPhotoTags();

  // Show modal
  const editPhotoModal = document.getElementById('editPhotoModal');
  editPhotoModal.classList.add('open');
}

async function loadEditPhotoTags() {
  try {
    const response = await fetch('/api/discover/search_items');
    const data = await response.json();
    const tags = data.items.filter(item => item.type === 'tag');
    
    console.log('[GALLERY EDIT] Loaded', tags.length, 'tags');

    const tagSearchContainer = document.getElementById('editPhotoTagSearchContainer');
    const selectedTagContainer = document.getElementById('editPhotoSelectedTag');
    
    tagSearchContainer.innerHTML = '';
    selectedTagContainer.innerHTML = '';

    // Initialize TagList
    if (!editPhotoTagListComponent) {
      editPhotoTagListComponent = new window.TagList({
        mountEl: selectedTagContainer,
        initialItems: []
      });
    }
    
    // Create autocomplete
    editPhotoTagAutocomplete = window.createSearchBarAutocomplete(
      tagSearchContainer,
      (selectedItem) => {
        console.log('[GALLERY EDIT] Tag selected:', selectedItem);
        editPhotoTagSelection = selectedItem;
        editPhotoTagListComponent.set_items([selectedItem]);
      },
      tags,
      { placeholder: 'Search and select main tag...' }
    );
  } catch (error) {
    console.error('[GALLERY EDIT] Error loading tags:', error);
  }
}

async function updatePhotoMainTag() {
  console.log('[GALLERY EDIT] Updating main tag');
  
  const response = await fetch(`/api/photos/${currentEditingPhoto.photo_id}/update-tag`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      main_tag_id: editPhotoTagSelection.id
    })
  });

  const data = await response.json();
  
  if (!response.ok) {
    showEditPhotoError(data.error || 'Failed to save');
    showEditPhotoLoading(false);
    return;
  }

  console.log('[GALLERY EDIT] Successfully saved');
  
  // Track the edit
  galleryEdits.set(currentEditingPhoto.photo_id, {
    main_tag_id: editPhotoTagSelection.id
  });

  showEditPhotoSuccess('Photo updated successfully!');
  
  showEditPhotoLoading(false);
  
  setTimeout(() => {
    const editPhotoModal = document.getElementById('editPhotoModal');
    editPhotoModal.classList.remove('open');
    resetEditPhotoForm();
    loadEditableGallery();
  }, 1500);
}

function resetEditPhotoForm() {
  currentEditingPhoto = null;
  editPhotoTagSelection = null;
  editPhotoNewFile = null;
  
  document.getElementById('editPhotoPreview').innerHTML = '';
  document.getElementById('editPhotoPreviewNew').innerHTML = '';
  document.getElementById('editPhotoTagSearchContainer').innerHTML = '';
  
  const photoInput = document.getElementById('editPhotoInput');
  if (photoInput) {
    photoInput.value = '';
  }
  
  if (editPhotoTagListComponent) {
    editPhotoTagListComponent.set_items([]);
  }
  
  document.getElementById('editPhotoErrorMessage').classList.remove('show');
  document.getElementById('editPhotoSuccessMessage').classList.remove('show');
}

function showEditPhotoError(message) {
  const errorEl = document.getElementById('editPhotoErrorMessage');
  errorEl.textContent = message;
  errorEl.classList.add('show');
}

function showEditPhotoSuccess(message) {
  const successEl = document.getElementById('editPhotoSuccessMessage');
  successEl.textContent = message;
  successEl.classList.add('show');
}

function hideEditPhotoMessages() {
  document.getElementById('editPhotoErrorMessage').classList.remove('show');
  document.getElementById('editPhotoSuccessMessage').classList.remove('show');
}

function showEditPhotoLoading(show) {
  const loading = document.getElementById('editPhotoLoading');
  if (show) {
    loading.classList.add('show');
  } else {
    loading.classList.remove('show');
  }
}

// Helper functions for add gallery photo
async function loadAddGalleryPhotoTags() {
  try {
    const response = await fetch('/api/discover/search_items');
    const data = await response.json();
    const tags = data.items.filter(item => item.type === 'tag');
    
    console.log('[GALLERY EDIT] Loaded', tags.length, 'tags for add gallery photo');

    const tagSearchContainer = document.getElementById('addGalleryPhotoTagSearchContainer');
    const selectedTagContainer = document.getElementById('addGalleryPhotoSelectedTag');
    
    tagSearchContainer.innerHTML = '';
    selectedTagContainer.innerHTML = '';

    // Initialize TagList
    if (!addGalleryPhotoTagListComponent) {
      addGalleryPhotoTagListComponent = new window.TagList({
        mountEl: selectedTagContainer,
        initialItems: []
      });
    }
    
    // Create autocomplete
    addGalleryPhotoTagAutocomplete = window.createSearchBarAutocomplete(
      tagSearchContainer,
      (selectedItem) => {
        console.log('[GALLERY EDIT] Add gallery photo tag selected:', selectedItem);
        addGalleryPhotoTag = selectedItem;
        addGalleryPhotoTagListComponent.set_items([selectedItem]);
      },
      tags,
      { placeholder: 'Search and select tag...' }
    );
  } catch (error) {
    console.error('[GALLERY EDIT] Error loading tags for add gallery photo:', error);
  }
}

function resetAddGalleryPhotoForm() {
  addGalleryPhotoTag = null;
  
  document.getElementById('addGalleryPhotoInput').value = '';
  document.getElementById('addGalleryPhotoPreview').innerHTML = '';
  document.getElementById('addGalleryPhotoTagSearchContainer').innerHTML = '';
  
  if (addGalleryPhotoTagListComponent) {
    addGalleryPhotoTagListComponent.set_items([]);
  }
  
  document.getElementById('addGalleryPhotoErrorMessage').classList.remove('show');
  document.getElementById('addGalleryPhotoSuccessMessage').classList.remove('show');
}

function showAddGalleryPhotoError(message) {
  const errorEl = document.getElementById('addGalleryPhotoErrorMessage');
  errorEl.textContent = message;
  errorEl.classList.add('show');
}

function showAddGalleryPhotoSuccess(message) {
  const successEl = document.getElementById('addGalleryPhotoSuccessMessage');
  successEl.textContent = message;
  successEl.classList.add('show');
}

function hideAddGalleryPhotoMessages() {
  document.getElementById('addGalleryPhotoErrorMessage').classList.remove('show');
  document.getElementById('addGalleryPhotoSuccessMessage').classList.remove('show');
}

function showAddGalleryPhotoLoading(show) {
  const loading = document.getElementById('addGalleryPhotoLoading');
  if (show) {
    loading.classList.add('show');
  } else {
    loading.classList.remove('show');
  }
}
