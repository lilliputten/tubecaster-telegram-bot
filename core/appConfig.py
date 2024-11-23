import os
from dotenv import dotenv_values

#  import json

appConfig = {
    **dotenv_values('.env'),  # load shared development variables
    **dotenv_values('.env.local'),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

#  debugAppConfig = json.dumps(appConfig, indent=2)
#  print('Config: %s' % debugAppConfig)

# Module exports...
__all__ = [
    'appConfig',
]

if __name__ == '__main__':
    test = appConfig.get('DOMAIN')
    print('main %s' % test)
