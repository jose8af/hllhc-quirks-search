# t4: LO inclusive E/Etilde at 200/500/1000 (E 500 = t3), MG default G_mu inputs set explicitly (review S2-R1 B7a)
launch @SIM@/mg_out/probe_E_incl -n E_m200
shower=OFF
set MXE 200
set aEWM1 132.507
set Gf 1.16639e-05
done
launch @SIM@/mg_out/probe_E_incl -n E_m1000
shower=OFF
set MXE 1000
set aEWM1 132.507
set Gf 1.16639e-05
done
launch @SIM@/mg_out/probe_S_incl -n S_m200
shower=OFF
set MSXE 200
set aEWM1 132.507
set Gf 1.16639e-05
done
launch @SIM@/mg_out/probe_S_incl -n S_m500
shower=OFF
set MSXE 500
set aEWM1 132.507
set Gf 1.16639e-05
done
launch @SIM@/mg_out/probe_S_incl -n S_m1000
shower=OFF
set MSXE 1000
set aEWM1 132.507
set Gf 1.16639e-05
done
