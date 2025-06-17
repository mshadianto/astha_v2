# ===== utils/formatters.py =====
def format_rupiah(value):
    """Format number as Rupiah currency"""
    if value >= 1e12:
        return f"Rp {value/1e12:.1f}T"
    elif value >= 1e9:
        return f"Rp {value/1e9:.1f}M"
    elif value >= 1e6:
        return f"Rp {value/1e6:.1f}jt"
    else:
        return f"Rp {value:,.0f}"

def format_percentage(value, decimals=1):
    """Format number as percentage"""
    return f"{value:.{decimals}f}%"

def format_number(value, decimals=0):
    """Format number with thousands separator"""
    return f"{value:,.{decimals}f}"
