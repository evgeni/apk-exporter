#!/bin/sh

set -eu
set -o pipefail

DIR=$(dirname "$0")

apk update
apk add python3
${DIR}/../apk-exporter.py
${DIR}/../apk-exporter.py --textfile out.prom
${DIR}/../apk-exporter.py --update
