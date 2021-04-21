#!/bin/bash

umask 0002
chmod g+w /config
chmod g+w /downloads

function isTrue() {
  local value=${1,,}

  result=

  case ${value} in
  true | on)
    result=0
    ;;
  *)
    result=1
    ;;
  esac

  return ${result}
}

function log() {
  echo "[init] $*"
}

if ! isTrue "${SKIP_SUDO:-false}" && [ $(id -u) = 0 ]; then
  runAsUser=webapp
  runAsGroup=webapp

  if [[ -v PUID ]]; then
    if [[ $PUID != 0 ]]; then
      if [[ $PUID != $(id -u webapp) ]]; then
        log "Changing uid of webapp to $PUID"
        usermod -u $PUID webapp
      fi
    else
      runAsUser=root
    fi
  fi

  if [[ -v PGID ]]; then
    if [[ $PGID != 0 ]]; then
      if [[ $PGID != $(id -g webapp) ]]; then
        log "Changing gid of webapp to $PGID"
        groupmod -o -g $PGID webapp
      fi
    else
      runAsGroup=root
    fi
  fi

  if [[ $(stat -c "%u" /config) != $PUID ]]; then
    log "Changing ownership of /config to $PUID ..."
    chown -R ${runAsUser}:${runAsGroup} /config
  fi

  if [[ $(stat -c "%u" /downloads) != $PUID ]]; then
    log "Changing ownership of /downloads to $PUID ..."
    chown -R ${runAsUser}:${runAsGroup} /downloads
  fi

  exec su-exec ${runAsUser}:${runAsGroup} /app/start.sh
else
  exec /app/start.sh
fi
