from setuptools import setup, find_packages  


setup(  
    name             = 'SPIKES_TO_US_IN',  
    version          = '0.0.0.7',  
    description      = 'SKKU ISRI Pose Estimation',  
    author           = 'sjhyeon1222',  
    author_email     = 'sjhyeon1222@gmail.com',  
    url              = '',  
    download_url     = '',  
    install_requires = [  
        'numpy==1.23.0',
        'ipykernel==6.20.1',
        'open3d==0.16.0',
        'scipy==1.10.0',
        'torch==1.12.1',
        'torchaudio==0.12.1',
        'torchvision==0.13.1',
        'tqdm==4.64.1',
        'pytorch-lightning==1.1.7',
        'torch-optimizer==0.3.0',
        'pyod==1.1.3',
    ],  
   include_package_data=True,  
   packages         = find_packages(),  
    entry_points     = {  
        'console_scripts': [ 
        ]  
    },  
    keywords         = [ 
    ],  
    python_requires  = '>=3',  
    zip_safe=False,  
    classifiers      = [  
        "Programming Language :: Python :: 3.6",  
        "License :: OSI Approved :: MIT License",  
        "Operating System :: Microsoft :: Windows"  
    ]  
)