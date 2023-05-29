#!C:\xampp\perl\bin\perl.exe
print "Content-type:text/html\r\n\r\n";

$randomx = int(rand(100));
$randomy = int(rand(100));

#make sure different numbers are generated
while ($randomx == $randomy) {
	$randomy = int(rand(100)); 
}

$xstatus = "";
$ystatus = "";

if ($randomx > $randomy) {
	$xstatus = "right.html";
	$ystatus = "wrong.html";
}
else {
	$xstatus = "wrong.html";
	$ystatus = "right.html";
}

print "<html>";
print "<head>";
print "<meta http-equiv='cache-control' content='no-cache'/>";
print "<title>Questionnaire</title>";
print "</head>";

print "<body>";

print "<h1>Pick the Largest Number</h1>";

print "<a href='../../../var/www/html/".$xstatus."'>".$randomx."</a>";
print "<p>OR</p>";
print "<a href='../../../var/www/html/".$ystatus."'>".$randomy."</a>";

print "</body>" ;
print "</html>" ;