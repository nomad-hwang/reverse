FROM python:3.10-slim-bullseye

RUN apt update && apt install openssh-server -y  && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m laborange -s /bin/false
RUN echo 'laborange:admin' | chpasswd

# add ssh key
RUN mkdir /home/laborange/.ssh -p
RUN echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIG7PbJK66Ine7pi3BioF+O+h/vho6Bm6QU/19qO6lp2t nomad.hwang@gmail.com" > /home/laborange/.ssh/authorized_keys
RUN service ssh start

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]

