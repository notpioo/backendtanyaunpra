
from datetime import datetime, timedelta
from app.config.firebase_config import get_db
from collections import defaultdict
import uuid

class AnalyticsService:
    def __init__(self):
        self.db = get_db()
    
    def log_request(self, endpoint, method, status_code, response_time, ip_address, user_agent):
        """Log API request to Firebase"""
        try:
            timestamp = datetime.now()
            date_key = timestamp.strftime('%Y-%m-%d')
            time_key = timestamp.strftime('%H:%M:%S')
            
            # Structure: analytics/daily/{date}/{endpoint_method}/
            analytics_ref = self.db.child('analytics').child('daily').child(date_key)
            endpoint_key = f"{method}_{endpoint.replace('/', '_')}"
            
            # Get existing data for this endpoint today
            endpoint_data = analytics_ref.child(endpoint_key).get() or {}
            
            # Update counters
            count = endpoint_data.get('count', 0) + 1
            total_time = endpoint_data.get('total_response_time', 0) + response_time
            avg_time = total_time / count
            
            # Track errors
            errors = endpoint_data.get('errors', 0)
            if status_code >= 400:
                errors += 1
            
            # Update endpoint analytics
            analytics_ref.child(endpoint_key).update({
                'endpoint': endpoint,
                'method': method,
                'count': count,
                'total_response_time': total_time,
                'avg_response_time': round(avg_time, 3),
                'errors': errors,
                'last_request': timestamp.isoformat(),
                'status_codes': {
                    str(status_code): endpoint_data.get('status_codes', {}).get(str(status_code), 0) + 1
                }
            })
            
            # Log individual request in realtime (keep last 100)
            request_log = {
                'id': str(uuid.uuid4())[:8],
                'endpoint': endpoint,
                'method': method,
                'status_code': status_code,
                'response_time': round(response_time, 3),
                'timestamp': timestamp.isoformat(),
                'ip': ip_address[:15],  # Truncate for privacy
                'user_agent': user_agent[:100]  # Truncate long user agents
            }
            
            # Store in realtime logs (limited to last 100)
            realtime_ref = self.db.child('analytics').child('realtime')
            realtime_ref.child(request_log['id']).set(request_log)
            
            # Update global stats
            self._update_global_stats(endpoint, method, status_code)
            
        except Exception as e:
            print(f"❌ Failed to log analytics: {e}")
    
    def _update_global_stats(self, endpoint, method, status_code):
        """Update global statistics"""
        try:
            stats_ref = self.db.child('analytics').child('stats')
            stats = stats_ref.get() or {}
            
            total_requests = stats.get('total_requests', 0) + 1
            total_errors = stats.get('total_errors', 0)
            if status_code >= 400:
                total_errors += 1
            
            stats_ref.update({
                'total_requests': total_requests,
                'total_errors': total_errors,
                'last_updated': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"⚠️ Failed to update global stats: {e}")
    
    def get_daily_stats(self, date=None):
        """Get analytics for a specific date"""
        try:
            if date is None:
                date = datetime.now().strftime('%Y-%m-%d')
            
            daily_ref = self.db.child('analytics').child('daily').child(date)
            data = daily_ref.get() or {}
            
            # Convert to list format
            endpoints = []
            for key, value in data.items():
                if isinstance(value, dict):
                    endpoints.append(value)
            
            return {
                'date': date,
                'endpoints': sorted(endpoints, key=lambda x: x.get('count', 0), reverse=True),
                'total_requests': sum(e.get('count', 0) for e in endpoints),
                'total_errors': sum(e.get('errors', 0) for e in endpoints)
            }
        except Exception as e:
            print(f"❌ Failed to get daily stats: {e}")
            return {'date': date, 'endpoints': [], 'total_requests': 0, 'total_errors': 0}
    
    def get_realtime_logs(self, limit=100):
        """Get recent API requests"""
        try:
            realtime_ref = self.db.child('analytics').child('realtime')
            logs = realtime_ref.get() or {}
            
            # Convert to list and sort by timestamp
            log_list = [v for v in logs.values() if isinstance(v, dict)]
            log_list.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return log_list[:limit]
        except Exception as e:
            print(f"❌ Failed to get realtime logs: {e}")
            return []
    
    def get_global_stats(self):
        """Get overall statistics"""
        try:
            stats_ref = self.db.child('analytics').child('stats')
            stats = stats_ref.get() or {}
            
            return {
                'total_requests': stats.get('total_requests', 0),
                'total_errors': stats.get('total_errors', 0),
                'error_rate': round((stats.get('total_errors', 0) / max(stats.get('total_requests', 1), 1)) * 100, 2),
                'last_updated': stats.get('last_updated', datetime.now().isoformat())
            }
        except Exception as e:
            print(f"❌ Failed to get global stats: {e}")
            return {'total_requests': 0, 'total_errors': 0, 'error_rate': 0, 'last_updated': ''}
    
    def get_top_endpoints(self, limit=10, date=None):
        """Get most used endpoints"""
        daily_stats = self.get_daily_stats(date)
        return daily_stats['endpoints'][:limit]
    
    def cleanup_old_logs(self, days_to_keep=7):
        """Delete analytics data older than specified days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            daily_ref = self.db.child('analytics').child('daily')
            all_dates = daily_ref.get() or {}
            
            deleted_count = 0
            for date_key in all_dates.keys():
                try:
                    log_date = datetime.strptime(date_key, '%Y-%m-%d')
                    if log_date < cutoff_date:
                        daily_ref.child(date_key).delete()
                        deleted_count += 1
                except ValueError:
                    continue
            
            print(f"✅ Cleaned up {deleted_count} old analytics entries")
            return deleted_count
        except Exception as e:
            print(f"❌ Failed to cleanup old logs: {e}")
            return 0

# Global instance
analytics_service = AnalyticsService()
