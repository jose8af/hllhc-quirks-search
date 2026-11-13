# Source this in every shell, job and pod of the quirks v2 study:  . /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
# Same absolute paths on every node and in every pod (brief 5.2). No sudo, nothing outside the allowed areas.
export REPO=/home/users/jdochoa/hllhc-quirks-search
export QV2=$REPO/analyses/quirks_v2
export QV2_DATA=/nfs/cajuela/jdochoa/quirks_v2/data
export QV2_LOGS=/nfs/cajuela/jdochoa/quirks_v2/logs
export QV2_SW=/home/users/jdochoa/sw
export QV2_SCRATCH=/home/scratch/jdochoa
export PIXI_HOME=/home/users/jdochoa/.pixi
export PIXI_CACHE_DIR=/home/users/jdochoa/.cache/rattler
export PIXI_NO_PATH_UPDATE=1
export DO_NOT_TRACK=1 PIXI_NO_TELEMETRY=1
case ":$PATH:" in *":$PIXI_HOME/bin:"*) ;; *) export PATH="$PIXI_HOME/bin:$PATH";; esac
umask 022
