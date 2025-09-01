from setuptools import find_packages
from setuptools import setup

package_name = 'go2_cli'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
    ],
    install_requires=['ros2cli'],
    zip_safe=True,
    author='Juan Carlos Manzanares Serrano',
    author_email='juancarlos.serrano@urjc.es',
    maintainer='Juan Carlos Manzanares Serrano',
    maintainer_email='juancarlos.serrano@urjc.es',
    keywords=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    description='Command line tools for Go2 robot.',
    long_description="""\
The package provides the go2 commands.""",
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'ros2cli.command': [
            'go2 = go2_cli.command.go2:Go2Command',
        ],
        'ros2cli.extension_point': [
            'go2.verb = go2_cli.verb:VerbExtension',
        ],
        'go2.verb': [
            'service = go2_cli.verb.service:ServiceVerb',
            'tts = go2_cli.verb.tts:TTSVerb',
            'obstacles_avoidance = go2_cli.verb.switch_obstacles_avoidance:SwitchObstaclesAvoidanceVerb',
            'vui = go2_cli.verb.vui:VUIVerb',
            'foot_raise_height = go2_cli.verb.foot_raise_height:FootRaiseHeightVerb',
            'body_height = go2_cli.verb.body_height:BodyHeightVerb',
        ],
    }
)
