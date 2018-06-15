FROM python:3.5

# Configura el modo no interactivo.
ENV DEBIAN_FRONTEND noninteractive

# Crea el directorio '/code' y lo establece como directorio de trabajo.
RUN mkdir /code
WORKDIR /code

# Instala las dependencias del proyecto, mediante pip.
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# Añade el contenido del repositorio al directorio '/code'.
ADD . /code/

# Instala NodeJS.
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

# Instala Bower.
RUN npm install -g bower

# Instala las herramientas de cliente de PostgreSQL.
RUN apt-get install -y postgresql-client
