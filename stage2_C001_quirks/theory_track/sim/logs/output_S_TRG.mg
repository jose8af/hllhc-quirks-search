import model /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/models/quirkE-no_b_mass
define p = p b b~
define j = j b b~
generate p p > sxe+ sxe- @0
add process p p > sxe+ sxe- j @1
add process p p > sxe+ sxe- j j @2
output /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/mg_out/prod_S_TRG -nojpeg
exit
