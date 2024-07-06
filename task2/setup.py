from setuptools import find_packages, setup

package_name = 'task2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shouryadeep',
    maintainer_email='shouryadeep@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['publisher_node=task2.camerapublisher:main',
        'suscriber_node=task2.SubscriberImage:main',
        'ball_detacting=task2.ball_detecting:main',
        'turtle_controler=task2.turtle_controler:main'
        ],
    },
)
