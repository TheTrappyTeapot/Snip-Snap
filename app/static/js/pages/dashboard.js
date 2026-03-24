// Modal management
const modal = document.getElementById('uploadModal');
const openBtn = document.getElementById('openUploadBtn');
const closeBtn = document.getElementById('closeUploadBtn');
const cancelBtn = document.getElementById('cancelUploadBtn');

openBtn.addEventListener('click', () => {
  modal.classList.add('open');
  loadTags();
});

closeBtn.addEventListener('click', () => {
  modal.classList.remove('open');
  resetForm();
});

cancelBtn.addEventListener('click', () => {
  modal.classList.remove('open');
  resetForm();
});

modal.addEventListener('click', (e) => {
  if (e.target === modal) {
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
      removeBtn.onclick = (e) => {
        e.preventDefault();
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

// Load tags from API
async function loadTags() {
  try {
    const response = await fetch('/api/discover/search_items');
    const data = await response.json();
    const tags = data.items.filter(item => item.type === 'tag');
    
    const tagSelector = document.getElementById('tagSelector');
    tagSelector.innerHTML = '';
    
    tags.forEach(tag => {
      const tagItem = document.createElement('div');
      tagItem.className = 'tag-item';
      tagItem.innerHTML = `
        <input type="checkbox" id="tag-${tag.id}" value="${tag.id}" class="tag-checkbox">
        <label for="tag-${tag.id}">${tag.label}</label>
      `;
      tagSelector.appendChild(tagItem);
    });
  } catch (error) {
    console.error('Error loading tags:', error);
    showError('Failed to load tags');
  }
}

// Form submission
const uploadForm = document.getElementById('uploadForm');
uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  // Validate photo
  const photoInput = document.getElementById('photoInput');
  if (!photoInput.files.length) {
    showError('Please select a photo');
    return;
  }
  
  const file = photoInput.files[0];
  
  // Validate tags
  const selectedTags = Array.from(document.querySelectorAll('.tag-checkbox:checked'));
  if (!selectedTags.length) {
    showError('Please select at least one tag');
    return;
  }
  
  // Get image dimensions
  const img = new Image();
  img.onload = () => {
    submitUpload(file, selectedTags.map(t => t.value), img.width, img.height);
  };
  img.onerror = () => {
    showError('Invalid image file');
  };
  img.src = URL.createObjectURL(file);
});

async function submitUpload(file, tagIds, width, height) {
  try {
    showLoading(true);
    hideMessages();
    
    const formData = new FormData();
    formData.append('photo', file);
    formData.append('width', width);
    formData.append('height', height);
    formData.append('tag_ids', tagIds.join(','));
    
    const response = await fetch('/api/photos/upload', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      showError(data.error || 'Upload failed');
      return;
    }
    
    showSuccess('Photo uploaded successfully!');
    resetForm();
    
    // Close modal after 2 seconds
    setTimeout(() => {
      modal.classList.remove('open');
    }, 2000);
    
  } catch (error) {
    console.error('Upload error:', error);
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
  document.querySelectorAll('.tag-checkbox').forEach(el => el.checked = false);
}
