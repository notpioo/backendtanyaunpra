from datetime import datetime, timezone, timedelta
import uuid
from app.config.firebase_config import get_db

# WIB Timezone (GMT+7)
WIB = timezone(timedelta(hours=7))

class ScheduleService:
    def __init__(self):
        self.db_ref = None

    def get_db_ref(self):
        """Get database reference"""
        if self.db_ref is None:
            self.db_ref = get_db()
        return self.db_ref

    def get_all_schedules(self):
        """Get all schedule events"""
        try:
            db_ref = self.get_db_ref()
            schedules_ref = db_ref.child('schedules')
            data = schedules_ref.get()

            if data:
                schedules = []
                for key, value in data.items():
                    # Support both old (date) and new (start_date/end_date) format
                    start_date = value.get('tanggal_mulai') or value.get('start_date') or value.get('date', '')
                    end_date = value.get('tanggal_selesai') or value.get('end_date') or value.get('date', '')
                    
                    schedule = {
                        'id': key,
                        'judul': value.get('judul') or value.get('title', 'No Title'),
                        'tanggal_mulai': start_date,
                        'tanggal_selesai': end_date,
                        'dibuat_pada': value.get('dibuat_pada') or value.get('created_at', ''),
                        'diperbarui_pada': value.get('diperbarui_pada') or value.get('updated_at', '')
                    }
                    schedules.append(schedule)

                # Sort by start_date (newest first)
                schedules.sort(key=lambda x: x.get('tanggal_mulai', ''), reverse=True)
                return schedules
            else:
                return []

        except Exception as e:
            print(f"❌ Error getting schedules: {e}")
            return []

    def get_schedule_by_id(self, schedule_id: str):
        """Get schedule by ID"""
        try:
            db_ref = self.get_db_ref()
            schedule_ref = db_ref.child('schedules').child(schedule_id)
            data = schedule_ref.get()

            if data:
                # Support both old (date) and new (start_date/end_date) format
                start_date = data.get('tanggal_mulai') or data.get('start_date') or data.get('date', '')
                end_date = data.get('tanggal_selesai') or data.get('end_date') or data.get('date', '')
                
                return {
                    'id': schedule_id,
                    'judul': data.get('judul') or data.get('title', 'No Title'),
                    'tanggal_mulai': start_date,
                    'tanggal_selesai': end_date,
                    'dibuat_pada': data.get('dibuat_pada') or data.get('created_at', ''),
                    'diperbarui_pada': data.get('diperbarui_pada') or data.get('updated_at', '')
                }
            else:
                return None

        except Exception as e:
            print(f"❌ Error getting schedule: {e}")
            return None

    def get_schedules_by_date_range(self, start_date: str, end_date: str):
        """Get schedules within date range for mobile app calendar view"""
        try:
            all_schedules = self.get_all_schedules()

            if not start_date or not end_date:
                return all_schedules

            filtered = [
                s for s in all_schedules 
                if start_date <= s.get('tanggal_mulai', '') <= end_date
            ]

            # Sort by date
            filtered.sort(key=lambda x: x.get('tanggal_mulai', ''))
            return filtered

        except Exception as e:
            print(f"❌ Error filtering schedules by date range: {e}")
            return []

    def create_schedule(self, title: str, start_date: str, end_date: str = None) -> dict:
        """Create new schedule event"""
        try:
            db_ref = self.get_db_ref()
            schedules_ref = db_ref.child('schedules')

            schedule_id = str(uuid.uuid4())
            now = datetime.now(WIB).strftime('%Y-%m-%d %H:%M:%S')

            # If end_date not provided, use start_date as end_date (single day event)
            if not end_date:
                end_date = start_date

            schedule_data = {
                'judul': title,
                'tanggal_mulai': start_date,
                'tanggal_selesai': end_date,
                'dibuat_pada': now,
                'diperbarui_pada': now
            }

            schedules_ref.child(schedule_id).set(schedule_data)
            print(f"✅ Schedule created successfully with ID: {schedule_id}")

            return {
                'id': schedule_id,
                **schedule_data
            }

        except Exception as e:
            print(f"❌ Error creating schedule: {e}")
            return None

    def update_schedule(self, schedule_id: str, title: str, start_date: str, end_date: str = None) -> bool:
        """Update existing schedule event"""
        try:
            db_ref = self.get_db_ref()
            schedule_ref = db_ref.child('schedules').child(schedule_id)

            existing = schedule_ref.get()
            if not existing:
                print(f"❌ Schedule {schedule_id} not found")
                return False

            # If end_date not provided, use start_date as end_date (single day event)
            if not end_date:
                end_date = start_date

            update_data = {
                'judul': title,
                'tanggal_mulai': start_date,
                'tanggal_selesai': end_date,
                'diperbarui_pada': datetime.now(WIB).strftime('%Y-%m-%d %H:%M:%S')
            }

            schedule_ref.update(update_data)
            print(f"✅ Schedule {schedule_id} updated successfully")
            return True

        except Exception as e:
            print(f"❌ Error updating schedule: {e}")
            return False

    def delete_schedule(self, schedule_id: str) -> bool:
        """Delete schedule event"""
        try:
            db_ref = self.get_db_ref()
            schedule_ref = db_ref.child('schedules').child(schedule_id)

            existing = schedule_ref.get()
            if not existing:
                print(f"❌ Schedule {schedule_id} not found")
                return False

            schedule_ref.delete()
            print(f"✅ Schedule {schedule_id} deleted successfully")
            return True

        except Exception as e:
            print(f"❌ Error deleting schedule: {e}")
            return False

    def get_schedule_stats(self):
        """Get schedule statistics"""
        try:
            schedules = self.get_all_schedules()

            today = datetime.now(WIB).date().isoformat()

            upcoming = [s for s in schedules if s.get('tanggal_selesai', '') >= today]
            past = [s for s in schedules if s.get('tanggal_selesai', '') < today]

            # Get this month schedules
            current_month = datetime.now(WIB).strftime('%Y-%m')
            this_month = [s for s in schedules if s.get('tanggal_mulai', '').startswith(current_month)]

            stats = {
                'total_schedules': len(schedules),
                'upcoming_count': len(upcoming),
                'past_count': len(past),
                'this_month_count': len(this_month)
            }

            return stats

        except Exception as e:
            print(f"❌ Error getting schedule stats: {e}")
            return {
                'total_schedules': 0,
                'upcoming_count': 0,
                'past_count': 0,
                'this_month_count': 0
            }

# Global instance
schedule_service = ScheduleService()