FROM python:3.6.6

RUN groupadd -r maker && useradd --no-log-init -r -g maker maker

COPY bin /opt/maker/d3m-keeper/bin
COPY lib /opt/maker/d3m-keeper/lib
COPY drip_keeper /opt/maker/d3m-keeper/d3m_keeper
COPY install.sh /opt/maker/d3m-keeper/install.sh
COPY requirements.txt /opt/maker/d3m-keeper/requirements.txt

WORKDIR /opt/maker/d3m-keeper
RUN pip3 install virtualenv
RUN ./install.sh
WORKDIR /opt/maker/d3m-keeper/bin

USER maker
