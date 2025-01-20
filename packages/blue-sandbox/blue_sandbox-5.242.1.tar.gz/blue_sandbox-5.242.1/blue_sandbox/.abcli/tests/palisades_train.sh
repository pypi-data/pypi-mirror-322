#! /usr/bin/env bash

function test_blue_sandbox_palisades_train() {
    local options=$1

    local query_object_name=palisades-dataset-v1

    # test is empty; the train subset causes the github worker to crash.
    if [[ "$abcli_is_github_workflow" == false ]]; then
        abcli_eval ,$options \
            roofai_dataset_review \
            download \
            $query_object_name \
            --index 0 \
            --subset test
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    fi

    local dataset_object_name=test-${query_object_name}-ingest-$(abcli_string_timestamp_short)

    abcli_eval ,$options \
        roofai_dataset_ingest \
        download,source=$query_object_name \
        $dataset_object_name \
        --test_count 1000 \
        --train_count 8000 \
        --val_count 1000
    [[ $? -ne 0 ]] && return 1

    abcli_hr

    local subset
    for subset in train test val; do
        abcli_eval ,$options \
            roofai_dataset_review \
            - \
            $dataset_object_name \
            --index 0 \
            --subset $subset
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    # next step

    return 0
}
