from setuptools import setup, find_packages

setup(
    name="p4cm_web",
    version="0.0.1",
    license='BSD',
    description="POC: p4cm as web service oriented application.",
    author='Eric.Qu',
    author_email='eric.qu@nagra.com',
    packages=find_packages('.'),
    package_dir={'': '.'},
    include_package_data=True,
    zip_safe=False,
)
