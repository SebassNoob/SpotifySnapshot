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

function TC(){
  let classesTC = $('#TC').attr('class').split(/\s+/);
  
  if (classesTC.includes("d-none")){
    $('#TC').removeClass("d-none").addClass('d-show');
    
  }
  if (classesTC.includes("d-show")){
    $('#TC').removeClass("d-show").addClass('d-none');
    
  }

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
    let count = 7;
    setInterval(()=>{
      
      count -=1;
      $("#countdown-for-redirect").text((i,original_text)=>{
        return count
      })
    }, 1000);

  
    //form validation
    //when page is loaded, checkbox will always be unchecked hence disable the submit button
    $('#submit-button').addClass('disabled');

    
    $( 'input[type="checkbox"]' ).click(function() {
      
      if (this.checked){
        
        $('#submit-button').removeClass('disabled');
      } else {
        
        $('#submit-button').addClass('disabled');
      }
      
    });
    
    $("#length-playlist").on("input",()=>{

      let input = $("#length-playlist").val();

      let validInt= input.match('^[0-9]*$');
      
      if (validInt && ((parseInt(input) <=50 && parseInt(input) >= 1 )|| input === "")){
        $('#num-error').addClass("d-none").removeClass('d-show')
      } else{
        $('#num-error').removeClass("d-none").addClass('d-show')
      }
    });
      
    }
  

  
})