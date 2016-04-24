function imageHandler(e2) 
{ 
  var myimage = 'myimage'
  var store = document.getElementById('imgstore');
  store.innerHTML='<img width="300" src="' + e2.target.result +'" id="' + myimage + '"/>';
  // var myimagesrc = document.getElementById('myimage').src;

  console.log (store);
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
  drawimg.width = $('#w').val();
  drawimg.height = $('#h').val();
  ctx.drawImage(origimg, $('#x').val(), $('#y').val(), $('#w').val(), $('#h').val(), 0,0,$('#w').val(),$('#h').val());

  var saveImg = drawimg.toDataURL("image/png");
  document.getElementById('mycanvas').src = saveImg;
  console.log(saveImg.data);

  //var newimg = new Image();
  //newimg.src = drawimg.toDataURL("image/png");
  //$('#save').append(newimg);

  $.ajax({
    url: '/upload_img',
    data: {'img': saveImg},
    type: 'POST',
    success: function(response) {
      console.log(response);
    },
    error: function(error) {
      console.log(error);
    }
  });

}

// function download() 
// {
//   var dt = document.getElementById("mycanvas").toDataURL('image/jpeg');
//   console.log(dt);
//   this.href = dt;
// }
// var el = document.getElementById('saveJpg');
// if(el)
// {
//   el.addEventListener('click', download, false);
// }

