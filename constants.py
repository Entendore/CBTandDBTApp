# FIX: Removed side-effect `Window.clearcolor = CLR_APP_BG` from module level.
# That import-time side effect could cause issues during testing or before
# the window is ready. It's now set in TherapyApp.build().

# -- Backgrounds --
CLR_APP_BG = (0.97, 0.96, 0.94, 1)        # Warm off-white

# -- Navigation Bar --
CLR_NAV_BG    = (0.13, 0.11, 0.21, 1)      # Deep indigo
CLR_NAV_TEXT  = (0.92, 0.91, 0.96, 1)      # Soft white

# -- Typography --
CLR_TITLE     = (0.13, 0.11, 0.21, 1)      # Deep indigo
CLR_HEADING   = (0.22, 0.20, 0.30, 1)      # Dark slate
CLR_BODY      = (0.30, 0.28, 0.36, 1)      # Medium slate
CLR_LIGHT_TEXT = (0.55, 0.53, 0.60, 1)     # Light slate
CLR_WHITE     = (1.0, 1.0, 1.0, 1)         # Pure white

# -- CBT Section — Ocean Blue --
CLR_CBT_PRIMARY = (0.11, 0.35, 0.60, 1)    # Deep blue
CLR_CBT_SECOND  = (0.18, 0.50, 0.78, 1)    # Medium blue
CLR_CBT_LIGHT   = (0.30, 0.62, 0.88, 1)    # Light blue
CLR_CBT_BG      = (0.91, 0.94, 0.98, 1)    # Pale blue tint

# -- DBT Section — Rich Plum --
CLR_DBT_PRIMARY = (0.44, 0.16, 0.48, 1)    # Deep plum
CLR_DBT_SECOND  = (0.56, 0.28, 0.60, 1)    # Medium plum
CLR_DBT_LIGHT   = (0.68, 0.42, 0.72, 1)    # Light plum
CLR_DBT_BG      = (0.95, 0.91, 0.96, 1)    # Pale plum tint

# -- Soothe Section — Forest Teal --
CLR_SOOTHE_PRIMARY = (0.08, 0.44, 0.40, 1) # Deep teal
CLR_SOOTHE_SECOND  = (0.14, 0.58, 0.52, 1) # Medium teal
CLR_SOOTHE_LIGHT   = (0.22, 0.70, 0.62, 1) # Light teal
CLR_SOOTHE_BG      = (0.91, 0.96, 0.95, 1) # Pale teal tint

# -- Tools Section — Warm Amber --
CLR_TOOLS_PRIMARY = (0.68, 0.44, 0.08, 1)  # Deep amber
CLR_TOOLS_SECOND  = (0.80, 0.56, 0.14, 1)  # Medium amber
CLR_TOOLS_LIGHT   = (0.90, 0.68, 0.24, 1)  # Light amber
CLR_TOOLS_BG      = (0.98, 0.95, 0.90, 1)  # Pale amber tint

# -- Actions --
CLR_SAVE         = (0.10, 0.50, 0.28, 1)   # Confident green
CLR_BACK         = (0.68, 0.12, 0.12, 1)   # Clear red
CLR_CRISIS       = (0.75, 0.10, 0.10, 1)   # Alert red
CLR_ALERT_ORANGE = (0.85, 0.45, 0.10, 1)   # Warning orange

# -- Specialty --
CLR_MOOD_BLUE    = (0.18, 0.40, 0.62, 1)   # Calm blue for mood
CLR_BREATHE_IN   = (0.18, 0.50, 0.78, 1)   # Inhale blue
CLR_BREATHE_HOLD = (0.80, 0.68, 0.10, 1)   # Hold gold
CLR_BREATHE_OUT  = (0.10, 0.50, 0.28, 1)   # Exhale green
CLR_MINDFUL      = (0.10, 0.48, 0.42, 1)   # Mindful teal

# -- Data --
DATA_FILE = "therapy_data_final.json"