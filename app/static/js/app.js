/* Add your Application JavaScript */
console.log('this is some JavaScript code');

function notify() {
  alert('in here I will do something');
}

const updateActiveNav = function() {
  let page = window.location.href.split('/').at(3);
  $('.nav-link').removeClass('active');

  $('.nav-link').each(function(link){
    if (page.length == 0) {

      $('.nav-link').first().addClass('active');
      return false;
      
    } else {

      if ($(this).html().toLowerCase() == page.toLowerCase()) {
        $(this).addClass('active');
        return false;
      }

    }
  });
}

$(document).ready(function(e){
  updateActiveNav();

});
