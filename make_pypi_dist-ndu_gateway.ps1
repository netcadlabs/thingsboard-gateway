# pre-requires
# pip install wheel

$NDU_GATEWAY_MODULE_NAME = "ndu_gateway"

# clear old dist files
Get-ChildItem *.egg-info | foreach { Remove-Item -Recurse -Path $_.FullName }

If ((Test-Path "$NDU_GATEWAY_MODULE_NAME.egg-info") -eq $True){ Remove-Item -Recurse -Path "$NDU_GATEWAY_MODULE_NAME.egg-info" }
If ((Test-Path build) -eq $True){ Remove-Item -Recurse -Path build }
If ((Test-Path dist) -eq $True){ Remove-Item -Recurse -Path dist }
If ((Test-Path $NDU_GATEWAY_MODULE_NAME) -eq $True){ Remove-Item -Recurse -Path $NDU_GATEWAY_MODULE_NAME }

$replaceLsit = @(
    ('from thingsboard_gateway.', 'from ndu_gateway.'),
    ('thingsboard-gateway', 'ndu-gateway'),
    ('thingsboard_gateway', 'ndu_gateway')
);

# copy all code to ndu_gateway folder
cp .\thingsboard_gateway\ .\$NDU_GATEWAY_MODULE_NAME -Recurse
Get-ChildItem .\$NDU_GATEWAY_MODULE_NAME -Recurse | foreach {
    if($_.FullName.endswith(".py")){
        for ($i=0; $i -lt $replaceLsit.length; $i++) {
            $find =  $replaceLsit[$i][0]
            $replace =  $replaceLsit[$i][1]
            Write-Output "Replacing  $find with $replace in $($_.FullName)"
            ((Get-Content -path $_.FullName -Raw) -replace $find, $replace) | Set-Content -Path $_.FullName
        }
    }
}

# preparing dist
python setup_ndu_gateway.py sdist bdist_wheel

# clear copied code
# Remove-Item -Recurse -Path ndu_gateway

# uploading dist
# python -m twine upload dist/*

# installing created whl file
# pip install ./dist/ndu_gateway-<VERSION>.whl