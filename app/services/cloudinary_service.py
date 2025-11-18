import os
import cloudinary
import cloudinary.uploader
from typing import Optional, Dict

class CloudinaryService:
    def __init__(self):
        """Initialize Cloudinary with credentials from environment variables"""
        self.cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        self.api_key = os.environ.get('CLOUDINARY_API_KEY')
        self.api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        
        # Validate credentials
        if not all([self.cloud_name, self.api_key, self.api_secret]):
            print("⚠️  Warning: Cloudinary credentials not fully configured")
            print(f"   CLOUDINARY_CLOUD_NAME: {'✓' if self.cloud_name else '✗'}")
            print(f"   CLOUDINARY_API_KEY: {'✓' if self.api_key else '✗'}")
            print(f"   CLOUDINARY_API_SECRET: {'✓' if self.api_secret else '✗'}")
            self.configured = False
        else:
            cloudinary.config(
                cloud_name=self.cloud_name,
                api_key=self.api_key,
                api_secret=self.api_secret
            )
            self.configured = True
            print("✅ Cloudinary configured successfully")
    
    def _check_configured(self) -> bool:
        """Check if Cloudinary is properly configured"""
        if not self.configured:
            print("❌ Cloudinary not configured: Missing credentials")
            return False
        return True
    
    def upload_image(self, file_data, folder: str = "knowledge") -> Optional[Dict]:
        """
        Upload image to Cloudinary
        
        Args:
            file_data: File object from Flask request.files
            folder: Cloudinary folder name (default: knowledge)
            
        Returns:
            Dict with url and public_id if successful, None otherwise
        """
        if not self._check_configured():
            return None
            
        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file_data,
                folder=folder,
                resource_type="image",
                transformation=[
                    {'width': 1000, 'crop': 'limit'},  # Limit width to 1000px
                    {'quality': 'auto:good'}  # Auto optimize quality
                ]
            )
            
            print(f"✅ Image uploaded to Cloudinary: {result.get('public_id')}")
            
            return {
                'url': result.get('secure_url'),
                'public_id': result.get('public_id'),
                'width': result.get('width'),
                'height': result.get('height'),
                'format': result.get('format')
            }
        except Exception as e:
            print(f"❌ Error uploading to Cloudinary: {e}")
            return None
    
    def delete_image(self, public_id: str) -> bool:
        """
        Delete image from Cloudinary
        
        Args:
            public_id: The public_id of the image to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self._check_configured():
            return False
            
        try:
            result = cloudinary.uploader.destroy(public_id)
            success = result.get('result') == 'ok'
            if success:
                print(f"✅ Image deleted from Cloudinary: {public_id}")
            else:
                print(f"⚠️  Cloudinary delete returned: {result.get('result')}")
            return success
        except Exception as e:
            print(f"❌ Error deleting from Cloudinary: {e}")
            return False
    
    def get_image_url(self, public_id: str, width: Optional[int] = None) -> str:
        """
        Get optimized image URL from Cloudinary
        
        Args:
            public_id: The public_id of the image
            width: Optional width for transformation
            
        Returns:
            Image URL
        """
        if not self._check_configured():
            return ""
            
        try:
            if width:
                url = cloudinary.CloudinaryImage(public_id).build_url(
                    width=width,
                    crop='limit',
                    quality='auto:good'
                )
            else:
                url = cloudinary.CloudinaryImage(public_id).build_url()
            return url
        except Exception as e:
            print(f"❌ Error getting image URL: {e}")
            return ""
