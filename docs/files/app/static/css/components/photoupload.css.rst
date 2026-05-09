photoupload.css - Photo Upload Component Styles
===============================================

**Purpose**: Styles for the file upload and image preview interface.

**What it styles**:

- Upload drop zone with drag-and-drop support
- File input and button styling
- Image preview/thumbnail display
- Upload progress indicators
- Image cropping/editing interface (if included)
- Error message styling

**How to use**:

Include in CSS links::

    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/photoupload.css') }}">

HTML structure::

    <div class="photo-upload">
        <div class="upload-zone" id="dropZone">
            <p>Drag photos here or click to select</p>
            <input type="file" id="fileInput" accept="image/*" />
        </div>
        <div class="preview-area">
            <img id="preview" src="" />
        </div>
    </div>

**Key CSS Classes**:

- ``.photo-upload``: Main container
- ``.upload-zone``: Drop zone area
- ``.upload-zone.dragover``: Drag over state
- ``.preview-area``: Image preview section
- ``.upload-progress``: Progress bar
- ``.upload-error``: Error message styling

**Features**:

- Drag and drop file upload
- Click to browse files
- Image preview before upload
- Multiple file support
- Upload progress animation
- Error handling and messages

**Supported Formats**:

- JPG, PNG, GIF, WebP
- File size limits enforced
- Image validation

app/static/css/components/photoupload.css controls layout, spacing, typography, colors, and interaction states for its target UI surface. Its rules provide the base visual treatment used when rendering the related template/components. The file is loaded by page templates alongside app/static/css/main.css and other component/page styles as needed.

Purpose
-------

This stylesheet defines presentation rules for the photoupload component. It styles selectors such as .photo-upload, .photo-upload-btn, .photo-upload-btn:hover, and .photo-upload-btn:active.
