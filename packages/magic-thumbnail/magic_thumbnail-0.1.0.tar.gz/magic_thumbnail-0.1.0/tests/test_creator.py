# tests/test_creator.py

import unittest
import os
from magic_thumbnail.creator import create_thumbnails, download_image, process_image, is_url
from unittest.mock import patch
from PIL import Image

class TestMagicThumbnail(unittest.TestCase):
    def setUp(self):
        # Create a sample image for testing
        self.sample_image_path = 'tests/sample_image.jpg'
        os.makedirs('tests', exist_ok=True)
        img = Image.new('RGB', (1200, 1200), color = 'red')
        img.save(self.sample_image_path)

        # Define output directory
        self.output_dir = 'tests/output'
        os.makedirs(self.output_dir, exist_ok=True)

        # Define thumbnail sizes
        self.sizes = [(150, 150), (300, 300), (600, 600), (2000, 2000)]  # Includes an oversized size

    def tearDown(self):
        # Remove created files and directories
        if os.path.exists(self.sample_image_path):
            os.remove(self.sample_image_path)
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, file))
            os.rmdir(self.output_dir)
        if os.path.exists('temp_images'):
            for file in os.listdir('temp_images'):
                os.remove(os.path.join('temp_images', file))
            os.rmdir('temp_images')

    def test_is_url(self):
        self.assertTrue(is_url('https://example.com/image.jpg'))
        self.assertFalse(is_url('/path/to/image.jpg'))

    def test_create_thumbnails(self):
        thumbnails = create_thumbnails(self.sample_image_path, self.output_dir, self.sizes)
        self.assertEqual(len(thumbnails), 3)  # Should skip the oversized size

        for thumb in thumbnails:
            self.assertTrue(os.path.isfile(thumb))
            with Image.open(thumb) as img:
                self.assertIn(img.size, self.sizes[:3])

    @patch('magic_thumbnail.creator.requests.get')
    def test_download_image(self, mock_get):
        # Mock response
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'Content-Type': 'image/jpeg'}
        mock_get.return_value.content = b'test image content'

        downloaded_path = download_image('https://example.com/image.jpg')
        self.assertTrue(os.path.isfile(downloaded_path))
        os.remove(downloaded_path)

    @patch('magic_thumbnail.creator.create_thumbnails')
    @patch('magic_thumbnail.creator.download_image')
    def test_process_image_url(self, mock_download_image, mock_create_thumbnails):
        mock_download_image.return_value = 'temp_images/downloaded_image.jpg'
        mock_create_thumbnails.return_value = ['thumb1.jpg', 'thumb2.jpg']

        thumbnails = process_image('https://example.com/image.jpg', 'tests/output', self.sizes)
        self.assertEqual(len(thumbnails), 2)
        mock_download_image.assert_called_once_with('https://example.com/image.jpg', 'temp_images')
        mock_create_thumbnails.assert_called_once_with('temp_images/downloaded_image.jpg', 'tests/output', self.sizes)

    def test_process_image_local(self):
        thumbnails = process_image(self.sample_image_path, self.output_dir, self.sizes)
        self.assertEqual(len(thumbnails), 3)
        for thumb in thumbnails:
            self.assertTrue(os.path.isfile(thumb))

if __name__ == '__main__':
    unittest.main()
