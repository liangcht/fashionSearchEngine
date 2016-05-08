function refresh_img(node){
  var address;
  if(node.src.indexOf('?')>-1){
    address = node.src.split('?')[0];
  }
  else {
    address = node.src;
    node.src = address+"?time="+new Date().getTime();
    console.log(node.src);
  }
}
window.onload = function(){
  var node = document.getElementById('stored_qimg');
  refresh_img(node);
}

