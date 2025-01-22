#! /usr/bin/env bash

function test_kamangir_help() {
    local options=$1

    local module
    for module in \
        "kamangir"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
