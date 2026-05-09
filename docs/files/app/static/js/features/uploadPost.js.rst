uploadPost.js - Photo Upload Feature
===================================

**Purpose**: Feature for uploading new gallery photos.

**What it does**:

- Manages photo upload form
- Handles file selection and validation
- Shows image preview
- Manages upload progress
- Compresses images before upload
- Handles errors and retries
- Manages captions and metadata
- Shows upload success/failure

**How to use**:

Initialize upload feature::

    const uploader = new UploadPostFeature('uploadContainer');
    uploader.onSuccess((postId) => {
        showSuccess('Photo uploaded!');
    });

**Key Functions**:

- ``UploadPostFeature(container)``: Initialize
- ``selectFile()``: Open file browser
- ``validateFile(file)``: Check file
- ``compressImage(file)``: Optimize image
- ``preview(file)``: Show preview
- ``upload(caption)``: Send to server
- ``cancel()``: Abort upload
- ``retry()``: Retry failed upload

**Validation**:

- File type (JPG, PNG, WebP)
- Max file size (10MB)
- Image dimensions (min 300x300px)
- Valid caption

**API Endpoint**:

``POST /api/upload-photo`` - Submit photo

**Features**:

- Drag-drop upload
- File browser selection
- Image preview
- Upload progress bar
- Caption input
- Error handling
- Retry functionality
- Success confirmation

The script in app/static/js/features/uploadPost.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It communicates with backend endpoints such as /api/discover/search_items and /api/photos/upload to fetch or persist data needed by the UI. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/features/uploadPost.js` provides frontend browser behavior. Function responsibilities: `resetForm` resets form; `showError` shows error; `showSuccess` shows success; `hideMessages` hides messages; `showLoading` shows loading.