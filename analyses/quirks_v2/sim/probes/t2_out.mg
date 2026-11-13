import model @SIM@/models/quirkE-no_b_mass
define p = p b b~
define j = j b b~
generate p p > xe+ xe-
output @SIM@/mg_out/probe_E_incl -nojpeg
generate p p > sxe+ sxe-
output @SIM@/mg_out/probe_S_incl -nojpeg
generate p p > xe+ xe- @0
add process p p > xe+ xe- j @1
add process p p > xe+ xe- j j @2
output @SIM@/mg_out/probe_E_mlm -nojpeg
exit
