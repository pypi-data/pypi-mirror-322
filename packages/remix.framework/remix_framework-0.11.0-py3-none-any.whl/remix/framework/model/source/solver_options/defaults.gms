* SPDX-FileCopyrightText: Copyright (c) 2023-2024 German Aerospace Center (DLR)
* SPDX-License-Identifier: BSD-3-Clause

$onVerbatim

$ifi not "%gams.optdir%"=="" $if not dexist "%gams.optdir%" put_utility 'exec' / 'mkdir -p %gams.optdir%'

* ==== GAMS solver options ====
$if not set solver           $setglobal solver           "cplex"
$if not set solvelink        $setglobal solvelink        0
$if not set optfile          $setglobal optfile          1
$if not set holdfixed        $setglobal holdfixed        1
$if not set equlist          $setglobal equlist          0

* ==== REMix solver defaults ====
$if not set solvermethod     $setglobal solvermethod     1
$if %solvermethod%==0        $setglobal solvermethod     "auto"
$if %solvermethod%==1        $setglobal solvermethod     "barrier"
$if %solvermethod%==2        $setglobal solvermethod     "simplex"

$if not set passproblem      $setglobal passproblem      1
$if %passproblem%==0         $setglobal passproblem      "auto"
$if %passproblem%==1         $setglobal passproblem      "primal"
$if %passproblem%==2         $setglobal passproblem      "dual"

$if not set ordering         $setglobal ordering         1
$if %ordering%==0            $setglobal ordering         "auto"
$if %ordering%==1            $setglobal ordering         "nd"
$if %ordering%==2            $setglobal ordering         "amd"
$if %ordering%==3            $setglobal ordering         "amf"

$if not set scaling          $setglobal scaling          "auto"
$if not set densecol         $setglobal densecol         0
$if not set crossover        $setglobal crossover        0
$if not set threads          $setglobal threads          8
$if not set accuracy         $setglobal accuracy         1e-6
$if not set mipaccuracy      $setglobal mipaccuracy      1e-3
$if not set names            $setglobal names            0
$if not set iis              $setglobal iis              0
$if not set rerun            $setglobal rerun            0


* ==== REMix debug options ====
$ife %debug%<>0              $setglobal solvermethod     "simplex"
$ife %debug%<>0              $setglobal names            1
$ife %debug%<>0              $setglobal iis              1


* ==== setup optimization ====
if ((sum(nodesModelToCalc, 1)>40 or sum(timeModelToCalc, 1)>50) and not %equlist%,
   option limRow=0, limCol=0, solPrint=off;
else
   option limRow=100000, limCol=100000, solPrint=on;
);


* ==== Solver specific default values ====

$iftheni.solver %solver%=="cplex"
$ifi %solvermethod%=="auto"       $setglobal lpmethod 0
$ifi %solvermethod%=="simplex"    $setglobal lpmethod 2
$ifi %solvermethod%=="barrier"    $setglobal lpmethod 4
$ifi %passproblem%=="auto"        $setglobal predual 0
$ifi %passproblem%=="primal"      $setglobal predual -1
$ifi %passproblem%=="dual"        $setglobal predual 1
$ifi %ordering%=="nd"             $setglobal barorder 3
$if set accuracy                  $setglobal barepcomp %accuracy%
$if set mipaccuracy               $setglobal epgap %mipaccuracy%
$ife %crossover%=0                $setglobal solutiontype 2
$ife %densecol%>0                 $setglobal barcolnz %densecol%
$if not set quality               $setglobal quality 1


$elseifi.solver %solver%=="gurobi"
* Gurobi "method" collides with REMix "method"
$ifi %solvermethod%=="auto"       $setglobal gurobimethod -1
$ifi %solvermethod%=="barrier"    $setglobal gurobimethod 2
$ifi %solvermethod%=="simplex"    $setglobal gurobimethod 5
$ifi %passproblem%=="auto"        $setglobal predual -1
$ifi %passproblem%=="primal"      $setglobal predual 0
$ifi %passproblem%=="dual"        $setglobal predual 1
$ifi %ordering%=="nd"             $setglobal barorder 1
$if set accuracy                  $setglobal barconvtol %accuracy%
$if set mipaccuracy               $setglobal mipgap %mipaccuracy%
$ife %densecol%>0                 $setglobal GURO_PAR_BARDENSETHRESH %densecol%


