# -*- coding:utf-8 -*-

import os
from dotenv import dotenv_values


changed = """
@changed 2024.11.24, 10:51
""".strip().replace(
    '@changed ', ''
)


appConfig = {
    **dotenv_values('.env'),
    **dotenv_values('.env.local'),
    **dotenv_values('.env.secure'),
    # NOTE: DEBUG: Testing remote logging configurations
    #  **dotenv_values('.env.logging-ngrok.SAMPLE'),
    #  **dotenv_values('.env.logging-local.SAMPLE'),
    # Override loaded values with environment variables
    **os.environ,
    **{'changed': changed},
}

# Module exports...
__all__ = [
    'appConfig',
]

if __name__ == '__main__':
    test = appConfig.get('DOMAIN')
    print('main %s' % test)
