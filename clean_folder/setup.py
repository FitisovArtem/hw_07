from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='0.0.1',
      description='HW_7 GOIT',
      author='Artem Fitisov',
      author_email='test@example.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={"clean_folder": ["clean_folder = clean_folder.clean:start"]}
      )