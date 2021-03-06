<?php

//fetch.php

include("database_connection.php");

$query = "SELECT * FROM schedules WHERE processed = 0 ORDER BY swdate, swtime";
$statement = $connect->prepare($query);
$statement->execute();
$result = $statement->fetchAll();
$total_row = $statement->rowCount();
$output = '
<table class="table table-striped table-bordered">
	<tr>
		<th>Datum</th>
		<th>Tijd</th>
		<th>Ingang</th>
		<th>Transitie</th>
		<th>Looptijd</th>
		<th>Herhaal</th>
		<th>Edit</th>
		<th>Delete</th>
	</tr>
';
if($total_row > 0)
{
	foreach($result as $row)
	{
		$output .= '
		<tr>
			<td width="10%">'.$row["swdate"].'</td>
			<td width="10%">'.$row["swtime"].'</td>
			<td width="10%">'.$row["scene"].'</td>
			<td width="10%">'.$row["transition"].'</td>
			<td width="20%">'.$row["duration"].'</td>
			<td width="20%">'.$row["repeattime"].'</td>
			<td width="5%">
				<button type="button" name="edit" class="btn btn-primary btn-xs edit" id="'.$row["id"].'">Edit</button>
			</td>
			<td width="5%">
				<button type="button" name="delete" class="btn btn-danger btn-xs delete" id="'.$row["id"].'">Delete</button>
			</td>
		</tr>
		';
	}
}
else
{
	$output .= '
	<tr>
		<td colspan="4" align="center">Data not found</td>
	</tr>
	';
}
$output .= '</table>';
echo $output;
?>