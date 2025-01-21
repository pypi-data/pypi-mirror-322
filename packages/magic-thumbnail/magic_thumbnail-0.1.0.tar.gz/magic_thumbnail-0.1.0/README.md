# Magic Thumbnail

**Magic Thumbnail** is a Python library designed to generate multiple thumbnails from high-resolution images. It supports downloading images from URLs or using local image files, handles multiple image sources, and offers advanced logging and parallel processing capabilities.

## Features

- **Multiple Image Sources**: Process multiple images from URLs or local paths.
- **Flexible Thumbnail Sizes**: Specify custom thumbnail dimensions.
- **Advanced Logging**: Logs detailed information to both console and log files.
- **Parallel Processing**: Utilize multiple threads for faster processing.
- **Extensible Formats**: Support for various image formats, configurable via environment variables.

## Installation

Install the package using `pip`:

```bash
pip install magic_thumbnail
```

## Usage
### 1. Set Up Environment Variables
Create a .env file in your project directory with the following variables:

```
# .env

# Comma-separated list of image URLs or local file paths
IMAGE_SOURCES=https://via.placeholder.com/1200, /path/to/local/image.jpg

# Enable parallel processing (true/false)
ENABLE_PARALLEL=true

# Log file name
LOG_FILE=magic_thumbnail.log

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Supported image formats (comma-separated)
SUPPORTED_FORMATS=jpeg,jpg,png,gif,bmp,tiff,webp

# Ensure there are no spaces around the commas.

```

### 2. Example Script
Here's how you can use the magic_thumbnail library in your Python project:

```# example_usage.py

from magic_thumbnail import process_images

def main():
    process_images()

if __name__ == "__main__":
    main()
```


### 3. Run the Script
Execute your script:
```bash
python example_usage.py
```

### 4. Output
Thumbnails will be saved in the specified output directories (url_thumbnails and local_thumbnails). Logs will be written to the console and the specified log file (magic_thumbnail.log).

## API Reference
`process_images()`
Processes multiple images based on the IMAGE_SOURCES environment variable. Handles both URLs and local file paths.
- Parameters: None (configurations are read from environment variables)
- Returns: None

## Configuration
All configurations are managed via environment variables in the .env file.

## Environment Variables
`IMAGE_SOURCES`: Comma-separated list of image URLs or local file paths.
`ENABLE_PARALLEL`: Enable (true) or disable (false) parallel processing.
`LOG_FILE`: Name of the log file.
`LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
`SUPPORTED_FORMATS`: Comma-separated list of supported image formats.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.