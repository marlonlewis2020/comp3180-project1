/* Add your Application JavaScript */
console.log('this is some JavaScript code');

function notify() {
  alert('in here I will do something');
}

const updateActiveNav = function() {
  let href = window.location.href.split('/');
  let page = href.at(3);
  let param = href.length>4 ? href.at(4) : null;
  $('.nav-link').removeClass('active');

  $('.nav-link').each(function(link){
    if (page.length == 0) {

      $('.nav-link').first().addClass('active');
      return false;
      
    } else {

      // $(this).addClass('active');
      if ($(this).html().toLowerCase() == page.toLowerCase()) {
        $(this).addClass('active');
        return false;
      }

      else {
        if (param !== null && param !== undefined && param == "create") {
          $('.nav-link:nth-child(1)')[2].classList.add('active');
          return false;
        }
      }


    }
  });
}

$(document).ready(function(e){
  updateActiveNav();

  (function(){
      setTimeout(function(){$('.alert').fadeOut("fast");}, 8000);
      setTimeout(function(){$(".input-field").removeClass("invalid");}, 8000);
  })();

});
