# t3: LO inclusive pp -> E+ E- at m = 500 GeV (CT18NLO, mu = sqrt(s-hat), G_mu inputs), 1000 events.  Script added by the
# fixer (review S2-R1 B7b): the original 2026-10-11 run was `generate_events -f probe_m500` typed in mg_out/probe_E_incl
# (log t3_E_incl.log, seed offset 23, default param card MXE = 500, aEWM1 = 132.507, Gf = 1.16639e-5).
launch /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/mg_out/probe_E_incl -n rerun_t3_m500
shower=OFF
set MXE 500
set aEWM1 132.507
set Gf 1.16639e-05
set nevents 1000
set iseed 23
done
