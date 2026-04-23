/* Script for app/static/js/pages/dashboard.js. */

import { initUploadPostFeature } from '../features/uploadPost.js';
import { initGalleryEditFeature } from '../features/galleryEdit.js';
import { initProfileEditFeature } from '../features/profileEdit.js';

console.log('[DASHBOARD] Dashboard module loaded');

// Initialize features when DOM is ready
// Module scripts defer by default, so this should be safe to run immediately
// But we'll check document.readyState to be safe
function initializeFeatures() {
  try {
    console.log('[DASHBOARD] Initializing features');
    initUploadPostFeature();
    console.log('[DASHBOARD] Upload post feature initialized');
    
    initGalleryEditFeature();
    console.log('[DASHBOARD] Gallery edit feature initialized');
    
    initProfileEditFeature();
    console.log('[DASHBOARD] Profile edit feature initialized');
    
    console.log('[DASHBOARD] All features initialized successfully');
  } catch (error) {
    console.error('[DASHBOARD] Error initializing features:', error);
    console.error('[DASHBOARD] Stack:', error.stack);
  }
}

// DOM should be ready since module scripts defer
if (document.readyState === 'loading') {
  console.log('[DASHBOARD] DOM still loading, waiting for DOMContentLoaded');
  document.addEventListener('DOMContentLoaded', initializeFeatures);
} else {
  console.log('[DASHBOARD] DOM already loaded, initializing now');
  initializeFeatures();
}
