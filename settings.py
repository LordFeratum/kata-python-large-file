from os import environ


settings = {
    'amazon': {
        'url': environ.get('AMAZONS3_URL')
    }
}
