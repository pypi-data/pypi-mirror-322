# magic_thumbnail/creator.py

import os
import requests
from PIL import Image
from urllib.parse import urlparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Fetch environment variables
IMAGE_SOURCES = os.getenv('IMAGE_SOURCES', '')
ENABLE_PARALLEL = os.getenv('ENABLE_PARALLEL', 'false').lower() == 'true'
LOG_FILE = os.getenv('LOG_FILE', 'magic_thumbnail.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
SUPPORTED_FORMATS_ENV = os.getenv('SUPPORTED_FORMATS', '')

# Define default supported formats
DEFAULT_SUPPORTED_FORMATS = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'webp']

# Extend supported formats based on .env
SUPPORTED_FORMATS = [fmt.strip().lower() for fmt in SUPPORTED_FORMATS_ENV.split(',') if fmt.strip()] or DEFAULT_SUPPORTED_FORMATS

# Configure logging
logger = logging.getLogger('MagicThumbnail')
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(LOG_FILE)

c_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
f_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# Create formatters and add them to handlers
c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

def is_url(path):
    """
    Check if the provided path is a URL.

    Parameters:
    - path (str): The path or URL to check.

    Returns:
    - bool: True if it's a URL, False otherwise.
    """
    parsed = urlparse(path)
    return parsed.scheme in ('http', 'https')

