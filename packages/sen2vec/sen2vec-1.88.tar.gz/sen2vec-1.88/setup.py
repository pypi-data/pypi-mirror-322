#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
import setuptools


setup(
    name='sen2vec',
    version='1.88',
    description='- A sen2vec MODEL that can transform sentence to vector, for Finance mainly, pytorch needed.',
    long_description='- Sen2vec module provides convenient solution to transform sentences to vectors.\n'
                     '- The vectors transformed contain high level of information of the original sentences, \n'
                     '- and this method has a wide range of applications in downstream tasks.\n'
                     '- The method could be directly applied to NLP tasks, \n'
                     '- as well as other machine learning assignments, integrated with any structured data.\n'
                     '- According to application scenarios, such as the sample size of downstream tasks,\n'
                     '- the dimension of vector extracted by sen2vec varies.\n'
                     '- The vectors transformed are able to carry out the four fundamental operations of arithmetic,\n'
                     '- and could calculate the average, the intersection angle and the distance,\n'
                     '- based on different code instructions of the original information.\n'
                     '- The method sen2vec_fi is currently used to analyze financial texts,\n'
                     '- and will be developed into different versions to meet demands in diverse areas. \n'
                     '- There are two ways to employ sen2vec:\n'
                     '- Use the default models we provide by function sen2vec_download() and sen2vec_fi\n'
                     '- Use the self-defined models: from sen2vec import sen2vec\n'
                     '- For more information: Please contact author.',
    long_description_content_type="text/markdown",
    author='xczcx',
    author_email='2292879219@qq.com',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    # package_dir={'sampled': 'sampled'},
    include_package_data=True,
    package_data={
        'sen2vec': ['sampled/bertwwm_pretrain/*.txt',
                    'sampled/bertwwm_pretrain/*.json',
                    'sampled/bertwwm_pretrain/*.csv',
                    'sampled/*.py',
                    # 'sampled/bertwwm_pretrain/*.bin',
                    # 'sampled/saved_dict/*.ckpt',
                    'sampled/data/*.txt',
                    'models/*.pyd',
                    'models/*.so']
        # 'sampled': ['bertwwm_pretrain/*.json'],
        # 'sampled': ['bertwwm_pretrain/*.txt'],
        # 'sampled': ['bertwwm_pretrain/*.bin'],
        # 'sampled': ['data/*.txt'],
        # 'sampled': ['saved_dict/*.ckpt']
    },
    install_requires=[''],
    python_requires="==3.7",
    # classifiers=[
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Operating System :: OS Independent'
    # ]
)
