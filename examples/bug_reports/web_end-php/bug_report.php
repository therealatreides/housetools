<?php
error_reporting(-1);
// Include config file
require_once 'bug_report_config.php';

// Define variables and initialize with empty values
$bug_report_err = "";

// Processing form data when form is submitted
if($_SERVER["REQUEST_METHOD"] == "POST")
{

    // Check if addon name is empty
    if(empty(trim($_POST["bug_report"]))){
        $bug_report_err = 'Please enter bug description.';
    }

    // Validate bullshit
    if(empty($bug_report_err))
    {

        $sql = "INSERT INTO bugs_table (description, submitted, resolved) VALUES (?, ?, ?)";

        $bug_report = trim($_POST["bug_report"]);
        $d = strtotime("now");
        $submission_date = date("Y-m-d", $d);
        $resolved = '0';

        $stmt = $link->prepare($sql);
        $stmt->bind_param("ssss", $bug_report, $submission_date, $resolved);

        $stmt->execute();
        $stmt->close();

    }
    $link->close();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bug Reporting</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.css">
    <style type="text/css">
        body{ font: 14px sans-serif; }
        .wrapper{ width: 350px; padding: 20px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <h2>Bug Reporting</h2>
        <p>Please fill in your bug report.</p>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="form-group <?php echo (!empty($bug_report_err)) ? 'has-error' : ''; ?>">
                <label>Bug Details</label>
                <input type="bug_report" name="bug_report" class="form-control">
                <span class="help-block"><?php echo $bug_report_err; ?></span>
            </div>
            <div class="form-group">
                <input type="submit" class="btn btn-primary" value="Submit">
            </div>
        </form>
    </div>
</body>
</html>