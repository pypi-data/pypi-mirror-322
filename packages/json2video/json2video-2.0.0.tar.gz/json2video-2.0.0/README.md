# JSON2Video Python SDK

Python SDK for creating videos programmatically using JSON2Video API.

## Installation

```bash
pip install json2video
```

## Quick Start

```python
from json2video import Movie, Scene

# Create a new movie
movie = Movie()
movie.set_api_key("YOUR-API-KEY")  # Get your API key at https://json2video.com/get-api-key/

# Set movie properties
movie.set("width", 1920)
movie.set("height", 1080)

# Create a scene
scene = Scene()
scene.set("duration", 5)
scene.set("background-color", "#000000")

# Add elements to the scene
scene.add_element({
    "type": "text",
    "text": "Hello World!",
    "style": {
        "fontSize": 64,
        "color": "#FFFFFF"
    }
})

# Add scene to movie
movie.add_scene(scene)

# Render the movie
response = movie.render()

# Wait for the movie to finish rendering
result = movie.wait_to_finish()
print(result)
```

## Documentation

For full documentation, visit [JSON2Video Documentation](https://json2video.com/docs/).

## Requirements

- Python 3.8 or higher
- `requests` library

## License

MIT License 