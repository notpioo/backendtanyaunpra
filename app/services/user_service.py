import os
import firebase_admin
from firebase_admin import firestore

class UserService:
    """Service untuk mengelola data user dari Firestore"""
    
    def __init__(self):
        """Initialize service"""
        pass
    
    def _get_firestore_client(self):
        """Get Firestore client if Firebase is initialized"""
        try:
            if firebase_admin._apps:
                return firestore.client()
            return None
        except Exception as e:
            print(f"❌ Error getting Firestore client: {e}")
            return None
    
    def get_all_users(self):
        """Ambil semua data user dari Firestore"""
        try:
            db = self._get_firestore_client()
            
            if db is None:
                # Return mock data for development
                print("⚠️ UserService: Using mock data (Firebase not initialized)")
                return self._get_mock_users()
            
            print("✅ UserService: Fetching users from real Firestore database")
            # Get all documents from 'users' collection
            users_ref = db.collection('users')
            users_docs = users_ref.stream()
            
            users_list = []
            for doc in users_docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id  # Add document ID
                users_list.append({
                    'id': user_data.get('uid', doc.id),
                    'name': user_data.get('name', 'N/A'),
                    'nim': user_data.get('nim', 'N/A'),
                    'faculty': user_data.get('faculty', 'N/A'),
                    'study_program': user_data.get('studyProgram', 'N/A'),
                    'role': user_data.get('role', 'mahasiswa'),
                    'profile_image': user_data.get('profileImageUrl', ''),
                    'banner_image': user_data.get('bannerImageUrl', '')
                })
            
            # Sort by name
            users_list.sort(key=lambda x: x['name'])
            
            print(f"✅ Retrieved {len(users_list)} users from Firestore")
            return users_list
            
        except Exception as e:
            print(f"❌ Error fetching users from Firestore: {e}")
            return self._get_mock_users()
    
    def _get_mock_users(self):
        """Return mock user data for development"""
        return [
            {
                'id': 'mock1',
                'name': 'John Doe',
                'nim': '2023000001',
                'faculty': 'Fakultas Teknik',
                'study_program': 'Informatika (S1)',
                'role': 'mahasiswa',
                'profile_image': '',
                'banner_image': ''
            },
            {
                'id': 'mock2',
                'name': 'Jane Smith',
                'nim': '2023000002',
                'faculty': 'Fakultas Ekonomi',
                'study_program': 'Manajemen (S1)',
                'role': 'mahasiswa',
                'profile_image': '',
                'banner_image': ''
            },
            {
                'id': 'mock3',
                'name': 'Ahmad Abdullah',
                'nim': '2023000003',
                'faculty': 'Fakultas Ilmu Komputer',
                'study_program': 'Sistem Informasi (S1)',
                'role': 'mahasiswa',
                'profile_image': '',
                'banner_image': ''
            }
        ]
    
    def get_user_by_id(self, user_id):
        """Ambil data user berdasarkan ID"""
        try:
            db = self._get_firestore_client()
            
            if db is None:
                # Return first mock user
                mock_users = self._get_mock_users()
                return mock_users[0] if mock_users else None
            
            # Query Firestore for user with matching uid
            users_ref = db.collection('users')
            query = users_ref.where('uid', '==', user_id).limit(1)
            docs = query.stream()
            
            for doc in docs:
                user_data = doc.to_dict()
                return {
                    'id': user_data.get('uid', doc.id),
                    'name': user_data.get('name', 'N/A'),
                    'nim': user_data.get('nim', 'N/A'),
                    'faculty': user_data.get('faculty', 'N/A'),
                    'study_program': user_data.get('studyProgram', 'N/A'),
                    'role': user_data.get('role', 'mahasiswa'),
                    'profile_image': user_data.get('profileImageUrl', ''),
                    'banner_image': user_data.get('bannerImageUrl', '')
                }
            
            return None
            
        except Exception as e:
            print(f"❌ Error fetching user by ID: {e}")
            return None
    
    def get_user_stats(self):
        """Dapatkan statistik user"""
        try:
            users = self.get_all_users()
            
            # Count by faculty
            faculty_counts = {}
            for user in users:
                faculty = user.get('faculty', 'Unknown')
                faculty_counts[faculty] = faculty_counts.get(faculty, 0) + 1
            
            # Count by study program
            program_counts = {}
            for user in users:
                program = user.get('study_program', 'Unknown')
                program_counts[program] = program_counts.get(program, 0) + 1
            
            return {
                'total_users': len(users),
                'by_faculty': faculty_counts,
                'by_program': program_counts
            }
            
        except Exception as e:
            print(f"❌ Error getting user stats: {e}")
            return {
                'total_users': 0,
                'by_faculty': {},
                'by_program': {}
            }

# Create a singleton instance
user_service = UserService()
