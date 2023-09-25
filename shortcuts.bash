# source me for shortcusts
SR() { systemctl restart $@ ; }
SS() { systemctl status $@ ; }
JF() { journalctl -f ; }
JFU() { journalctl -fu $@ ; }
JXE() { journalctl -xe  ; }
JXEU() { journalctl -xeu $@ ; }
