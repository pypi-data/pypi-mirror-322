import setuptools
from wheel.bdist_wheel import bdist_wheel as bdist_wheel_orig


class bdist_wheel(bdist_wheel_orig):
    def get_tag(self):
        # 返回 (python tag, abi tag, platform tag)
        return ('cp36', 'cp36m', 'win_amd64')


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

package_data = {
    'tessng': ['*.pyd', '*.pyi', '*.dll', '*.pdb', '*.exe']
}

setuptools.setup(
    name="tessng",
    version="4.0.0",
    author="Jida",
    author_email="17315487709@163.com",
    description="tessng with python3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    cmdclass={'bdist_wheel': bdist_wheel},
    install_requires=[
        "PySide2==5.15.2.1",
        "shiboken2==5.15.2.1",
    ],
    python_requires='==3.6.*',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    package_data=package_data,
    zip_safe=False,
    include_package_data=True,
)