def generate_thumbnail_filename(original_name, size):
    """
    Generate a thumbnail filename based on the original name, size, and timestamp.

    Parameters:
    - original_name (str): The base name of the original image (without extension).
    - size (tuple): The (width, height) of the thumbnail.
    
    Returns:
    - str: The generated thumbnail filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{original_name}_thumb_{size[0]}x{size[1]}_{timestamp}.jpg"

def create_thumbnails(input_image_path, output_dir, sizes):
    """
    Create thumbnails of the input image in specified sizes, ensuring each size
    is smaller than the original image's dimensions.

    Parameters:
    - input_image_path (str): Path to the high-resolution input image.
    - output_dir (str): Directory where thumbnails will be saved.
    - sizes (list of tuples): List of (width, height) tuples for thumbnail sizes.

    Returns:
    - List of paths to the created thumbnail images.
    """
    if not os.path.isfile(input_image_path):
        raise FileNotFoundError(f"Input image not found at {input_image_path}")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the input image
    with Image.open(input_image_path) as img:
        original_width, original_height = img.size
        logger.info(f"Original image size: {original_width}x{original_height}")

        # Extract the base name without extension
        base_name = os.path.splitext(os.path.basename(input_image_path))[0]

        thumbnails = []
        for size in sizes:
            desired_width, desired_height = size

            # Check if desired size is smaller than original
            if desired_width > original_width or desired_height > original_height:
                logger.warning(
                    f"Desired size {desired_width}x{desired_height} "
                    f"is larger than the original image size. Skipping."
                )
                continue  # Skip this size

            # Create a copy of the image to avoid altering the original
            img_copy = img.copy()
            # Updated Resampling filter
            img_copy.thumbnail(size, Image.Resampling.LANCZOS)

            # Generate a better thumbnail filename
            thumbnail_filename = generate_thumbnail_filename(base_name, size)
            thumbnail_path = os.path.join(output_dir, thumbnail_filename)

            # Save the thumbnail
            img_copy.save(thumbnail_path, "JPEG")
            logger.info(f"Thumbnail created: {thumbnail_path}")
            thumbnails.append(thumbnail_path)

        if not thumbnails:
            logger.warning("No thumbnails were created. Check the requested sizes.")
        else:
            logger.info(f"Total thumbnails created: {len(thumbnails)}")

        return thumbnails

def download_image(image_url, temp_dir='temp_images'):
    """
    Download an image from a URL and save it to a temporary directory.

    Parameters:
    - image_url (str): URL of the image to download.
    - temp_dir (str): Temporary directory to store downloaded images.

    Returns:
    - str: Path to the downloaded image.
    """
    # Ensure temporary directory exists
    os.makedirs(temp_dir, exist_ok=True)

    try:
        logger.info(f"Downloading image from {image_url}...")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        # Determine image format and extension
        content_type = response.headers.get('Content-Type', '').lower()
        if 'image' not in content_type:
            raise ValueError(f"URL does not point to an image. Content-Type: {content_type}")

        # Extract the image format
        image_format = content_type.split('/')[-1]
        if image_format == 'jpeg':
            image_format = 'jpg'  # Standardize extension

        if image_format not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {image_format}")

        # Create a filename based on the image format and timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"downloaded_image_{timestamp}.{image_format}"
        temp_image_path = os.path.join(temp_dir, filename)

        # Save the image to the temporary directory
        with open(temp_image_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Image downloaded and saved to {temp_image_path}")

        return temp_image_path

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to download image from {image_url}: {e}")

def process_image(image_source, output_dir, sizes, temp_dir='temp_images'):
    """
    Process an image source (URL or local path) to create thumbnails.

    Parameters:
    - image_source (str): URL or local path of the image.
    - output_dir (str): Directory where thumbnails will be saved.
    - sizes (list of tuples): List of (width, height) tuples for thumbnail sizes.
    - temp_dir (str): Temporary directory to store downloaded images.

    Returns:
    - List of paths to the created thumbnail images.
    """
    temp_image_path = None

    try:
        if is_url(image_source):
            # Handle URL: download the image first
            temp_image_path = download_image(image_source, temp_dir)
            image_path = temp_image_path
        else:
            # Handle local path: verify the file exists
            if not os.path.isfile(image_source):
                raise FileNotFoundError(f"Local image not found at {image_source}")
            image_path = image_source
            logger.info(f"Using local image: {image_path}")

        # Create thumbnails using the existing function
        thumbnails = create_thumbnails(image_path, output_dir, sizes)
        logger.info("Thumbnails created successfully.")
        return thumbnails

    except Exception as e:
        raise RuntimeError(f"An error occurred while processing the image: {e}")

    finally:
        # Clean up the temporary image if it was downloaded
        if temp_image_path and os.path.exists(temp_image_path):
            os.remove(temp_image_path)
            logger.info(f"Temporary image {temp_image_path} removed.")

def process_images():
    """
    Entry point to process multiple images based on environment variables.
    Handles parallel processing if enabled.
    """
    if not IMAGE_SOURCES:
        logger.error("No IMAGE_SOURCES provided in environment variables.")
        return

    # Split IMAGE_SOURCES by comma and strip whitespace
    image_sources = [src.strip() for src in IMAGE_SOURCES.split(',') if src.strip()]

    if not image_sources:
        logger.error("IMAGE_SOURCES is empty after parsing.")
        return

    # Define thumbnail sizes (can also be made configurable via .env)
    thumbnail_sizes = [(150, 150), (300, 300), (600, 600), (2000, 2000)]  # Example sizes

    # Define output directories
    url_output_dir = "url_thumbnails"
    local_output_dir = "local_thumbnails"

    def handle_source(source):
        """
        Handle processing of a single image source.
        """
        try:
            if is_url(source):
                logger.info(f"Processing URL: {source}")
                output_directory = url_output_dir
            else:
                logger.info(f"Processing local image: {source}")
                output_directory = local_output_dir

            thumbnails = process_image(
                image_source=source,
                output_dir=output_directory,
                sizes=thumbnail_sizes,
                temp_dir="temp_images"
            )

            if thumbnails:
                logger.info("Thumbnails created at:")
                for thumb in thumbnails:
                    logger.info(f" - {thumb}")
        except Exception as e:
            logger.error(f"Failed to process {source}: {e}")

    if ENABLE_PARALLEL:
        logger.info("Parallel processing enabled.")
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(handle_source, src) for src in image_sources]
            for future in as_completed(futures):
                pass  # All logging is handled within handle_source
    else:
        logger.info("Parallel processing disabled. Processing images sequentially.")
        for src in image_sources:
            handle_source(src)
