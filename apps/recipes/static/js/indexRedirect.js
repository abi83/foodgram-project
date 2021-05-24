   setTimeout(function(){
      window.location.href = '/';
   }, 5000);
   setInterval(function(){
     document.querySelector('#timer').innerHTML -= 1;
   }, 1000)