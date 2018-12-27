<?php


$py_home = "/usr/bin/python";
$source = $_GET["source"];
$file_path = $_GET["file_path"];
$drug = $_GET["drug"];

if ($source == "get_list"){
    $cmd = $py_home.' ./get_list_dir.py';

}else if($source == "parse_json"){
    $cmd = $py_home.' ./parse_json.py '.$file_path;

}else if($source == "get_drug"){
    $cmd = $py_home.' ./get_drug_info.py '.$file_path;

}else if($source == "get_watson_ct"){
    $cmd = $py_home.' ./get_watson_clinical_trial.py '.$file_path.' '.$drug;

}else if($source == "get_gene_anno"){
    $cmd = $py_home.' ./get_gene_anno.py '.$file_path;

}else if($source == "get_gene"){
    $cmd = $py_home.' ./get_gene_info.py '.$file_path;

}else if($source == "get_drug_each"){
    $cmd = $py_home.' ./get_drug_info_each.py '.$file_path.' '.$drug;
}


$result = exec($cmd, $output, $return_ver);
#print_r ($return_ver);
#print_r ($output);
#print_r ($result);

echo $result;

exit;



?>
