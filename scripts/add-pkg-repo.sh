#/bin/bash
set -e

function main() {
    echo -e "Adding Zimbra repository ..."

    sudo apt-get install -y -qq apt-transport-https

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9BE6ED79

    sudo tee -a /etc/apt/sources.list.d/zimbra.list > /dev/null <<END
deb [arch=amd64] https://repo.zimbra.com/apt/87 $(lsb_release -cs) zimbra
deb [arch=amd64] https://repo.zimbra.com/apt/90 $(lsb_release -cs) zimbra
deb-src [arch=amd64] https://repo.zimbra.com/apt/87 $(lsb_release -cs) zimbra
deb [arch=amd64] https://repo.zimbra.com/apt/90-ne $(lsb_release -cs) zimbra
END

    sudo apt-get update -y -qq
}

main "$@"