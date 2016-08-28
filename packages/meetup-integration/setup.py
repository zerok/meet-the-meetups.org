from setuptools import setup

setup(
    name='lektor-meetup-integration',
    version='0.1',
    author=u'Horst Gutmann',
    author_email='horst@zerokspot.com',
    license='MIT',
    py_modules=['lektor_meetup_integration'],
    entry_points={
        'lektor.plugins': [
            'meetup-integration = lektor_meetup_integration:MeetupIntegrationPlugin',
        ]
    }
)
