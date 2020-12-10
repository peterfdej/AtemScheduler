<?php

//action.php

include('database_connection.php');

if(isset($_POST["action"]))
{
	if($_POST["action"] == "insert")
	{
		$query = "
		INSERT INTO schedules 
		(swdate, swtime, scene, transition, duration, repeattime, processed) 
		VALUES (
		'".$_POST["swdate"]."',
		'".$_POST["swtime"]."',
		'".$_POST["scene"]."',
		'".$_POST["transition"]."',
		'".$_POST["duration"]."',
		'".$_POST["repeattime"]."',
		'0')
		";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Inserted...</p>';
	}
	if($_POST["action"] == "fetch_single")
	{
		$query = "
		SELECT * FROM schedules WHERE id = '".$_POST["id"]."'
		";
		$statement = $connect->prepare($query);
		$statement->execute();
		$result = $statement->fetchAll();
		foreach($result as $row)
		{
			$output['swdate'] = $row['swdate'];
			$output['swtime'] = $row['swtime'];
			$output['scene'] = $row['scene'];
			$output['transition'] = $row['transition'];
			$output['duration'] = $row['duration'];
			$output['repeattime'] = $row['repeattime'];
		}
		echo json_encode($output);
	}
	if($_POST["action"] == "update")
	{
		$query = "
		UPDATE schedules 
		SET swdate = '".$_POST["swdate"]."',
		swtime = '".$_POST["swtime"]."',
		scene = '".$_POST["scene"]."',
		transition = '".$_POST["transition"]."',
		duration = '".$_POST["duration"]."',
		repeattime = '".$_POST["repeattime"]."'
		WHERE id = '".$_POST["hidden_id"]."'
		";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Updated</p>';
	}
	if($_POST["action"] == "delete")
	{
		$query = "DELETE FROM schedules WHERE id = '".$_POST["id"]."'";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Deleted</p>';
	}
}

?>