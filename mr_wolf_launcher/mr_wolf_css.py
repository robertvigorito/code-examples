

# Main color: #030a0d
# Main radial gradient qradialgradient(cx: 0.5, cy: 0.5,fx: 0.5, fy: 0.5,radius: 0.9, stop:0 #123140, stop:1 black)
# Hover color: #123140
# Pressed color: #111f42

main_style = \
    '* {color: gray; font-family: Open Sans; }' \
    '#HeaderMenu ' \
    '{background-color: #030a0d; border-bottom: .5px solid gray;}' \
    '' \
    '#MainMenu ' \
    '{background: qradialgradient(cx: 0.5, cy: 0.5,fx: 0.5, fy: 0.5,radius: 0.9, stop:0 #123140, stop:1 black);}' \
    '' \
    '#BottomMenu ' \
    '{background-color: #030a0d; border-top: .5px solid gray;}' \
    '' \
    '#CancelButton ' \
    '{background-color: #030a0d; border: 2px solid gray; height: 25px; width: 90px; border-radius: 8px}' \
    '#CancelButton:hover ' \
    '{background: #123140}' \
    '' \
    '#MinimizeButton ' \
    '{background: None; border-radius: 3px; height: 30px; font-size:35px;}' \
    '#MinimizeButton:hover ' \
    '{background-color: #123140;}' \
    '' \
    'QTabBar::tab ' \
    '{border-bottom:1px solid gray; height: 35px; width: 125px; font: 16px; background-color:rgba(0,0,0,0);' \
    'margin: 0 20 0 10;}' \
    'QTabBar:tab:hover ' \
    '{font-weight: bold;}' \
    'QTabBar:tab:selected ' \
    '{font-weight: bold;}' \
    '' \
    'QTabWidget::pane ' \
    '{border: None; background-color: rgba(0,0,0,0);}' \
    '' \
    'QLabel ' \
    '{height: 50px;font: 14px;}' \
    '' \
    '#ToolButton ' \
    '{background-color: rgba(0,0,0,100);}' \
    '#ToolButton:hover' \
    '{background-color: black;}' \
    '#ToolButton:pressed' \
    '{background-color: #111f42;}' \
    '' \
    '#ToolLabel ' \
    '{background-color: rgba(0,0,0,255);}' \
    '' \
    'QPixmap:hover ' \
    '{blackground-color: black;}' \

