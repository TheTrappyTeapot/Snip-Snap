photoupload.html - Photo Upload Page Template
==========================================

**Purpose**: Interface for uploading new gallery photos (gallery posts).

**What it contains**:

- Photo selection area (drag-drop zone)
- File input button
- Image preview
- Caption/description input
- Tags/category selection
- Upload progress bar
- Submit button
- Success/error messages
- Cancel button
- Previously uploaded photos list

**How it works**:

Users select photos to upload, add captions and tags, then submit. Photos are validated, compressed, and uploaded to cloud storage. The page shows progress and success/error feedback.

**Upload Process**:

1. Drag photo or click to browse
2. Select photo from computer
3. Image preview displays
4. Enter caption/description
5. Select tags/categories
6. Click Upload
7. See progress bar
8. Receive success message
9. Photo appears in gallery

**Form Fields**:

- Photo file (required)
- Caption (optional, max 500 chars)
- Tags (optional, multi-select)
- Category (optional)

**Validation**:

- File type (JPG, PNG, WebP)
- File size (max 10MB)
- Image dimensions (min 300x300px)
- Caption max length

**Features**:

- Drag-drop support
- Image preview
- Upload progress
- Error handling
- Success confirmation
- Recent uploads display
- Batch upload option

**Mobile Support**:

- Touch-friendly
- Large file input
- Mobile camera option
- Responsive layout=

Overview
--------

app/templates/pages/photoupload.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts.

Purpose
-------

This template renders the photoupload view for the web application.
