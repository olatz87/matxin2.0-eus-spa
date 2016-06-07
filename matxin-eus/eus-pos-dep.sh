#!/bin/sh

sh ixa-pipe-pos-eu/run.sh | sh ixa-pipe-dep-eu/run.sh | python3 naf2matxin_v2.py
