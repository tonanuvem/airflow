FROM comics/centos:7

## Install/Update packages
RUN yum clean all && \
    yum install -y epel-release gcc gcc-c++ && \
    yum install -y python36 python36-libs python36-devel python36-pip && \
    pip3 install pip --upgrade

## Install Airflow
COPY airflow/. /opt/airflow/airflow
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes
RUN cd /opt/airflow && pip3 install apache-airflow==1.10.9

## Install other Airflow dependencies
ENV POSTGRES_USER=test
ENV POSTGRES_PASSWORD=test
ENV POSTGRES_DB=test
# Remove this flask installation when https://issues.apache.org/jira/browse/AIRFLOW-4900
# is fixed upstream. Flask should be installed as a part of Airflow.
# RUN pip3 install flask==1.0.3 && \
RUN pip3 install flask_bcrypt && \
    pip3 install apache-airflow[postgres,docker]


## Add files to configure Airflow for production
COPY dev.cfg /root/airflow/airflow.cfg
COPY entrypoint.sh /root/airflow/
COPY add_superuser.py /root/airflow/
WORKDIR /root/airflow/
RUN mkdir dags
EXPOSE 18080


## Run both webserver and scheduler by default (using supervisord)
RUN pip3 install supervisor
### Create supervisord config
RUN echo "[supervisord]" >> /etc/supervisord.conf && \
    echo "nodaemon=true" >> /etc/supervisord.conf && \
    echo "user=root" >> /etc/supervisord.conf && \
    echo "" >> /etc/supervisord.conf && \
    echo "[program:webserver]" >> /etc/supervisord.conf && \
    echo "command=/usr/local/bin/airflow webserver" >> /etc/supervisord.conf && \
    echo "stdout_logfile=/dev/stdout" >> /etc/supervisord.conf && \
    echo "stdout_logfile_maxbytes=0" >> /etc/supervisord.conf && \
    echo "stderr_logfile=/dev/stderr" >> /etc/supervisord.conf && \
    echo "stderr_logfile_maxbytes=0" >> /etc/supervisord.conf && \
    echo "" >> /etc/supervisord.conf && \
    echo "[program:scheduler]" >> /etc/supervisord.conf && \
    echo "command=/usr/local/bin/airflow scheduler" >> /etc/supervisord.conf && \
    echo "stdout_logfile=/dev/stdout" >> /etc/supervisord.conf && \
    echo "stdout_logfile_maxbytes=0" >> /etc/supervisord.conf && \
    echo "stderr_logfile=/dev/stderr" >> /etc/supervisord.conf && \
    echo "stderr_logfile_maxbytes=0" >> /etc/supervisord.conf

COPY ../dags /opt/airflow/dags

ENTRYPOINT ["./entrypoint.sh"]
