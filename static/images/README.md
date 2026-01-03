# Images Folder

## Adding Your Concert Background Image

To add your own concert/music event background image:

1. Place your image file in this folder (`static/images/`)
2. Name it `concert-bg.jpg` (or update the filename in `templates/index.html`)
3. Supported formats: JPG, PNG, WebP
4. Recommended size: 1920x1080 or larger for best quality

### Current Setup

The hero section (Slide 1) currently uses a placeholder image from Unsplash. To use your own image:

1. Open `templates/index.html`
2. Find the `.slide-1` CSS section (around line 119)
3. Comment out the Unsplash URL line
4. Uncomment the local image path line
5. Update the filename if needed

Example:
```css
/* Comment this: */
/* background-image: url('https://images.unsplash.com/...'); */

/* Uncomment this: */
background-image: url('/static/images/concert-bg.jpg');
```

