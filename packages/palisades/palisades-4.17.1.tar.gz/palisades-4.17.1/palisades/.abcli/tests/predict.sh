#! /usr/bin/env bash

function test_palisades_predict() {
    local options=$1

    palisades_predict \
        ingest,$options \
        - \
        palisades-dataset-v1-ingest-2025-01-20-520ze1-model-2025-01-20-s5xtkp \
        datacube-maxar_open_data-WildFires-LosAngeles-Jan-2025-11-031311102213-103001010B9A1B00
}