$elseifi.solver %solver%=="copt"
$ifi %solvermethod%=="auto"       $setglobal lpmethod 5
$ifi %solvermethod%=="barrier"    $setglobal lpmethod 2
$ifi %solvermethod%=="simplex"    $setglobal lpmethod 1
$ifi %passproblem%=="auto"        $setglobal dualize -1
$ifi %passproblem%=="primal"      $setglobal dualize 0
$ifi %passproblem%=="dual"        $setglobal dualize 1
$ifi %ordering%=="nd"             $setglobal barorder 1
$if set accuracy                  $setglobal relgap %accuracy%


$elseifi.solver %solver%=="xpress"
$ifi %solvermethod%=="barrier"    $setglobal algorithm "barrier"
$ifi %solvermethod%=="simplex"    $setglobal algorithm "simplex"
$ifi %passproblem%=="auto"        $setglobal dualize -1
$ifi %passproblem%=="primal"      $setglobal dualize 0
$ifi %passproblem%=="dual"        $setglobal dualize 1
$ifi %ordering%=="nd"             $setglobal barorder 3
$if set accuracy                  $setglobal barGapStop %accuracy%
$if set mipaccuracy               $setglobal mipRelStop %mipaccuracy%


$elseifi.solver %solver%=="highs"
$ifi %solvermethod%=="auto"       $setglobal highssolver "choose"
$ifi %solvermethod%=="barrier"    $setglobal highssolver "ipm"
$ifi %solvermethod%=="simplex"    $setglobal highssolver "simplex"
$ifi %solvermethod%=="pdlp"       $setglobal highssolver "pdlp"
$ifi %solvermethod%=="choose"     $setglobal highssolver "choose"
$ifi %solvermethod%=="ipm"        $setglobal highssolver "ipm"


$elseifi.solver %solver%=="mosek"
$ifi %solvermethod%=="auto"       $setglobal MSK_IPAR_OPTIMIZER "MSK_OPTIMIZER_FREE"
$ifi %solvermethod%=="barrier"    $setglobal MSK_IPAR_OPTIMIZER "MSK_OPTIMIZER_INTPNT"
$ifi %solvermethod%=="barrier"    $setglobal MSK_IPAR_OPTIMIZER "MSK_IPAR_MIO_ROOT_OPTIMIZER"
$ifi %solvermethod%=="simplex"    $setglobal MSK_IPAR_OPTIMIZER "MSK_OPTIMIZER_FREE_SIMPLEX"
$ifi %passproblem%=="auto"        $setglobal MSK_IPAR_INTPNT_SOLVE_FORM "MSK_SOLVE_FREE"
$ifi %passproblem%=="primal"      $setglobal MSK_IPAR_INTPNT_SOLVE_FORM "MSK_SOLVE_PRIMAL"
$ifi %passproblem%=="dual"        $setglobal MSK_IPAR_INTPNT_SOLVE_FORM "MSK_SOLVE_DUAL"
$ife %presolve%<>0                $setglobal MSK_IPAR_PRESOLVE_USE "MSK_PRESOLVE_MODE_FREE"
$ife %presolve%=0                 $setglobal MSK_IPAR_PRESOLVE_USE "MSK_PRESOLVE_MODE_OFF"
$ife %scaling%=0                  $setglobal MSK_IPAR_INTPNT_SCALING "MSK_SCALING_NONE"
$ife %scaling%<>0                 $setglobal MSK_IPAR_INTPNT_SCALING "MSK_SCALING_FREE"
$if set threads                   $setglobal MSK_IPAR_NUM_THREADS %threads%
$if set accuracy                  $setglobal MSK_DPAR_INTPNT_TOL_REL_GAP %accuracy%
$if set accuracy                  $setglobal MSK_DPAR_MIO_REL_GAP_CONST %accuracy%
$if set mipaccuracy               $setglobal MSK_DPAR_MIO_TOL_REL_GAP %mipaccuracy%


$elseifi.solver %solver%=="convert"


$elseifi.solver %solver%=="scip"


$else.solver
$abort "No valid solver specified. Available solvers are CPLEX, Gurobi, COPT, XPRESS, HiGHS, MOSEK, Convert, or SCIP."
$endif.solver


$setenv GDXCOMPRESS 1

option mip = %solver%;
option reslim = 1209600;
option optcr = %mipaccuracy%;
remix.threads = %threads%;
remix.optFile = %optfile%;
remix.solveLink = %solvelink%;
remix.holdFixed = %holdfixed%;

$offVerbatim