var scale;

function imageHandler(e2) 
{ 

  var myimage = 'myimage'
  var store = document.getElementById('imgstore');
  var img = document.createElement('img');
  img.src = e2.target.result;
  img.id = myimage;

  console.log("2: " + img.width);
  var new_imgwidth = 300;
  scale = img.width / new_imgwidth;

  img.width = 300;
  store.innerHTML='<img width=' + img.width + ' src="' + e2.target.result +'" id="' + myimage + '"/>';
  // var myimagesrc = document.getElementById('myimage').src;

  console.log(store);
  // console.log(myimagesrc);
  // window.open(myimagesrc);

  jQuery(function($){
    console.log($('#myimage'));
    $('#myimage').Jcrop({
      setSelect: [0, 0, 50, 50],
      onSelect: updateCoordinates
    });
  });
  
}

function loadimage(e1)
{
  var filename = e1.target.files[0]; 
  var fr = new FileReader();
  fr.onload = imageHandler;
  fr.readAsDataURL(filename); 
}

window.onload=function()
{
  var y = document.getElementById("getimage");
  y.addEventListener('change', loadimage, false);
}

function updateCoordinates (c)
{
  $('#x').val(c.x);
  $('#y').val(c.y);
  $('#w').val(c.w);
  $('#h').val(c.h);
}

function checkCoords()
{
  if (parseInt($('#w').val())) return true;
  alert('Please select a crop region then press submit.');
  return false;
}

function crop_image()
{

  console.log("crop image.");
  var drawimg = document.getElementById("mycanvas");
  var ctx = drawimg.getContext("2d");
  var origimg = document.getElementById("myimage");
  drawimg.width = $('#w').val()*scale;
  drawimg.height = $('#h').val()*scale;
  ctx.drawImage(origimg, $('#x').val()*scale, $('#y').val()*scale, $('#w').val()*scale, $('#h').val()*scale, 0,0,drawimg.width,drawimg.height);
  
  var saveImg = drawimg.toDataURL("image/jpeg");

  $.ajax({
    url: '/upload_img',
    data: {'img': saveImg},
    type: 'POST',
    success: function(response) {
      console.log("success");
    },
    error: function(error) {
      console.log("error");
    }
  });

}
