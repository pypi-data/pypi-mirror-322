from setuptools import setup, find_packages  


setup(  
    name             = 'SPIKES_TO_US_IN',  
    version          = '0.0.0.1',  
    description      = 'SKKU ISRI Pose Estimation',  
    author           = 'sjhyeon1222',  
    author_email     = 'sjhyeon1222@gmail.com',  
    url              = '',  
    download_url     = '',  
    install_requires = [  
        'requests',  
        'beautifulsoup4',  
        'clipboard',  
        'Markdown',  
        'aiohttp'  
    ],  
   include_package_data=True,  
   packages         = find_packages(),  
    entry_points     = {  
        'console_scripts': [  
            'get_pose = SPIKES_TO_US_IN.pf_pose:run'  
        ]  
    },  
    keywords         = [ 
    ],  
    python_requires  = '>=3',  
    zip_safe=False,  
    classifiers      = [  
        "Programming Language :: Python :: 3.11",  
        "License :: OSI Approved :: MIT License",  
        "Operating System :: Microsoft :: Windows"  
    ]  
)