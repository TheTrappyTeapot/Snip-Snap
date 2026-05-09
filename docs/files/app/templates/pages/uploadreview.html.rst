uploadreview.html - Write Review Page Template
============================================

**Purpose**: Form for customers to submit reviews and ratings for barbers.

**What it contains**:

- Barber info/photo display
- Star rating selector (1-5 stars)
- Review text area (with character count)
- Title field (optional)
- Upload photo option (optional)
- Submit button
- Cancel button
- Preview of review
- Form validation messages

**How it works**:

Customers can submit reviews about their haircut experience. They rate the barber with stars and write optional comments. Photos of the haircut can be attached.

**Review Form**:

1. User views barber being reviewed
2. Selects star rating (required)
3. Optionally uploads before/after photo
4. Enters review title (optional)
5. Writes review text (min 10, max 1000 chars)
6. Optionally adds tags
7. Clicks Submit
8. Review posted and visible

**Form Fields**:

- **Rating**: 1-5 stars (required)
- **Title**: Review title (optional)
- **Text**: Review body (optional, 1000 max)
- **Photo**: Before/after photo (optional)
- **Tags**: Haircut type tags (optional)

**Validation**:

- Rating required
- Review text max 1000 chars
- Photo file size/type
- One review per customer per barber

**Features**:

- Star rating widget
- Live character count
- Photo upload
- Preview before submit
- Success message
- Edit existing review
- Delete review option

**Mobile Responsive**:

- Full-width form
- Large star targets
- Mobile photo upload
- Touch-friendly buttons=

Overview
--------

app/templates/pages/uploadreview.html defines the HTML/Jinja structure, page regions, and server-rendered placeholders required by this screen. It composes display sections for content rendering and component mounting points used by client scripts.

Purpose
-------

This template renders the uploadreview view for the web application.
