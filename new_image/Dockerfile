FROM centos:7.2.1511
MAINTAINER moyan
RUN set -ex \
    # 预安装所需组件
    && yum install -y wget tar libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make initscripts \
    && wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz \
    && tar -zxvf Python-3.5.0.tgz \
    && cd Python-3.5.0 \
    && ./configure prefix=/usr/local/python3 \
    && make \
    && make install \
    && make clean \
    && rm -rf /Python-3.5.0* \
    && yum install -y epel-release \
    && yum install -y python-pip
RUN mv /usr/bin/python /usr/bin/python27 && mv /usr/bin/pip /usr/bin/pip-python2.7
RUN ln -s /usr/local/python3/bin/python3.5 /usr/bin/python
RUN ln -s /usr/local/python3/bin/pip3 /usr/bin/pip
RUN sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/bin/yum 
RUN sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/libexec/urlgrabber-ext-down
RUN yum install -y deltarpm  
RUN rpm --rebuilddb && yum install -y perl
RUN rpm --rebuilddb && yum install -y glibc-headers gcc-c++

#download and build openmpi 
RUN mkdir /build/
ADD openmpi-4.0.1.tar.gz /build/
RUN cd /build/openmpi-4.0.1 && ./configure &&  make && make install
RUN cd /build && wget https://bitbucket.org/mpi4py/mpi4py/downloads/mpi4py-3.0.2.tar.gz \
  && tar xvzf mpi4py-3.0.2.tar.gz
RUN cd /build/mpi4py-3.0.2 && python setup.py build && python setup.py install
ADD tini /tini
RUN chmod +x /tini

RUN touch /var/lib/rpm/* && \
    yum  -y install openssh openssh-clients openssh-server openssl-devel && \
    yum clean all

RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key && \
    ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
ADD sshd /root/.ssh
RUN chmod -R 600 /root/.ssh/
ADD sshd/ssh_config /etc/ssh/ssh_config
ADD sshd/sshd_config /etc/ssh/sshd_config

RUN echo 'root:root' | chpasswd

ENV LC_ALL en_US.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

VOLUME /var/lib/docker
VOLUME /home/jenkins
EXPOSE 22
ENTRYPOINT ["/tini", "--"]
CMD ["/usr/sbin/sshd", "-D"]

 

