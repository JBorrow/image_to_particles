#!/bin/bash

# Run SWIFT
./swiftsim/swift --hydro --threads=4 album_cover.yml

python3 makeMovieSwiftsimIO.py

