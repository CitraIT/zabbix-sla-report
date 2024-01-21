FROM ubuntu:20.04

# TZ
ENV PATH="/scripts:${PATH}"
ENV TZ America/Sao_Paulo
RUN echo $TZ > /etc/timezone
ENV DEBIAN_FRONTEND noninteractive


# Atualizando a lista de pacotes
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update \
	&& apt-get -y dist-upgrade \
	&& apt-get -y install --no-install-recommends \
		python3.8 \
		python3-pip 


# Installing Python Requirements
RUN mkdir /app
COPY requirements.txt /app/requirements.txt
RUN python3 -m pip install -U pip
RUN python3 -m pip install -r /app/requirements.txt


# Cleanup package cache data
RUN rm -rf /var/lib/apt/lists/*


# Copiando os arquivos da aplicação
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY . /app
WORKDIR /app


# Expondo a porta 8000
EXPOSE 80

CMD ["/entrypoint.sh"]
