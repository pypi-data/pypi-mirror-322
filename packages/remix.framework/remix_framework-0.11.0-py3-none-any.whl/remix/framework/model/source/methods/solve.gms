* SPDX-FileCopyrightText: Copyright (c) 2023-2024 German Aerospace Center (DLR)
* SPDX-License-Identifier: BSD-3-Clause

$onVerbatim
$iftheni.method %method%==solve
$offVerbatim

$include "%sourcedir%/solver_options/defaults.gms"
$include "%sourcedir%/solver_options/write.gms"


* ==== solve the problem ====

loop ( optiframeToCalc,
    yearsSel(years) = no;
    yearsSel(years)$map_optiframe(optiframeToCalc,years) = yes;
    yearsToFix(years) = no;
    yearsToFix(years)$(years.val < smin(years_a$yearsSel(years_a), years_a.val)) = yes;
    accYearsSel(accYears) = no;
    accYearsSel("horizon") = yes;
    accYearsSel(accYears)$(sum(yearsSel$sameas(accYears,yearsSel), 1)) = yes;
    accYearsToFix(accYears) = no;
    accYearsToFix(accYears)$(sum(years$(sameas(years,accYears) and years.val < smin(years_a$yearsSel(years_a), years_a.val)), 1) > 0) = yes;
    timeModelSel(timeModel) = no;
    timeModelSel(timeModel)$timeModelToCalc(timeModel) = yes;
    nodesModelSel(nodesModel) = no;
    nodesModelSel(nodesModel)$nodesModelToCalc(nodesModel) = yes;

* Fix decision for years previously optimized in case of myopic or foresight
    converter_unitsDelta(nodesModelToCalc,yearsToFix,converter_techs)
        $(sum(yearsToCalc$sameas(yearsToFix, yearsToCalc), 1))
        = sum(vintage, converter_unitsTotal.l(nodesModelToCalc,yearsToFix,converter_techs,vintage))
            - converter_capacityParam(nodesModelToCalc,yearsToFix,converter_techs,"unitsUpperLimit");
    converter_unitsDelta(nodesModelToCalc,yearsToFix,converter_techs)
        $(converter_unitsDelta(nodesModelToCalc,yearsToFix,converter_techs) < 0) = 0;

    converter_unitsBuild.l(nodesModelToCalc,yearsToFix,converter_techs,vintage)
        $converter_availTech(nodesModelToCalc,yearsToFix,converter_techs,vintage)
        = converter_unitsBuild.l(nodesModelToCalc,yearsToFix,converter_techs,vintage)
            - converter_unitsDelta(nodesModelToCalc,yearsToFix,converter_techs);

    converter_unitsBuild.l(nodesModelToCalc,yearsToFix,converter_techs,vintage)
        $(converter_unitsBuild.l(nodesModelToCalc,yearsToFix,converter_techs,vintage) < 0) = 0;
    converter_unitsBuild.fx(nodesModelToCalc,yearsToFix,converter_techs,vintage)
        = converter_unitsBuild.l(nodesModelToCalc,yearsToFix,converter_techs,vintage);
    converter_unitsDecom.l(nodesModelToCalc,yearsToFix,converter_techs,vintage)
        $(converter_unitsDecom.l(nodesModelToCalc,yearsToFix,converter_techs,vintage) < 0) = 0;
    converter_unitsDecom.fx(nodesModelToCalc,yearsToFix,converter_techs,vintage)
        = converter_unitsDecom.l(nodesModelToCalc,yearsToFix,converter_techs,vintage);
    converter_unitsTotal.fx(nodesModelToCalc,yearsToFix,converter_techs,vintage)
        = converter_unitsTotal.l(nodesModelToCalc,yearsToFix,converter_techs,vintage);


    storage_unitsDelta(nodesModelToCalc,yearsToFix,storage_techs)
        $(sum(yearsToCalc$sameas(yearsToFix, yearsToCalc), 1))
        = sum(vintage, storage_unitsTotal.l(nodesModelToCalc,yearsToFix,storage_techs,vintage))
            - storage_reservoirParam(nodesModelToCalc,yearsToFix,storage_techs,"unitsUpperLimit");
    storage_unitsDelta(nodesModelToCalc,yearsToFix,storage_techs)
        $(storage_unitsDelta(nodesModelToCalc,yearsToFix,storage_techs) < 0) = 0;

    storage_unitsBuild.l(nodesModelToCalc,yearsToFix,storage_techs,vintage)
        $storage_availTech(nodesModelToCalc,yearsToFix,storage_techs,vintage)
        = storage_unitsBuild.l(nodesModelToCalc,yearsToFix,storage_techs,vintage)
            - storage_unitsDelta(nodesModelToCalc,yearsToFix,storage_techs);

    storage_unitsBuild.l(nodesModelToCalc,yearsToFix,storage_techs,vintage)
        $(storage_unitsBuild.l(nodesModelToCalc,yearsToFix,storage_techs,vintage) < 0) = 0;
    storage_unitsBuild.fx(nodesModelToCalc,yearsToFix,storage_techs,vintage)
        = storage_unitsBuild.l(nodesModelToCalc,yearsToFix,storage_techs,vintage);
    storage_unitsDecom.l(nodesModelToCalc,yearsToFix,storage_techs,vintage)
        $(storage_unitsDecom.l(nodesModelToCalc,yearsToFix,storage_techs,vintage) < 0) = 0;
    storage_unitsDecom.fx(nodesModelToCalc,yearsToFix,storage_techs,vintage)
        = storage_unitsDecom.l(nodesModelToCalc,yearsToFix,storage_techs,vintage);
    storage_unitsTotal.fx(nodesModelToCalc,yearsToFix,storage_techs,vintage)
        = storage_unitsTotal.l(nodesModelToCalc,yearsToFix,storage_techs,vintage);


    transfer_linksDelta(linksModelToCalc,yearsToFix,transfer_techs)
        $(sum(yearsToCalc$sameas(yearsToFix, yearsToCalc), 1))
        = sum(vintage, transfer_linksTotal.l(linksModelToCalc,yearsToFix,transfer_techs,vintage))
            - transfer_linksParam(linksModelToCalc,yearsToFix,transfer_techs,"linksUpperLimit");
    transfer_linksDelta(linksModelToCalc,yearsToFix,transfer_techs)
        $(transfer_linksDelta(linksModelToCalc,yearsToFix,transfer_techs) < 0) = 0;

    transfer_linksBuild.l(linksModelToCalc,yearsToFix,transfer_techs,vintage)
        $transfer_availTech(linksModelToCalc,yearsToFix,transfer_techs,vintage)
        = transfer_linksBuild.l(linksModelToCalc,yearsToFix,transfer_techs,vintage)
            - transfer_linksDelta(linksModelToCalc,yearsToFix,transfer_techs);

    transfer_linksBuild.l(linksModelToCalc,yearsToFix,transfer_techs,vintage)
        $(transfer_linksBuild.l(linksModelToCalc,yearsToFix,transfer_techs,vintage) < 0) = 0;
    transfer_linksBuild.fx(linksModelToCalc,yearsToFix,transfer_techs,vintage)
        = transfer_linksBuild.l(linksModelToCalc,yearsToFix,transfer_techs,vintage);
    transfer_linksDecom.l(linksModelToCalc,yearsToFix,transfer_techs,vintage)
        $(transfer_linksDecom.l(linksModelToCalc,yearsToFix,transfer_techs,vintage) < 0) = 0;
    transfer_linksDecom.fx(linksModelToCalc,yearsToFix,transfer_techs,vintage)
        = transfer_linksDecom.l(linksModelToCalc,yearsToFix,transfer_techs,vintage);
    transfer_linksTotal.fx(linksModelToCalc,yearsToFix,transfer_techs,vintage)
        = transfer_linksTotal.l(linksModelToCalc,yearsToFix,transfer_techs,vintage);

    accounting_indicator.fx(accNodesModel,accYearsToFix,indicator)
        = accounting_indicator.l(accNodesModel,accYearsToFix,indicator);

* Optimize and log values
    if (opti_sense < 0,
    solve remix minimizing accounting_objective using mip;
    else
    solve remix maximizing accounting_objective using mip;
    );

    put_utility 'log' / 'Model status ' remix.modelstat:0:0;
    put_utility 'log' / 'Objective value ' accounting_objective.l:0:3;

);

$onVerbatim
$endif.method
$offVerbatim
