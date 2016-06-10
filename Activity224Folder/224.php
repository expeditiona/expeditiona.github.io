<?php
// This block allows our program to access the MySQL database.
// Stores your login information in PHP variables
require_once 'studentdb.php';
// Accesses the login information to connect to the MySQL server using your credentials and database
$db_server = mysql_connect($host, $username, $password);
// This provides the error message that will appear if your credentials or database are invalid
if (!$db_server) die("Unable to connect to MySQL: " . mysql_error());
mysql_select_db($dbname)
	or die("Unable to select database: " . mysql_error());

// First lines of HTML, up to where MySQL is needed	
echo '<!DOCTYPE html>
<html>

<head>
<!-- Refer to CSS and JS files -->
<link rel="stylesheet" href="updated_32_css.css">
<script src="updated_32_js.js"></script>

</head>


<body>

    <div id="full">
        <!-- Button click adds grade to table -->
        <button class="myButton" onclick="NumCheck()">Add Grade</button>

        <!-- Page header -->
        <div>
            <h1 class="Title">GradeLock</h1>
            <p class="descrip"><b><em>Your personal grade book</em></b></p>
            <br>
        </div>
        <br>


        <div class="dropdown1">
            <!-- Dropdown menu of student names -->
            <select onclick="dropDown100()" class="dropbtn1">Dropdown</button>
            <div id="myDropdown" class="dropdown-content1">
                <option value="Select A Student">Select A Student</option>
                <option value="Steve Harvey">Steve Harvey</option>
                <option value="Calvin Hobbes">Calvin Hobbes</option>
                <option value="Sharkeisha Jones">Sharkeisha Jones</option>
                <option value="Michael Kors">Michael Kors</option>
                <option value="Kristy Porzingis">Kristy Porzingis</option>
                <option value="Christina Bosh">Christina Bosh</option>
                <option value="Shaniqua Martinez">Shaniqua Martinez</option>
                <option value="Stephanie Curry">Stephanie Curry</option>
                <option value="Andrea Drummond">Andrea Drummond</option>
                <option value="Janelle Okafor">Janelle Okafor</option>
            </div>
            </select>

            <!-- Dropdown menu of assignment numbers -->
            <select onclick="dropDown100()" class="dropbtn1">Dropdown</button>
            <div id="myDropdown" class="dropdown-content1">
                <option value="Select An Assignment">Select An Assignment</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
            </div>
            </select>
        </div>

            <!-- User inputs grade here -->
            <input type="text" label="Enter a grade." id="tbox"></input>

        <br>
        <br>
        <br>
        <br>

            <!-- Main table that is displayed -->
            <!-- Data queried from MySQL database -->
            <table id="grades">
                <tr>
                    <th>Student ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Grade Level</th>
                    <th>Assignment 1</th>
                    <th>Assignment 2</th>
                    <th>Assignment 3</th>
                    <th>Assignment 4</th>
                    <th>Assignment 5</th>
                    <th>Average</th>
                </tr>';

//query strings; selects whole table
$query = "SELECT * FROM gradebook_full"; 
$lockerquery = "SELECT * FROM locker";
//queries the string, returns MySQL table
$grade_reqs = mysql_query($query);
$locker_reqs = mysql_query($lockerquery);
//gets # of rows
$num = mysql_num_rows($grade_reqs);
//variable representing # of columns
$init_col_count = 9;
//iterates through rows in grade_reqs, creates HTML row
for ($i = 0; $i < $num; $i++){
    //initializes sum of grades in row to 0
    $row_total = 0;
    $req = mysql_fetch_row($grade_reqs);
    echo '<tr>';
    //iterates through fields in row and if field is a grade, adds it to $row_total
    for($j = 0; $j < $init_col_count; $j++) {
        echo '<td>' . $req[$j] . '</td>';
        if($j >= 4) $row_total += $req[$j];
    }
    //calculates and displays average
    $av = ($row_total)/($init_col_count-4);
    echo '<td>' . (int) $av . '</td>';
    echo '</tr>';
}
echo '</table>
    </div> 
</body>

</html>';
?>