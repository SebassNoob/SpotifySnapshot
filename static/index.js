//w3schools getcookie function
//takes name of cookie one is trying to find, outputs value if found else returns null
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return null;
}



$('document').ready(()=>{
  const pathname = window.location.pathname;
  if (pathname === "/"){
    console.log(getCookie('auth'))
    if (getCookie("auth") === null){
      $('#getit-link').addClass("disabled").css("color","grey");
    }
    else{
      // do nothing, it is enabled
    }
    $('.get-started').click(()=>{
      window.location.pathname='/login';
    })
  }
  
  if (pathname === "/getit") {

    //countdown for error page
    let count = 5;
    setInterval(()=>{
      
      count -=1;
      $("#countdown-for-redirect").text((i,original_text)=>{
        return count
      })
    }, 1000);
    
    
  }
  

  
})