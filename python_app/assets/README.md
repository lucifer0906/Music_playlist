# Assets Folder

This folder contains cover images and icons for the music player.

## Cover Images

- Place cover images here with the naming format: `<song_basename>.jpg` or `<song_basename>.png`
- For example, if your song is `summer_love.mp3`, place the cover as `summer_love.jpg`
- If a cover image is not found for a song, the app will use `default.jpg`

## Default Cover

The `default.jpg` file is used when no specific cover is found for a song. You can replace it with your own default cover image.

## Generating Default Cover

Run the `generate_default_cover.py` script to create a default cover image if it doesn't exist:

```bash
cd python_app/assets
python generate_default_cover.py
```

