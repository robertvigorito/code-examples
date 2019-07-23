"""
Project details scheme for shot creation, that is code friendly...

"""

proj_details = \
    {
        'TB':
            {
                'FPS': 23.976,
                'Handles': 10,
                'Resolution': (3840, 1634),
                'Final': 'exr',
                'Offset': False,  # Setting the handles offset
                'Start': 1,
                'Project': 'The boys season 1'
            },

        'CHM':
            {
                'FPS': 23.976,
                'Handles': 12,
                'Resolution': (2048, 1152),
                'Final': 'dpx',
                'Offset': True,  # Setting the handles offset
                'Start': 1001,
                'Project': 'CHM Season 1',
            },

        'LAF':
            {
                'FPS': 23.976,
                'Handles': 10,
                'Resolution': (4096, 2160),
                'Final': 'exr',
                'Offset': False,  # Setting the handles offset
                'Start': 1,
                'Project': 'LAF Season 1',
            },

        'VDA':
            {
                'FPS': 23.976,
                'Handles': 10,
                'Resolution': (3840, 2160),
                'Final': ('mov', 'ap4h'),  # Nuke mov codec prefix
                'Offset': False,  # Setting the handles offset
                'Start': 1,
                'Project': 'VIDA - Season 2',
            },

        'MRS1':
            {
                'FPS': 23.976,
                'Handles': 0,
                'Resolution': (3840, 2160),
                'Final': 'exr',
                'Offset': False,  # Setting the handles offset
                'Start': 1001,
                'Project': 'MRS',
            },

        'CLW':
            {
                'FPS': 23.976,
                'Handles': 4,
                'Resolution': (1920, 1080),
                'Final': 'dpx',
                'Offset': False,  # Setting the handles offset
                'Start': 1001,
                'Project': 'CLAWS',
            },

        'FWD':
            {
                'FPS': 23.976,
                'Handles': 10,
                'Resolution': (2048, 1152),
                'Final': 'dpx',
                'Offset': False,  # Setting the handles offset
                'Start': 1001,
                'Project': 'SCORPION - SEASON 5',
            },

        'ALV':
            {
                'FPS': 23.976,
                'Handles': 10,
                'Resolution': (1920, 1080),
                'Final': 'dpx',
                'Offset': False,  # Setting the handles offset
                'Start': 1001,
                'Project': 'ALV',
            },

        'KLS':
            {
                'FPS': 23.976,
                'Handles': 10,
                'Resolution': (4096, 2160),
                'Final': 'dpx',
                'Offset': False,  # Setting the handles offset
                'Start': 1001,
                'Project': 'KLS',
            },
    }