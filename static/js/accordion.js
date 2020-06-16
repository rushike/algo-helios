/* accordion.js */

function getAccordion(element_id,screen) 
{
    $(window).resize(function () { location.reload(); });

	if ($(window).width() < screen) 
	{
		var concat = '';
		obj_tabs = $( element_id + " li" ).toArray();
		obj_cont = $( ".tab-content .tab-pane" ).toArray();
		jQuery.each( obj_tabs, function( n, val ) 
		{
			concat += '<div id="' + n + '" class="panel panel-default">';
			concat += '<div class="panel-heading" role="tab" id="heading' + n + '">';
			concat += '<a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse' + n + '" aria-expanded="false" aria-controls="collapse' + n + '"><h4 class="panel-title">' + val.innerText + '</h4></a>';
			concat += '</div>';
			concat += '<div id="collapse' + n + '" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading' + n + '">';
			concat += '<div class="panel-body">' + obj_cont[n].innerHTML + '</div>';
			concat += '</div>';
			concat += '</div>';
		});
		$("#accordion").html(concat);
		$("#accordion").find('.panel-collapse:first').addClass("in");
		$("#accordion").find('.panel-title a:first').attr("aria-expanded","true");
		$(element_id).remove();
		$(".tab-content").remove();
	}	
}




  (function($) {
    // $('.accordion > li:eq(0) a').addClass('active').next().slideDown();
	
    $('.accordion a').click(function(j) {
        var dropDown = $(this).closest('li').find('p');
		console.log("inside FAQ")
        $(this).closest('.accordion').find('p').not(dropDown).slideUp();

        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
        } else {
            $(this).closest('.accordion').find('a.active').removeClass('active');
            $(this).addClass('active');
        }

        dropDown.stop(false, true).slideToggle();

        j.preventDefault();
    });

	})(jQuery);