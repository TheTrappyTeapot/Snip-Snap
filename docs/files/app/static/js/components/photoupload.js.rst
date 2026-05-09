photoupload.js - Photo Upload Component Script
==============================================

**Purpose**: JavaScript for handling image file uploads and previews.

**What it does**:

- Manages drag-and-drop file uploads
- Displays image preview before upload
- Sends images to server/storage
- Shows upload progress
- Handles upload errors
- Validates file types and sizes
- Compresses images before upload

**How to use**:

Include in HTML::

    <script src="{{ url_for('static', filename='js/components/photoupload.js') }}"></script>

Initialize upload handler::

    <div class="photo-upload" id="uploadWidget"></div>
    <script>
        const uploader = new PhotoUpload('uploadWidget', {
            maxSize: 5242880,  // 5MB
            allowedTypes: ['image/jpeg', 'image/png'],
            uploadEndpoint: '/api/upload-photo'
        });
    </script>

**Key Functions**:

- ``PhotoUpload(container, options)``: Initialize uploader
- ``handleDrop(event)``: Handle drag-and-drop
- ``selectFile()``: Open file browser
- ``previewImage(file)``: Display image preview
- ``uploadImage(file)``: Send to server
- ``setProgress(percent)``: Update progress bar

**API Endpoint**:

``POST /api/upload-photo`` - Upload image to storage

**Features**:

- Drag and drop support
- File validation (type and size)
- Image compression
- Progress tracking
- Error handling and messages
- Multiple file support
- Preview before upload

The script in app/static/js/components/photoupload.js binds event listeners, updates DOM state, and keeps the related UI view interactive. It focuses on local client behavior, validation, rendering, and state transitions for the associated page or component. It is loaded by the corresponding template and works with neighboring component/feature scripts in app/static/js.

Purpose
-------

This script in `app/static/js/components/photoupload.js` provides frontend browser behavior. Function responsibilities: `createPhotoUploadComponent` creates photo upload component; `renderPreview` renders preview.