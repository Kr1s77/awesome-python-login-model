# coding:utf-8


from setuptools import setup,find_packages

setup(
    name="TSDK",
    version = "0.2",
    install_requires = [
        'requests',
    ],
    packages = find_packages(),
    #packages = ['TSDK'],
    description = "淘宝爬虫SDK",
    long_description = "淘宝爬虫SDK",
    author = 'xinlingqudongX',
    author_email = 'aa@163.com',
    #py_modules = ['mTop'],
    # license = 'GPL',
    # keywords = ('淘宝','SDK','爬虫'),
    # platforms = 'Independant',
    url = 'https://github.com/xinlingqudongX/TSDK',
    #data_files = ['./README.md']
    #include_package_data=True, #不要使用这个
    #package_data = {'':['*.md']}
    #include_package_data=True
)
