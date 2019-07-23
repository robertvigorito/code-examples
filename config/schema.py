from config.api import drive

client = \
    [
        'internal',
        'client',
    ]

color = \
    [
        'clds',
        'luts',
    ]

prod = \
    [
        'documents',
        'from_client',
        'thumbnails',
    ]

edit = \
    [
        'turnover',
        'audio',
        'camera_footage',
        'edits',
        'output',
        'prep',
    ]

tracking = \
    [
        'exports',
        'setup',
        'sources',
    ]

nuke = \
    {
        '{shot_code}':
            [
                'comp/scripts',
                'comps/scripts',
                'precomp',
                'elements',
                'tracks',
                'luts',
            ]
    }

comp = \
    {
        'tracking': tracking,
        '_dailies': None,
        'aftereffects': None,
        'flame': 'setups',
        'nuke': nuke,
        'roto': tracking,
    }

project = \
    {
        '{project}':
            {
                '{episode}':
                    {
                        'assets': client,
                        'breakout': None,
                        'color': color,
                        'posting': 'client',
                        'prod': prod,
                        'refs': None,
                        'edit': edit,
                        'comp': comp,
                    },
            }
    }

server = \
    {
        drive():
            {
                'JOBS': project,
                'users': None,
                '.pipeline': None,
                'tools': None,
                '1pt1': 'Elements'
            }
    }
