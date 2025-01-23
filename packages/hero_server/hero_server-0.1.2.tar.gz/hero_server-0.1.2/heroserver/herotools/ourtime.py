from datetime import datetime, timezone, timedelta
import re


def epoch_get(deadline: str) -> int:
        """
        Set the deadline based on various input formats.
        
        Supports:
        - Relative: +1h (hours), +2d (days), +1w (week), +1m (month)
        - Absolute: 20/10/2024, 20/10, 20/10/24 (all same day)
        
        If hour not specified, defaults to midday (noon).
        
        Returns the deadline as a Unix timestamp (epoch).
        """
        now = datetime.now(timezone.utc)
        
        # Check for relative time format
        relative_match = re.match(r'\+(\d+)([hdwm])', deadline)
        if relative_match:
            amount, unit = relative_match.groups()
            amount = int(amount)
            if unit == 'h':
                delta = timedelta(hours=amount)
            elif unit == 'd':
                delta = timedelta(days=amount)
            elif unit == 'w':
                delta = timedelta(weeks=amount)
            elif unit == 'm':
                delta = timedelta(days=amount * 30)  # Approximate
            
            new_deadline = now + delta
            return int(new_deadline.timestamp())
        
        # Check for absolute date format
        date_formats = ['%d/%m/%Y', '%d/%m/%y', '%d/%m']
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(deadline, fmt)
                if fmt == '%d/%m':
                    # If year is not provided, use the current year
                    date_obj = date_obj.replace(year=now.year)
                
                # If the resulting date is in the past, assume next year
                if date_obj.replace(tzinfo=timezone.utc) < now:
                    date_obj = date_obj.replace(year=date_obj.year + 1)
                
                # Set time to noon (12:00)
                date_obj = date_obj.replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
                return int(date_obj.timestamp())
            except ValueError:
                continue
        
        raise ValueError("Invalid deadline format. Use +Xh/d/w/m for relative or DD/MM/YYYY for absolute dates.")
