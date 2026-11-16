#!/bin/bash
# queue_install.sh -- wait until channel (i)'s rho = 2 jobs have left maxwell and it is 13:30 or later, check that no
# pixi install runs on any worker, then run install_herwig_local.sh once (channel (ii), install slot held).
set -u
H=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/herwig
echo "$(date '+%F %T %z') queued"
while [ "$(date +%H%M)" -lt 1330 ] || ls -d /home/scratch/jdochoa/d0pu2* >/dev/null 2>&1; do sleep 60; done
for n in landau maxwell schrodinger; do
  if ssh -x -o BatchMode=yes $n "pgrep -af 'pixi (install|add)' | grep -v pgrep" | grep -q pixi; then
    echo "$(date '+%F %T %z') another pixi install runs on $n: abort"; exit 3; fi
done
echo "$(date '+%F %T %z') start install"
bash "$H/install_herwig_local.sh"
echo "$(date '+%F %T %z') install script exit $?"
