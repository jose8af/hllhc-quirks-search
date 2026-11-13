convert model @SIM@/models/fr/quirkE_FR_UFO
import model @SIM@/models/fr/quirkE_FR_UFO
define p = g u d s u~ d~ s~
generate p p > xe+ xe-
output @SIM@/mg_out/xcheck_FR_E -nojpeg
generate p p > sxe+ sxe-
output @SIM@/mg_out/xcheck_FR_S -nojpeg
import model @SIM@/models/quirkE
define p = g u d s u~ d~ s~
generate p p > xe+ xe-
output @SIM@/mg_out/xcheck_HW_E -nojpeg
generate p p > sxe+ sxe-
output @SIM@/mg_out/xcheck_HW_S -nojpeg
exit
