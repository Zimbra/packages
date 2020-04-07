FROM zimbra/zm-base-os:devcore-ubuntu-18.04

COPY zimbra.list /etc/apt/sources.list.d/zimbra.list

USER root

RUN \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5234D2B73B6996C7 && \
    apt-get update && \
    apt-get install -yqq libpcre3-dev libz-dev

USER build
