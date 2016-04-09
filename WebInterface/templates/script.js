function imageHandler(e2) 
{ 
  var myimage = 'myimage'
  var store = document.getElementById('imgstore');
  store.innerHTML='<img src="' + e2.target.result +'" id="' + myimage + '"/>';

  console.log (store);
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

function cropFunc ()
{
  var v_top = document.getElementById("top-region").value;
  var v_bottom = document.getElementById("bottom-region").value;
  var v_right = document.getElementById("right-region").value;
  var v_left = document.getElementById("left-region").value;
  v_top +="px";
  v_top = Number(v_top);
  v_bottom +="px";
  v_bottom = Number(v_bottom);
  v_left +="px";
  v_left = Number(v_left);
  v_right +="px";
  v_right = Number(v_right);
  document.getElementById("myimage").style.clip = "rect(v_top v_right v_bottom v_left)";
}