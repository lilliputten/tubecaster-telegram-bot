# -*- coding:utf-8 -*-

import os
from dotenv import dotenv_values

#  import json

changed = """
@changed 2024.11.24, 10:51
""".strip().replace(
    '@changed ', ''
)


appConfig = {
    **dotenv_values('.env'),
    **dotenv_values('.env.local'),
    **dotenv_values('.env.secure'),
    **os.environ,  # override loaded values with environment variables
    **{'changed': changed},
}

#  YT_COOKIE = appConfig.get('YT_COOKIE')
#  print('YT_COOKIE:', YT_COOKIE)

#  debugAppConfig = json.dumps(appConfig, indent=2)
#  print('Config: %s' % debugAppConfig)

# Module exports...
__all__ = [
    'appConfig',
]

if __name__ == '__main__':
    test = appConfig.get('DOMAIN')
    print('main %s' % test)
