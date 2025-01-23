from setuptools import setup, find_packages

setup(
 name="team_3_library",
 version="0.1.0",
 license='MIT',
 description="Data set cleaning library",
 long_description=open("README.md").read(),
 long_description_content_type="text/markdown",
 author="Team 3",
 author_email="enarayiyuan.errasti@alumni.mondragon.edu",
 packages=find_packages(), 
 install_requires=['numpy', 'pandas', 'seaborn','matplotlib.pyplot'],
 classifiers=[
 "Programming Language :: Python :: 3",
 "License :: OSI Approved :: MIT License",
 "Operating System :: OS Independent",
 ],
 python_requires=">=3.6",
)