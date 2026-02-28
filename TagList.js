/**
 * TagList Component - Reusable Tag Display & Management
 * 
 * A pure UI component that displays a list of removable tags.
 * Supports types: filter, tag, barber, barbershop
 * 
 * Public API:
 *   - add_item(json): Add a tag to the list
 *   - get_items(): Get all current tags as JSON array
 * 
 * Author: MIRZA MD SAKIF SHAHNOOR - SnipSnap Project
 * University of Portsmouth - Group 7E
 */

class TagList {
  constructor(mountElementId) {
    // Internal state - stores all current tags
    this.tags = [];
    
    // Mount point - where this component renders
    this.mountElement = document.getElementById(mountElementId);
    
    if (!this.mountElement) {
      console.error(`TagList: Mount element '${mountElementId}' not found`);
      return;
    }
    
    // Initial render
    this.render();
  }

  /**
   * PUBLIC API: Add a tag to the list
   * @param {Object} tagJson - Must contain {name: string, type: string}
   * @returns {boolean} - Success status
   * 
   * Example usage:
   *   tagList.add_item({"name": "closest", "type": "filter"})
   */
  add_item(tagJson) {
    // Validate input
    if (!tagJson || typeof tagJson !== 'object') {
      console.error('TagList.add_item: Invalid input - must be JSON object');
      return false;
    }

    if (!tagJson.name || typeof tagJson.name !== 'string') {
      console.error('TagList.add_item: Missing or invalid "name" field');
      return false;
    }

    if (!tagJson.type || typeof tagJson.type !== 'string') {
      console.error('TagList.add_item: Missing or invalid "type" field');
      return false;
    }

    // Validate type is one of the supported types
    const validTypes = ['filter', 'tag', 'barber', 'barbershop'];
    if (!validTypes.includes(tagJson.type)) {
      console.error(`TagList.add_item: Invalid type "${tagJson.type}". Must be one of: ${validTypes.join(', ')}`);
      return false;
    }

    // Check for duplicates (optional - prevents same tag being added twice)
    const isDuplicate = this.tags.some(
      tag => tag.name === tagJson.name && tag.type === tagJson.type
    );
    
    if (isDuplicate) {
      console.warn('TagList.add_item: Tag already exists in list');
      return false;
    }

    // Add tag to internal state
    this.tags.push({
      name: tagJson.name,
      type: tagJson.type
    });

    // Re-render UI
    this.render();
    
    return true;
  }

  /**
   * PUBLIC API: Get all current tags
   * @returns {Array} - JSON array of all tags with name and type
   * 
   * Example output:
   *   [
   *     {"name": "closest", "type": "filter"},
   *     {"name": "fade", "type": "tag"},
   *     {"name": "alex_barber", "type": "barber"}
   *   ]
   */
  get_items() {
    // Return a copy to prevent external modification
    return this.tags.map(tag => ({
      name: tag.name,
      type: tag.type
    }));
  }

  /**
   * PRIVATE: Remove a tag by index
   * @param {number} index - Index of tag to remove
   */
  _removeTag(index) {
    if (index >= 0 && index < this.tags.length) {
      this.tags.splice(index, 1);
      this.render();
    }
  }

  /**
   * PRIVATE: Get CSS class for tag type (for styling)
   * @param {string} type - Tag type
   * @returns {string} - CSS class name
   */
  _getTagClass(type) {
    const classMap = {
      'filter': 'tag-filter',
      'tag': 'tag-generic',
      'barber': 'tag-barber',
      'barbershop': 'tag-barbershop'
    };
    return classMap[type] || 'tag-default';
  }

  /**
   * PRIVATE: Render the component
   * Updates the DOM with current tag state
   */
  render() {
    if (!this.mountElement) return;

    // Clear existing content
    this.mountElement.innerHTML = '';

    // Create container
    const container = document.createElement('div');
    container.className = 'taglist-container';

    // Render each tag
    this.tags.forEach((tag, index) => {
      const tagElement = document.createElement('div');
      tagElement.className = `taglist-item ${this._getTagClass(tag.type)}`;
      
      // Tag name text
      const nameSpan = document.createElement('span');
      nameSpan.className = 'taglist-name';
      nameSpan.textContent = tag.name;
      
      // Remove button (X)
      const removeBtn = document.createElement('button');
      removeBtn.className = 'taglist-remove';
      removeBtn.textContent = '×';
      removeBtn.setAttribute('aria-label', `Remove ${tag.name} tag`);
      
      // Click handler for remove
      removeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this._removeTag(index);
      });
      
      // Assemble tag element
      tagElement.appendChild(nameSpan);
      tagElement.appendChild(removeBtn);
      container.appendChild(tagElement);
    });

    // Mount to DOM
    this.mountElement.appendChild(container);
  }
}

/**
 * OPTIONAL: Auto-inject basic styles
 * Remove this if you want to use external CSS
 */
(function injectStyles() {
  if (document.getElementById('taglist-styles')) return;
  
  const style = document.createElement('style');
  style.id = 'taglist-styles';
  style.textContent = `
    .taglist-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 8px 0;
    }

    .taglist-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 500;
      transition: all 0.2s ease;
    }

    .taglist-name {
      user-select: none;
    }

    .taglist-remove {
      background: none;
      border: none;
      font-size: 20px;
      line-height: 1;
      cursor: pointer;
      padding: 0;
      margin: 0;
      color: inherit;
      opacity: 0.7;
      transition: opacity 0.2s ease;
    }

    .taglist-remove:hover {
      opacity: 1;
    }

    /* Type-specific styles */
    .tag-filter {
      background: #D4AF37;
      color: #000;
    }

    .tag-generic {
      background: #2A2A2A;
      color: #FFF;
    }

    .tag-barber {
      background: #1A1A1A;
      color: #D4AF37;
      border: 1px solid #D4AF37;
    }

    .tag-barbershop {
      background: #0A0A0A;
      color: #FFF;
      border: 1px solid #2A2A2A;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .taglist-item {
        font-size: 12px;
        padding: 5px 10px;
      }
    }
  `;
  document.head.appendChild(style);
})();

// Export for use in other modules (if using module system)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TagList;
}
