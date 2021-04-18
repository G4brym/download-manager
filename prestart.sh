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

  if [[ -v UID ]]; then
    if [[ $UID != 0 ]]; then
      if [[ $UID != $(id -u webapp) ]]; then
        log "Changing uid of webapp to $UID"
        usermod -u $UID webapp
      fi
    else
      runAsUser=root
    fi
  fi

  if [[ -v GID ]]; then
    if [[ $GID != 0 ]]; then
      if [[ $GID != $(id -g webapp) ]]; then
        log "Changing gid of webapp to $GID"
        groupmod -o -g $GID webapp
      fi
    else
      runAsGroup=root
    fi
  fi

  if [[ $(stat -c "%u" /config) != $UID ]]; then
    log "Changing ownership of /config to $UID ..."
    chown -R ${runAsUser}:${runAsGroup} /config
  fi

  if [[ $(stat -c "%u" /downloads) != $UID ]]; then
    log "Changing ownership of /downloads to $UID ..."
    chown -R ${runAsUser}:${runAsGroup} /downloads
  fi

  exec su-exec ${runAsUser}:${runAsGroup} /app/start.sh
else
  exec /app/start.sh
fi
