<!doctype html>
<html>
	<head>
		<title> Coding Club </title>
		<link type="text/css" rel="stylesheet" href="code.css"/>
	</head>
	<body>
		<script src="template.js"></script>
		  <?php 
		    echo '<img src="';
		    $option = array("cat-of-doom.jpg","cat.jpeg","minion.jpeg","pocahontas.jpeg","turtle.jpeg");
		    $img = rand(0,$option.length());
		    echo $option[$img];
		    echo '"/>';
		  ?>
		</div>
	</body>
</html>
