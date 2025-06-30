import os
import time
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from app.config import Settings
from typing import Dict, Optional

class FileCleanupService:

    def __init__(self, logger: Optional[logging.Logger] = None):

        self.scheduler = BackgroundScheduler()
        self.temp_dir = "/tmp/leaseboost_uploads"
        self.cleanup_interval_minutes = Settings.file_cleanup_minutes
        self.logger = logger or logging.getLogger(__name__)
    
    def start_cleanup_scheduler(self):
        # create uploads folder if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)

        self.scheduler.add_job(
            self.cleanup_old_files,
            'interval',
            minutes=self.cleanup_interval_minutes,
            id='file_cleanup',
        )

        self.scheduler.start()

        self.logger.info(f"File cleanup scheduler started (every {self.cleanup_interval_minutes} minutes)")
    
    def cleanup_old_files(self):

        try:
            current_time = time.time()
            cutoff_time = current_time - (self.cleanup_interval_minutes * 60)

            cleaned_count = 0

            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)

                if os.path.isfile(file_path):
                    file_age = os.path.getctime(file_path)

                    if file_age < cutoff_time:
                        os.remove(file_path)
                        cleaned_count += 1

            if cleaned_count > 0:
                self.logger.info(f"Cleaned up {cleaned_count} old files")
        
        except Exception as e:
            self.logger.error(f"Error during file cleanup: {str(e)}")
    
    def stop_cleanup_scheduler(self):

        if self.scheduler.running:
            self.scheduler.shutdown()
            self.logger.info("File cleanup scheduler stopped")