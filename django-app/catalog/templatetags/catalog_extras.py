from django import template

register = template.Library()

@register.filter
def animation_delay(value):
    """Convert a number to animation delay in seconds"""
    return f"{float(value) * 0.1:.1f}"

@register.filter
def format_duration(seconds):
    """Format seconds as MM:SS"""
    if not seconds:
        return "0:00"
    
    try:
        seconds = int(seconds)
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02d}"
    except (ValueError, TypeError):
        return "0:00" 