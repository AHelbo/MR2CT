show_my_jobs="$1"
sort_by_name="$2"
squeue_cmd="squeue --format=\"%.10i %.40j %.10u %.15M %.15l %.20R\""

if [[ "${show_my_jobs^^}" == "M" ]]; then
    squeue_cmd+=" --me"
    if [[ "${sort_by_name^^}" == "S" ]]; then
        squeue_cmd+=" --sort j"
    fi    
fi

eval "$squeue_cmd"