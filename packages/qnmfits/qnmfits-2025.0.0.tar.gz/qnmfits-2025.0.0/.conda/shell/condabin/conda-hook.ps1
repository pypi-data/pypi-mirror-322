$Env:CONDA_EXE = "/Users/eliot/Documents/Research/Ringdown/sxs-collaboration/qnmfits/.conda/bin/conda"
$Env:_CE_M = $null
$Env:_CE_CONDA = $null
$Env:_CONDA_ROOT = "/Users/eliot/Documents/Research/Ringdown/sxs-collaboration/qnmfits/.conda"
$Env:_CONDA_EXE = "/Users/eliot/Documents/Research/Ringdown/sxs-collaboration/qnmfits/.conda/bin/conda"
$CondaModuleArgs = @{ChangePs1 = $True}
Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs