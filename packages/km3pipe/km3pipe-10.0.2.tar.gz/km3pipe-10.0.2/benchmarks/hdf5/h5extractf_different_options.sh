#!/bin/bash
set -e

for file in $(python -m km3net_testdata offline)/*.root; do
    echo "Processing $file"
    h5extractf --without-full-reco --without-calibration $file
    echo done
done
