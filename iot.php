
<html>
<head>
<meta name="viewport" content="width=device-width" />
<title>Monitoring</title>
</head>
	<meta http-equiv="refresh" content="2">

        <body align="center" style="background:powderblue;"> 

		<h1>Smart bell notification </h1> 

	<form method="get" action="iot.php">

		<img src="capture.jpg"  height="320" width="480">
	</form>      

        <form method="get" action="iot.php">

                <input type="submit" value="open" name="on">
                <input type="submit" value="close" name="off">
		<input type="submit" value="Alert" name="off">
			
		
        </form>
	

        <?php

		$setmode21 = shell_exec("/usr/local/bin/gpio -g mode 21 out");

		
	        if(isset($_GET['on'])){
	                $gpio_on = shell_exec("/usr/local/bin/gpio -g write 21 1");
	        }
		else if(isset($_GET['off'])){
	                $gpio_off = shell_exec("/usr/local/bin/gpio -g write 21 0");
	        }

	?>
	<br><br>
	<?php
		
		$myfile = fopen("/home/pi/log.txt", "r") or die("Unable to open file!");
		echo fread($myfile,filesize("/home/pi/log.txt"));
		fclose($myfile);	

        ?>
	
        </body>
</html>