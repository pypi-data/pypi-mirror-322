from setuptools import setup, find_packages

readme = open('README.md','r')

from setuptools import setup, find_packages

# Leer el archivo README.md para la descripción larga del paquete
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='py.business_intelligence',  # Nombre del paquete
    version='0.1.1',  # Versión del paquete
    description='Paquete orientado al Business Intelligence',  # Breve descripción
    long_description=long_description,  # Descripción larga desde README.md
    long_description_content_type='text/markdown',  # Tipo de contenido de la descripción larga
    author='Alejandro Yegros Schmidt',  # Autor
    author_email='alejandro_aug@hotmail.com',  # Email del autor
    url='https://github.com/AlejandroYegrosSchmidt/py.business_intelligence',  # URL del repositorio
    download_url='https://github.com/AlejandroYegrosSchmidt/py.business_intelligence/tarball/0.1',  # URL de descarga
    packages=find_packages(where='src'),  # Buscar paquetes dentro de 'src'
    package_dir={'': 'src'},  # Directorio raíz del paquete
    install_requires=[
        'pandas',  # Dependencias necesarias
    ],
    keywords=['business intelligence', 'elasticidad de la demanda', 'elastic demand'],  # Palabras clave
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],  # Clasificación del paquete para PyPI
    license='MIT',  # Licencia
    include_package_data=True,  # Incluir archivos adicionales especificados en MANIFEST.in
    python_requires='>=3.6',  # Versión mínima de Python requerida
)
