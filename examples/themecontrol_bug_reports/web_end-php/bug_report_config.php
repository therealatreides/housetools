<?php
/* Database credentials. Assuming you are running MySQL
server with default setting (user 'root' with no password) */
define('DB_SERVER', 'my.server.com');
define('DB_USERNAME', 'myUsername');
define('DB_PASSWORD', 'myPassword');
define('DB_NAME', 'addonbugs');

/* Attempt to connect to MySQL database */
$link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);

// Check connection
if($link === false){
    die("ERROR: Could not connect to database. " . mysqli_connect_error());
}
?>