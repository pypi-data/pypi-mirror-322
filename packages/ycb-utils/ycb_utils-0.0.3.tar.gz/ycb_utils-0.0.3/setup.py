from setuptools import find_packages, setup

install_requires = ["trimesh"]

setup(
    name="ycb_utils",
    version="0.0.3",
    description="ycb utils",
    author="Hirokazu Ishida",
    author_email="h-ishida@jsk.imi.i.u-tokyo.ac.jp",
    license="MIT",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True
)
