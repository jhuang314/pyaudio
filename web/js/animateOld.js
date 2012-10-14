var canvas = document.getelementbyid("canvas");
ctx = canvas.getContext("2d");

var src = "../uploads/";
var img = new Image();
img.onload = function(){
	ctx.drawImage(img, 0, 0);

};
img.src = src;
