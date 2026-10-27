(* make_ufo.wls -- batch generation of the FeynRules cross-check UFO.
   Run: /Applications/Mathematica.app/Contents/MacOS/wolframscript -file make_ufo.wls   (from sim/models/fr/) *)
$FeynRulesPath = Environment["FEYNRULES_PATH"];  (* FeynRules install, e.g. .../feynrules-current *)
here = DirectoryName[$InputFileName];
SetDirectory[$FeynRulesPath];
<< FeynRules`;
SetDirectory[here];
LoadModel[FileNameJoin[{$FeynRulesPath, "Models", "SM", "SM.fr"}], FileNameJoin[{here, "quirkE.fr"}]];
LoadRestriction[FileNameJoin[{$FeynRulesPath, "Models", "SM", "DiagonalCKM.rst"}]];
FeynmanGauge = False;
LE := I xebar.Ga[mu].DC[xe, mu] - MXE xebar.xe;
LS := DC[sxebar, mu] DC[sxe, mu] - MSXE^2 sxebar sxe;
Print["E vertices: ", FeynmanRules[LE]];
Print["S vertices: ", FeynmanRules[LS]];
WriteUFO[LSM + LE + LS, Output -> FileNameJoin[{here, "quirkE_FR_UFO"}]];
Print["DONE"];
