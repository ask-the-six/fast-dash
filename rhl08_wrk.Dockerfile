FROM redhat/ubi8:latest
COPY unified-supervisord.conf supervisord.conf /etc/supervisord/ 
COPY mc.ini /home/abc/.config/mc/ini 
COPY zsh-in-docker.sh /tmp/zsh-in-docker.sh 
RUN /bin/sh -c 'dnf -y update && \
    dnf install -y sudo jq git curl wget nc bind-utils zip gzip tar acl psmisc && \
    ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    dnf reinstall -y tzdata && \
    useradd -u 8877 -p $(openssl passwd -1 abc) abc && \
    mkdir -p /home/abc && \
    chown -R abc:abc /home/abc && \
    mkdir -p /home/abc/apps && \
    chown -R abc:abc /home/abc/apps && \
    setfacl -m u:abc:rwx /etc'    
# Nix folder and conf
#RUN /bin/sh -c 'echo "------------------------------------------------------ Nix folder and conf" \
#    && mkdir -m 0750 /nix \
#    && chown abc:abc /nix'

# docker systemctl replacement
RUN /bin/sh -c 'echo "------------------------------------------------------ docker systemctl replacement" \
    && wget https://raw.githubusercontent.com/gdraheim/docker-systemctl-replacement/master/files/docker/systemctl3.py -O /usr/local/bin/systemctl \
    && chown abc:abc /usr/local/bin/systemctl'

# Python
RUN /bin/sh -c 'echo "------------------------------------------------------ Python" \
    && dnf install -y python3 \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && pip3 install --upgrade distlib \
    && alternatives --set python /usr/bin/python3 \
    && mkdir -p /usr/bin/pip3.8 \
    && chown abc:abc /usr/bin/pip3.8'
 
# Add abc user to sudo
RUN /bin/sh -c 'echo "------------------------------------------------------ Add abc user to sudo" \
    && usermod -aG wheel abc'

RUN /bin/sh -c 'echo "abc ALL=(ALL) NOPASSWD: ALL " >> /etc/sudoers'
# Nodeenv
RUN /bin/sh -c 'echo "------------------------------------------------------ Nodeenv" \
    && pip install nodeenv \
    && sudo wget https://dl.yarnpkg.com/rpm/yarn.repo -O /etc/dnf.repos.d/yarn.repo \
    && dnf install yarn -y'

# Cron
RUN /bin/sh -c 'echo "------------------------------------------------------ Cron" \
    && dnf install -y cronie cronie-anacron \
    && systemctl enable crond \
    && mkdir -p /var/log/supervisord/ \
    && mkdir -p /var/spool/cron/crontabs \
    && chown -R abc:abc /var/spool/cron/crontabs \
    && chown -R abc:abc /var/log \
    && chmod gu+rw /var/run \
    && chmod gu+s /usr/sbin/crond'  


# Supervisor
RUN /bin/sh -c 'echo "------------------------------------------------------ Supervisor" \
    && pip3 install supervisor==4.2.2 \
    && mkdir -p /etc/supervisord.d/ \
    && mkdir -p /var/log/supervisord/ \
    && chown -R abc:abc /etc/supervisord.d/ \
    && chown -R abc:abc /var/log/supervisord/'

# socat
RUN /bin/sh -c 'echo "------------------------------------------------------ socat" \
    && dnf install -y socat'

# frp
RUN /bin/sh -c 'echo "------------------------------------------------------ frp" \
    && cd /tmp \
    && wget https://github.com/fatedier/frp/releases/download/v0.44.0/frp_0.44.0_linux_amd64.tar.gz \
    && tar xvf frp_0.44.0_linux_amd64.tar.gz \
    && mv frp_0.44.0_linux_amd64 /etc/frp \
    && rm frp_0.44.0_linux_amd64.tar.gz'

