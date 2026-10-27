convert model /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/models/fr/quirkE_FR_UFO
import model /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/models/fr/quirkE_FR_UFO
define p = g u d s u~ d~ s~
generate p p > xe+ xe-
output /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/mg_out/xcheck_FR_E -nojpeg
generate p p > sxe+ sxe-
output /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/mg_out/xcheck_FR_S -nojpeg
import model /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/models/quirkE
define p = g u d s u~ d~ s~
generate p p > xe+ xe-
output /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/mg_out/xcheck_HW_E -nojpeg
generate p p > sxe+ sxe-
output /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/mg_out/xcheck_HW_S -nojpeg
exit
