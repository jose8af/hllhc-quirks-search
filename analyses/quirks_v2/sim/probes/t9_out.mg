import model @SIM@/models/quirkE-no_b_mass
define p = p b b~
define j = j b b~
generate p p > xe+ xe- @0
add process p p > xe+ xe- j @1
add process p p > xe+ xe- j j @2
output @SIM@/mg_out/probe_E_mlm_pt80 -nojpeg
exit
