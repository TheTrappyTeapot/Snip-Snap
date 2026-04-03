// Profile Edit Feature

export function initProfileEditFeature() {
  console.log('[PROFILE EDIT] Starting feature initialization');
  
  const profileForm = document.querySelector('.dashboard-section form');

  if (!profileForm) {
    console.log('[PROFILE EDIT] Profile form not found - this is OK if there are no profile settings');
    return;
  }

  console.log('[PROFILE EDIT] Profile form found:', profileForm);
  console.log('[PROFILE EDIT] Initializing profile edit feature');

  profileForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('[PROFILE EDIT] Form submitted');

    const formData = new FormData(profileForm);
    const username = formData.get('username');

    if (!username.trim()) {
      console.warn('[PROFILE EDIT] Username is empty');
      return;
    }

    try {
      const response = await fetch(window.location.href, {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        console.log('[PROFILE EDIT] Profile updated successfully');
        const successMsg = document.createElement('div');
        successMsg.className = 'success-message show';
        successMsg.textContent = 'Profile updated successfully!';
        profileForm.parentNode.insertBefore(successMsg, profileForm);
        
        setTimeout(() => {
          successMsg.remove();
        }, 3000);
      } else {
        console.error('[PROFILE EDIT] Profile update failed');
      }
    } catch (error) {
      console.error('[PROFILE EDIT] Error updating profile:', error);
    }
  });
  
  console.log('[PROFILE EDIT] Feature initialization complete');
}