#RUN /bin/sh -c 'echo "------------------------------------------------------ timelimit" \
#    && dnf install -y timelimit'
RUN /bin/sh -c '\
  echo "------------------------------------------------------ ZSH root" \
  && HOME=/root \
  && chmod +x /tmp/zsh-in-docker.sh \
  && /tmp/zsh-in-docker.sh \
    -t https://github.com/pascaldevink/spaceship-zsh-theme \
    -a "SPACESHIP_PROMPT_ADD_NEWLINE=\"false\"" \
    -a "SPACESHIP_PROMPT_SEPARATE_LINE=\"false\"" \
    -a "export LS_COLORS=\"$LS_COLORS:ow=1;34:tw=1;34:\"" \
    -a "SPACESHIP_USER_SHOW=\"false\"" \
    -a "SPACESHIP_TIME_SHOW=\"true\"" \
    -a "SPACESHIP_TIME_COLOR=\"grey\"" \
    -a "SPACESHIP_DIR_COLOR=\"cyan\"" \
    -a "SPACESHIP_GIT_SYMBOL=\"⇡\"" \
    -a "SPACESHIP_BATTERY_SHOW=\"false\"" \
    -a "if [[ \$(pwd) != /root ]]; then cd /root; fi" \
    -a "hash -d r=/root" \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-history-substring-search \
    -p https://github.com/zsh-users/zsh-syntax-highlighting \
    -p history-substring-search \
    -p https://github.com/bobthecow/git-flow-completion \
    -a "bindkey \"\$terminfo[kcuu1]\" history-substring-search-up" \
    -a "bindkey \"\$terminfo[kcud1]\" history-substring-search-down" \
  && printf "%s\\n%s\\n" "export ZSH_DISABLE_COMPFIX=true" "$(cat /root/.zshrc)" > /root/.zshrc \
  && mkdir -p /home/project'

# ZSH abc
RUN /bin/sh -c 'echo "------------------------------------------------------ ZSH abc" \
    && HOME=/home/abc \
    && /tmp/zsh-in-docker.sh -t https://github.com/pascaldevink/spaceship-zsh-theme -a "DISABLE_UPDATE_PROMPT=\"true\"" -a "SPACESHIP_PROMPT_ADD_NEWLINE=\"false\"" -a "SPACESHIP_PROMPT_SEPARATE_LINE=\"false\"" -a "export LS_COLORS=\"$LS_COLORS:ow=1;34:tw=1;34:\"" -a "SPACESHIP_USER_SHOW=\"true\"" -a "SPACESHIP_TIME_SHOW=\"true\"" -a "SPACESHIP_TIME_COLOR=\"grey\"" -a "SPACESHIP_DIR_COLOR=\"cyan\"" -a "SPACESHIP_GIT_SYMBOL=\"⇡\"" -a "SPACESHIP_BATTERY_SHOW=\"false\"" -a "if [[ \$(pwd) != /home/project ]]; then cd /home/project; fi" -a "hash -d p=/home/project" -p git -p https://github.com/zsh-users/zsh-autosuggestions -p https://github.com/zsh-users/zsh-completions -p https://github.com/zsh-users/zsh-history-substring-search -p https://github.com/zsh-users/zsh-syntax-highlighting -p history-substring-search -p https://github.com/bobthecow/git-flow-completion -a "bindkey \"\$terminfo[kcuu1]\" history-substring-search-up" -a "bindkey \"\$terminfo[kcud1]\" history-substring-search-down"'

# Cleanup
RUN /bin/sh -c 'rm /tmp/zsh-in-docker.sh \
    && printf "%s\\n%s\\n" "export ZSH_DISABLE_COMPFIX=true" "$(cat /home/abc/.zshrc)" > /home/abc/.zshrc'


# Code editors
RUN /bin/sh -c 'dnf install nano -y'

# File browsers: MC
RUN /bin/sh -c 'echo "------------------------------------------------------ File browsers: MC" \
#    && dnf install -y'

# multitasking in a terminal
#RUN /bin/sh -c 'echo "------------------------------------------------------ multitasking in a terminal" \
#    && dnf install -y tmux'

