# TagList Component - Documentation

## Overview
A reusable, pure UI component for displaying and managing removable tags. Built for the SnipSnap barber discovery app.

**Author:** MIRZA MD SAKIF SHAHNOOR
**Project:** SnipSnap - Group 7E, University of Portsmouth  
**Component Type:** Pure UI (no backend calls, no business logic)

---

## Features
- Display tags with remove functionality
- Support for 4 tag types: `filter`, `tag`, `barber`, `barbershop`
- Public API: `add_item()` and `get_items()`
- Instant UI updates on add/remove
- Built-in styling (customizable)
- Duplicate prevention
- Input validation
- Mobile responsive

---

## Quick Start

### 1. Include the component
```html
<script src="TagList.js"></script>
```

### 2. Create mount point in HTML
```html
<div id="myTagList"></div>
```

### 3. Initialize
```javascript
const tagList = new TagList('myTagList');
```

### 4. Use it
```javascript
// Add tags
tagList.add_item({"name": "closest", "type": "filter"});
tagList.add_item({"name": "fade", "type": "tag"});

// Get all tags
const currentTags = tagList.get_items();
console.log(currentTags);
// Output: [{"name":"closest","type":"filter"}, {"name":"fade","type":"tag"}]
```

---

## Public API

### `add_item(json)`
Adds a tag to the list.

**Parameters:**
- `json` (Object): Must contain `name` (string) and `type` (string)

**Returns:**
- `boolean`: `true` if successful, `false` if validation fails

**Supported Types:**
- `"filter"` - Filter tags (e.g., "closest", "highest rated")
- `"tag"` - Generic tags (e.g., "fade", "curly hair")
- `"barber"` - Barber name tags (e.g., "alex_barber")
- `"barbershop"` - Barbershop name tags (e.g., "Fade House")

**Example:**
```javascript
tagList.add_item({"name": "fade", "type": "tag"});
tagList.add_item({"name": "alex_barber", "type": "barber"});
```

**Validation:**
- Checks if input is valid JSON object
- Validates `name` and `type` fields exist and are strings
- Ensures `type` is one of the 4 supported types
- Prevents duplicate tags (same name + type)

---

### `get_items()`
Returns all current tags as a JSON array.

**Parameters:** None

**Returns:**
- `Array`: JSON array of tag objects, each with `name` and `type`

**Example:**
```javascript
const tags = tagList.get_items();
console.log(tags);
// Output: [
//   {"name": "closest", "type": "filter"},
//   {"name": "fade", "type": "tag"}
// ]
```

---

## Integration Examples

### Example 1: Discover Page Filters
```javascript
// User selects a filter from dropdown
function onFilterSelected(filterName) {
  tagList.add_item({
    "name": filterName,
    "type": "filter"
  });
  
  // Get all active filters to send to backend
  const activeFilters = tagList.get_items();
  
  // Send to backend (handled by backend team)
  // updateDiscoverFeed(activeFilters);
}
```

### Example 2: Search Bar Tag Addition
```javascript
// User types a tag in search bar and hits enter
searchInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    const tagName = e.target.value.trim();
    
    tagList.add_item({
      "name": tagName,
      "type": "tag"
    });
    
    e.target.value = ''; // Clear input
  }
});
```

### Example 3: Following a Barber
```javascript
// User clicks "Follow" button on barber profile
function followBarber(barberName) {
  tagList.add_item({
    "name": barberName,
    "type": "barber"
  });
  
  // Get followed barbers to filter discover feed
  const followedBarbers = tagList.get_items()
    .filter(tag => tag.type === 'barber');
}
```

---

## Styling

### Default Styling
The component includes built-in styles that match the SnipSnap urban streetwear aesthetic:
- Dark mode colors (blacks, golds, whites)
- Gold accent for filter tags
- Different colors for each tag type
- Smooth hover/remove animations
- Mobile responsive

### Custom Styling
To use your own CSS, remove the auto-injected styles section from `TagList.js` and target these classes:

```css
.taglist-container   /* Main container */
.taglist-item        /* Individual tag */
.taglist-name        /* Tag name text */
.taglist-remove      /* Remove button (X) */

/* Type-specific classes */
.tag-filter         /* Filter tags */
.tag-generic        /* Generic tags */
.tag-barber         /* Barber tags */
.tag-barbershop     /* Barbershop tags */
```

---

## Component Scope & Responsibility

### What it DOES:
- Manages internal tag state
- Renders tags with remove buttons
- Handles add/remove interactions
- Exposes public API for external use
- Validates input data

### What it DOES NOT do:
- Make backend API calls
- Contain filtering logic
- Perform search operations
- Handle business logic
- Store data persistently (state resets on page refresh)

---

## File Structure
```
TagList.js           - Main component file
TagList_Demo.html    - Demo page with usage examples
README.md           - This documentation
```

---

## Browser Support
- Chrome/Edge: 
- Firefox: 
- Safari: 
- Mobile browsers: 

**Requirements:** ES6+ support (modern browsers)

---

## Testing the Component

### Manual Testing
1. Open `TagList_Demo.html` in a browser
2. Click "Add Filter Tag" - should display gold tag
3. Click "Add Generic Tag" - should display gray tag
4. Click "Add Barber Tag" - should display gold-bordered tag
5. Click X on any tag - should remove immediately
6. Click "Get All Tags" - check console for JSON output

### Integration Testing
```javascript
// Test 1: Add valid tag
console.assert(
  tagList.add_item({"name": "test", "type": "filter"}) === true,
  "Should add valid tag"
);

// Test 2: Reject invalid type
console.assert(
  tagList.add_item({"name": "test", "type": "invalid"}) === false,
  "Should reject invalid type"
);

// Test 3: Get items returns array
console.assert(
  Array.isArray(tagList.get_items()),
  "get_items should return array"
);

// Test 4: Prevent duplicates
tagList.add_item({"name": "fade", "type": "tag"});
const beforeCount = tagList.get_items().length;
tagList.add_item({"name": "fade", "type": "tag"});
const afterCount = tagList.get_items().length;
console.assert(
  beforeCount === afterCount,
  "Should prevent duplicate tags"
);
```

---

## Troubleshooting

### Tags not displaying
- Check if mount element ID is correct
- Verify `TagList.js` is loaded before initialization
- Check browser console for errors

### Styles not applying
- Ensure auto-inject styles section is present in `TagList.js`
- Check for CSS conflicts with existing styles
- Verify no `!important` rules overriding component styles

### Remove button not working
- Check browser console for JavaScript errors
- Ensure clicks aren't being blocked by parent elements
- Verify event listeners are attached (inspect element)

---

## Future Enhancements (Optional)
- Drag-and-drop reordering
- Tag grouping by type
- Keyboard navigation support
- Animation on add/remove
- Maximum tag limit
- Persistent storage (localStorage)



---

## Contact & Support
**Component Owner:** MIRZA MD SAKIF SHAHNOOR
**Project:** SnipSnap - Group 7E  
**University:** University of Portsmouth

---

**Last Updated:** February 27, 2026  
