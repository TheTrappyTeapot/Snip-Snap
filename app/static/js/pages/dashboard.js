// Modal management
const modal = document.getElementById('uploadModal');
const openBtn = document.getElementById('openUploadBtn');
const closeBtn = document.getElementById('closeUploadBtn');
const cancelBtn = document.getElementById('cancelUploadBtn');

// Tag management with autocomplete and tag list
let tagAutocomplete = null;
let tagList = null;

console.log('[MODAL DEBUG] Modal elements found:', {
  modal: !!modal,
  openBtn: !!openBtn,
  closeBtn: !!closeBtn,
  cancelBtn: !!cancelBtn
});

openBtn.addEventListener('click', () => {
  console.log('[MODAL DEBUG] Open button clicked');
  modal.classList.add('open');
  console.log('[MODAL DEBUG] Modal opened, loading tags');
  loadTags();
});

closeBtn.addEventListener('click', () => {
  console.log('[MODAL DEBUG] Close button clicked');
  modal.classList.remove('open');
  resetForm();
});

cancelBtn.addEventListener('click', () => {
  console.log('[MODAL DEBUG] Cancel button clicked');
  modal.classList.remove('open');
  resetForm();
});

modal.addEventListener('click', (e) => {
  if (e.target === modal) {
    console.log('[MODAL DEBUG] Clicked outside modal');
    modal.classList.remove('open');
    resetForm();
  }
});

// File input handling
const photoInput = document.getElementById('photoInput');
const preview = document.getElementById('preview');

photoInput.addEventListener('change', function() {
  preview.innerHTML = '';
  
  const file = this.files[0];
  console.log('[FILE_INPUT DEBUG] File selected:', {
    name: file.name,
    type: file.type,
    size: file.size,
    lastModified: file.lastModified
  });
  
  if (file && file.type.startsWith('image/')) {
    console.log('[FILE_INPUT DEBUG] File is a valid image type');
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
      removeBtn.onclick = (e) => {
        e.preventDefault();
        photoInput.value = '';
        preview.innerHTML = '';
        console.log('[FILE_INPUT DEBUG] File removed');
      };
      
      box.appendChild(img);
      box.appendChild(removeBtn);
      preview.appendChild(box);
      console.log('[FILE_INPUT DEBUG] Preview displayed');
    };
    reader.readAsDataURL(file);
  } else {
    console.warn('[FILE_INPUT DEBUG] Selected file is not a valid image type');
  }
});

// Load tags from API and initialize autocomplete + tag list
async function loadTags() {
  console.log('[LOAD_TAGS DEBUG] Starting to load tags');
  try {
    const response = await fetch('/api/discover/search_items');
    console.log('[LOAD_TAGS DEBUG] API response status:', response.status);
    const data = await response.json();
    console.log('[LOAD_TAGS DEBUG] API response data:', data);
    
    const tags = data.items.filter(item => item.type === 'tag');
    console.log('[LOAD_TAGS DEBUG] Filtered tags:', tags);
    
    // Initialize tag list (display of selected tags)
    if (!tagList) {
      tagList = new window.TagList({
        mountEl: document.getElementById('selectedTagsContainer'),
        initialItems: []
      });
      console.log('[LOAD_TAGS DEBUG] TagList initialized');
    }
    
    // Initialize autocomplete
    if (!tagAutocomplete) {
      tagAutocomplete = window.createSearchBarAutocomplete(
        document.getElementById('tagSearchContainer'),
        (selectedItem) => {
          console.log('[LOAD_TAGS DEBUG] Tag selected from autocomplete:', selectedItem);
          // Add to tag list
          tagList.add_item(selectedItem);
        },
        tags,
        { placeholder: 'Search and select tags...' }
      );
      console.log('[LOAD_TAGS DEBUG] Search autocomplete initialized with', tags.length, 'tags');
    } else {
      // Update existing autocomplete with new items
      tagAutocomplete.setItems(tags);
      console.log('[LOAD_TAGS DEBUG] Search autocomplete updated with', tags.length, 'tags');
    }
    
    console.log('[LOAD_TAGS DEBUG] Tags loaded successfully');
  } catch (error) {
    console.error('[LOAD_TAGS DEBUG] Error loading tags:', error);
    showError('Failed to load tags');
  }
}

