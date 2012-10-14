<?php
$allowedExts = array("jpg", "jpeg", "gif", "png");
$extension = end(explode(".", $_FILES["file"]["name"]));
//print_r($_FILES["file"]["size"]);

if ((($_FILES["file"]["type"] == "image/gif")
     || ($_FILES["file"]["type"] == "image/jpeg")
     || ($_FILES["file"]["type"] == "image/png")
     || ($_FILES["file"]["type"] == "image/pjpeg"))
    && ($_FILES["file"]["size"] < 2000000)
    && in_array($extension, $allowedExts))
{
     if ($_FILES["file"]["error"] > 0)
     {
          echo "Return Code: " . $_FILES["file"]["error"] . "<br />";
     }
     else
     {
          echo "<script src='./js/jquery.js'></script>";
          echo "<script src='./js/animate.js'></script>";
          echo "Upload: " . $_FILES["file"]["name"] . "<br />";
          echo "Type: " . $_FILES["file"]["type"] . "<br />";
          echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
          echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />";
          echo "<img  class='face' src=./upload/". $_FILES["file"]["name"] . " alt='yea'>";
//          echo "<canvas id='canvas'></canvas>";

          if (file_exists("upload/" . $_FILES["file"]["name"]))
          {
               echo $_FILES["file"]["name"] . " already exists. ";
          }
          else
          {
               move_uploaded_file($_FILES["file"]["tmp_name"],
                                  "./upload/" . $_FILES["file"]["name"]);
               echo "Stored in: " . "./upload/" . $_FILES["file"]["name"];
          }
     }
}
else
{
     echo "Invalid file";
}
?>
