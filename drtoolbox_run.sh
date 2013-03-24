if [ ${OCTAVE+x} ]; then
    echo ' Testing MTfDR using Octave.'
    octave -qf drtoolbox_run.m | grep 'Elapsed'
else
    echo ' Testing MTfDr using Matlab.'
    matlab -jvm -nodisplay -r 'drtoolbox_run; quit' | grep 'Elapsed'
fi
