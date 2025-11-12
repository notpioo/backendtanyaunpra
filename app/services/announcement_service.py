
from datetime import datetime
import uuid
from app.config.firebase_config import get_db

class AnnouncementService:
    def __init__(self):
        self.db_ref = None
    
    def get_db_ref(self):
        """Get database reference"""
        if self.db_ref is None:
            self.db_ref = get_db()
        return self.db_ref
    
    def get_all_announcements(self):
        """Get all announcements"""
        try:
            db_ref = self.get_db_ref()
            announcements_ref = db_ref.child('announcements')
            data = announcements_ref.get()
            
            if data:
                announcements = []
                for key, value in data.items():
                    announcement = {
                        'id': key,
                        'title': value.get('title', 'No Title'),
                        'message': value.get('message', 'No Message'),
                        'category': value.get('category', 'Umum'),
                        'created_at': value.get('created_at', ''),
                        'updated_at': value.get('updated_at', '')
                    }
                    announcements.append(announcement)
                
                announcements.sort(key=lambda x: x.get('created_at', ''), reverse=True)
                return announcements
            else:
                return []
                
        except Exception as e:
            print(f"❌ Error getting announcements: {e}")
            return []
    
    def get_announcement_by_id(self, announcement_id: str):
        """Get announcement by ID"""
        try:
            db_ref = self.get_db_ref()
            announcement_ref = db_ref.child('announcements').child(announcement_id)
            data = announcement_ref.get()
            
            if data:
                return {
                    'id': announcement_id,
                    'title': data.get('title', 'No Title'),
                    'message': data.get('message', 'No Message'),
                    'category': data.get('category', 'Umum'),
                    'created_at': data.get('created_at', ''),
                    'updated_at': data.get('updated_at', '')
                }
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error getting announcement: {e}")
            return None
    
    def create_announcement(self, title: str, message: str, category: str = 'Umum') -> dict:
        """Create new announcement"""
        try:
            db_ref = self.get_db_ref()
            announcements_ref = db_ref.child('announcements')
            
            announcement_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            announcement_data = {
                'title': title,
                'message': message,
                'category': category,
                'created_at': now,
                'updated_at': now
            }
            
            announcements_ref.child(announcement_id).set(announcement_data)
            print(f"✅ Announcement created successfully with ID: {announcement_id}")
            
            return {
                'id': announcement_id,
                'title': title,
                'message': message,
                'category': category,
                'created_at': now,
                'updated_at': now
            }
            
        except Exception as e:
            print(f"❌ Error creating announcement: {e}")
            return None
    
    def update_announcement(self, announcement_id: str, title: str, message: str, category: str = 'Umum') -> bool:
        """Update existing announcement"""
        try:
            db_ref = self.get_db_ref()
            announcement_ref = db_ref.child('announcements').child(announcement_id)
            
            existing = announcement_ref.get()
            if not existing:
                print(f"❌ Announcement {announcement_id} not found")
                return False
            
            update_data = {
                'title': title,
                'message': message,
                'category': category,
                'updated_at': datetime.now().isoformat()
            }
            
            announcement_ref.update(update_data)
            print(f"✅ Announcement {announcement_id} updated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error updating announcement: {e}")
            return False
    
    def delete_announcement(self, announcement_id: str) -> bool:
        """Delete announcement"""
        try:
            db_ref = self.get_db_ref()
            announcement_ref = db_ref.child('announcements').child(announcement_id)
            
            existing = announcement_ref.get()
            if not existing:
                print(f"❌ Announcement {announcement_id} not found")
                return False
            
            announcement_ref.delete()
            print(f"✅ Announcement {announcement_id} deleted successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting announcement: {e}")
            return False
    
    def get_current_announcement(self):
        """Get current announcement (for backward compatibility with dashboard)"""
        try:
            announcements = self.get_all_announcements()
            if announcements:
                latest = announcements[0]
                return {
                    'title': latest['title'],
                    'message': latest['message'],
                    'updated_at': latest['updated_at']
                }
            else:
                return {
                    'title': 'Belum ada pengumuman',
                    'message': 'Belum ada pengumuman yang dibuat. Silakan buat pengumuman baru di halaman Announcement.',
                    'updated_at': ''
                }
                
        except Exception as e:
            print(f"❌ Error getting current announcement: {e}")
            return {
                'title': 'Belum ada pengumuman',
                'message': 'Belum ada pengumuman yang dibuat.',
                'updated_at': ''
            }

# Global instance
announcement_service = AnnouncementService()
