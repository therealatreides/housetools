<?php
    // Include config file
    require_once 'bug_report_config.php';

    $sql = "SELECT * FROM bugs_table";
    $result = $link->query($sql);

    while ($row = mysqli_fetch_array($result)){
        $number = $row['ind'];
        $desc = $row['description'];
        $submitted = $row['submitted'];
        $resolved = $row['resolved'];
        $resolution = $row['resolution'];

        if($resolved == '0'){
            echo ''.$number.' ('.$submitted.'): '.$desc.'[CR]';
        }
    }
    $link->close();
?>