# Sys monitoring
RUN /bin/sh -c 'echo "------------------------------------------------------ Sys monitoring" \
    && dnf install -y ncdu htop'

# Web-based terminal
RUN echo "------------------------------------------------------ Web-based terminal"     \
    && cd /tmp      \
    && wget https://github.com/tsl0922/ttyd/releases/download/1.7.1/ttyd.x86_64     \
    && mv ttyd.x86_64 /usr/bin/ttyd     \
    && chmod +x /usr/bin/ttyd 

# User
RUN echo "------------------------------------------------------ User"     \
    && chown abc:abc /home/project     \
    && mkdir -p /home/abc/bin     \
    && chown abc:abc /home/abc/bin     \
    && mkdir -p /home/abc/.local/bin     \
    && chown abc:abc /home/abc/.local      \
    && chown abc:abc /home/abc/.local/bin     \
    && find /home -type d | xargs -I{} chown -R abc:abc {}     \
    && find /home -type f | xargs -I{} chown abc:abc {} 

# Aliases
RUN echo "------------------------------------------------------ Aliases"     \
    && echo 'alias python="python3"' >> /root/.zshrc     \
    && echo 'alias python="python3"' >> /home/abc/.zshrc 

RUN /bin/sh echo "------------------------------------------------------ Clean"     \
    # Changed from apt-get to dnf clean commands
    && dnf clean all     \
    && rm -rf /var/cache/dnf     \
    && rm -rf /home/abc/.oh-my-zsh/.git     \
    && rm -rf /home/abc/.oh-my-zsh/.github     \
    && rm -rf /home/abc/.oh-my-zsh/custom/plugins/git-flow-completion/.git     \
    && rm -rf /home/abc/.oh-my-zsh/custom/plugins/zsh-autosuggestions/.git     \
    && rm -rf /home/abc/.oh-my-zsh/custom/plugins/zsh-completions/.git     \
    && rm -rf /home/abc/.oh-my-zsh/custom/plugins/zsh-history-substring-search/.git     \
    && rm -rf /home/abc/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting/.git     \
    && rm -rf /home/abc/.oh-my-zsh/custom/themes/spaceship-zsh-theme/.git
USER abc
### Set up git credential helper
RUN git config --global credential.helper cache
##
### Install Nix package manager
##RUN echo "------------------------------------------------------ Nix" && \
#    curl -L https://nixos.org/nix/install > /tmp/nix.sh && \
#    chmod +x /tmp/nix.sh && \
#    sh /tmp/nix.sh --no-daemon && \
#    rm /tmp/nix.sh

### Install Pipx and Python virtual environment
RUN echo "------------------------------------------------------ Pipx" && \
    dnf install -y python3.10 && \
    python3 -m pip install --user pipx && \
    python3 -m pipx ensurepath

# Update PATH
ENV PATH=/home/abc/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PATH=/home/abc/.local/bin:/home/abc/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PATH=/home/abc/.nix-profile/bin:/home/abc/.local/bin:/home/abc/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Install packages and perform actions after PATH updates
RUN echo "------------------------------------------------------ after PATH updates" && \
    pipx install rich-cli && \
    echo 'alias p="rich"' >> /home/abc/.zshrc && \
    nix-env -iA cachix -f https://cachix.org/api/v1/install && \
    echo "------------------------------------------------------ asdf" && \
    git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.11.3 && \
    rm -rf /home/abc/.asdf/.git && \
    echo '. "$HOME/.asdf/asdf.sh"' >> ~/.zshrc && \
    echo 'fpath=(${ASDF_DIR}/completions $fpath)' >> ~/.zshrc && \
    echo 'autoload -Uz compinit && compinit' >> ~/.zshrc

# Define entrypoint
RUN echo 'ENTRYPOINT ["/bin/sh" "-c" "/etc/init.d/cron start; supervisord -c \"/etc/supervisord/unified-supervisord.conf\""]'