// Form submission
const uploadForm = document.getElementById('uploadForm');
uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  console.log('[FORM_SUBMIT DEBUG] Form submission started');
  
  // Validate photo
  const photoInput = document.getElementById('photoInput');
  if (!photoInput.files.length) {
    console.warn('[FORM_SUBMIT DEBUG] No file selected');
    showError('Please select a photo');
    return;
  }
  
  const file = photoInput.files[0];
  console.log('[FORM_SUBMIT DEBUG] Selected file:', {
    name: file.name,
    type: file.type,
    size: file.size
  });
  
  // Validate tags
  const selectedTags = tagList ? tagList.get_items() : [];
  console.log('[FORM_SUBMIT DEBUG] Selected tags:', selectedTags.length, selectedTags);
  
  if (!selectedTags.length) {
    console.warn('[FORM_SUBMIT DEBUG] No tags selected');
    showError('Please select at least one tag');
    return;
  }
  
  // Get image dimensions
  const img = new Image();
  img.onload = () => {
    console.log('[FORM_SUBMIT DEBUG] Image loaded, dimensions:', {width: img.width, height: img.height});
    submitUpload(file, selectedTags.map(t => t.id), img.width, img.height);
  };
  img.onerror = () => {
    console.error('[FORM_SUBMIT DEBUG] Failed to load image');
    showError('Invalid image file');
  };
  img.src = URL.createObjectURL(file);
  console.log('[FORM_SUBMIT DEBUG] Image loading started');
});

async function submitUpload(file, tagIds, width, height) {
  try {
    showLoading(true);
    hideMessages();
    
    console.log('[UPLOAD DEBUG] File details:', {
      name: file.name,
      type: file.type,
      size: file.size,
      lastModified: file.lastModified
    });
    
    console.log('[UPLOAD DEBUG] Image dimensions:', { width, height });
    console.log('[UPLOAD DEBUG] Tag IDs:', tagIds);
    
    const formData = new FormData();
    formData.append('photo', file);
    formData.append('width', width);
    formData.append('height', height);
    formData.append('tag_ids', tagIds.join(','));
    
    // Debug: Log FormData contents
    console.log('[UPLOAD DEBUG] FormData contents:');
    for (let pair of formData.entries()) {
      if (pair[0] === 'photo') {
        console.log(`  ${pair[0]}: [File] name="${pair[1].name}", type="${pair[1].type}", size=${pair[1].size}`);
      } else {
        console.log(`  ${pair[0]}: ${pair[1]}`);
      }
    }
    
    console.log('[UPLOAD DEBUG] Sending POST request to /api/photos/upload');
    const response = await fetch('/api/photos/upload', {
      method: 'POST',
      body: formData
    });
    
    console.log('[UPLOAD DEBUG] Response status:', response.status);
    console.log('[UPLOAD DEBUG] Response headers:', {
      contentType: response.headers.get('content-type'),
      contentLength: response.headers.get('content-length')
    });
    
    const data = await response.json();
    console.log('[UPLOAD DEBUG] Response data:', data);
    
    if (!response.ok) {
      console.error('[UPLOAD DEBUG] Upload failed with status', response.status, ':', data);
      showError(data.error || 'Upload failed');
      return;
    }
    
    console.log('[UPLOAD DEBUG] Upload successful!', {
      photoId: data.photo_id,
      storagePath: data.storage_path
    });
    
    showSuccess('Photo uploaded successfully!');
    resetForm();
    
    // Close modal after 2 seconds
    setTimeout(() => {
      modal.classList.remove('open');
    }, 2000);
    
  } catch (error) {
    console.error('[UPLOAD DEBUG] Upload error:', error);
    console.error('[UPLOAD DEBUG] Error stack:', error.stack);
    showError('An error occurred during upload');
  } finally {
    showLoading(false);
  }
}

function showError(message) {
  const errorEl = document.getElementById('errorMessage');
  errorEl.textContent = message;
  errorEl.classList.add('show');
}

function showSuccess(message) {
  const successEl = document.getElementById('successMessage');
  successEl.textContent = message;
  successEl.classList.add('show');
}

function hideMessages() {
  document.getElementById('errorMessage').classList.remove('show');
  document.getElementById('successMessage').classList.remove('show');
}

function showLoading(show) {
  const loading = document.getElementById('loading');
  if (show) {
    loading.classList.add('show');
  } else {
    loading.classList.remove('show');
  }
}

function resetForm() {
  uploadForm.reset();
  preview.innerHTML = '';
  hideMessages();
  showLoading(false);
  
  // Clear tag list and search
  if (tagList) {
    tagList.set_items([]);
  }
  if (tagAutocomplete) {
    // Clear the search input
    const searchInput = document.querySelector('.sa-input');
    if (searchInput) {
      searchInput.value = '';
    }
  }
}
