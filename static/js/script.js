$(document).ready(function() {

	var temp = 0;

	// Credentials
	var baseUrl = "https://api.dialogflow.com/v1/query?v=20150910&";
	var accessToken = "eb2fbc1987d24fbfbff0fa2f96c9cf27";

	//---------------------------------- Add dynamic html bot content(Widget style) ----------------------------
	// You can also add the html content in html page and still it will work!
	var mybot = '<div class="chatCont" id="chatCont">'+

								'<div class="bot_profile">'+
									'<img src="/static/img/bot2.svg" class="bot_p_img">'+
									'<div class="close">'+
										'<i class="fa fa-times" aria-hidden="true"></i>'+
									'</div>'+

								'</div><!--bot_profile end-->'+

								'<div id="result_div" class="resultDiv">			</div>'+

								'<div class="spinner">'+
									'<div class="bounce1"></div>'+
									'<div class="bounce2"></div>'+
									'<div class="bounce3"></div>'+
								'</div>'+

								'<div class="chatForm" id="chat-div">'+

									'<div style="float: left; width: 87%;">'+
    								'<input type="text" id="chat-input" autocomplete="off" placeholder="Try typing here"'+ 'class="form-control bot-txt"/>'+
  								'</div>'+
  								'<div style="float: right;">'+
    								'<input id="send-img" type="image" src="/static/img/send.png" style="width:3rem; height:3rem; text-align: center;"/>'+
  								'</div>'+
								'</div>'+

							'</div>'+

							'<div class="profile_div">'+
								'<div class="row">'+
									'<div class="col-hgt">'+
										'<img src="/static/img/bot2.svg" class="img-circle img-profile">'+
									'</div><!--col-hgt end-->'+
									'<div class="col-hgt">'+
										'<div class="chat-txt">'+
											'Chat with us now!'+
										'</div>'+
									'</div><!--col-hgt end-->'+
								'</div><!--row end-->'+
							'</div><!--profile_div end-->'+

							// class="btn-group-vertical"

							'<div class="help">'+
								'<i class="far fa-question-circle"></i>'+
							'</div>';

	$("mybot").html(mybot);

	// ------------------------------------------ Toggle chatbot -----------------------------------------------
	$('.profile_div').click(function() {
		$('.profile_div').toggle();
		$('.chatCont').toggle();
		$('.bot_profile').toggle();
		$('.chatForm').toggle();
		$('.help').toggle();

		valArray = ['You Can Ask Questions like this!','Founders of Agonauts','Know more about Algonauts','What do we do?','Price of our Products?'];

		val = valArray[0];

		var BotResponse = '';

		var i;
		for (i = 1; i < (valArray.length); i++) {
			BotResponse = BotResponse + '<br class="dynamic_button"><button id="button'+i+'" class="dynamic_button mybtn btn btn-sm btn-primary" type="button">'+ valArray[i] +'</button>';
		}
		temp = i;

		BotResponse = '<p class="botResult">'+val+BotResponse+'</p><div class="clearfix"></div>';

		$(BotResponse).appendTo('#result_div');

		$("#result_div").animate({ scrollTop: $("#result_div")[0].scrollHeight}, 1000);

		document.getElementById('chat-input').focus();
	});

	$('.close').click(function() {
		$('.profile_div').toggle();
		$('.chatCont').toggle();
		$('.bot_profile').toggle();
		$('.chatForm').toggle();
		$('.help').toggle();
	});

	$('.mybtn').click(function(){
	});

	$('.help').click(function(){
		valArray = ['You Can Ask Questions like this!','Founders of Agonauts','Know more about Algonauts','What do we do?','Price of our Products?'];

		val = valArray[0];

		var BotResponse = '';

		var i;
		for (i = 1; i < (valArray.length); i++) {
			BotResponse = BotResponse + '<br class="dynamic_button"><button id="button'+i+'" class="dynamic_button mybtn btn btn-sm btn-primary" type="button">'+ valArray[i] +'</button>';
		}
		temp = i;

		BotResponse = '<p class="botResult">'+val+BotResponse+'</p><div class="clearfix"></div>';

		$(BotResponse).appendTo('#result_div');

		$("#result_div").animate({ scrollTop: $("#result_div")[0].scrollHeight}, 1000);
	});


	// Session Init (is important so that each user interaction is unique)--------------------------------------
	var session = function() {
		// Retrieve the object from storage
		if(sessionStorage.getItem('session')) {
			var retrievedSession = sessionStorage.getItem('session');
		} else {
			// Random Number Generator
			var randomNo = Math.floor((Math.random() * 1000) + 1);
			// get Timestamp
			var timestamp = Date.now();
			// get Day
			var date = new Date();
			var weekday = new Array(7);
			weekday[0] = "Sunday";
			weekday[1] = "Monday";
			weekday[2] = "Tuesday";
			weekday[3] = "Wednesday";
			weekday[4] = "Thursday";
			weekday[5] = "Friday";
			weekday[6] = "Saturday";
			var day = weekday[date.getDay()];
			// Join random number+day+timestamp
			var session_id = randomNo+day+timestamp;
			// Put the object into storage
			sessionStorage.setItem('session', session_id);
			var retrievedSession = sessionStorage.getItem('session');
		}
		return retrievedSession;
		// console.log('session: ', retrievedSession);
	}

	// Call Session init
	var mysession = session();


	// on input/text enter--------------------------------------------------------------------------------------
	$('#chat-input').on('keyup keypress', function(e) {
		var keyCode = e.keyCode || e.which;
		var text = $("#chat-input").val();
		if (keyCode === 13) {
			if(text == "" ||  $.trim(text) == '') {
				e.preventDefault();
				$('#chat-input').focus();
				return false;
			} else {
				$("#chat-input").blur();
				setUserResponse(text);
				send(text);
				e.preventDefault();
				$('#chat-input').focus();
				return false;
			}
		}
	});

	$("#send-img").click(function(f){
		var text = $("#chat-input").val();

		if(text == "" ||  $.trim(text) == '') {
				f.preventDefault();
				$('#chat-input').focus();
				return false;
		} else {
				$("#chat-input").blur();
				setUserResponse(text);
				send(text);
				f.preventDefault();
				$('#chat-input').focus();
				return false;
		}
});

$(".mybtn").click(function(f){
	var text = $("#"+$(this).attr('id')).text();

	// console.log(text);

	if(text == "" ||  $.trim(text) == '') {
			f.preventDefault();
			$('#chat-input').focus();
			return false;
	} else {
			$("#chat-input").blur();
			setUserResponse(text);
			send(text);
			f.preventDefault();
			$('#chat-input').focus();
			return false;
	}
});

$(document).on("click", "button.mybtn", function(f){
	var text = $("#"+$(this).attr('id')).text();

	// console.log(text);

	if(text == "" ||  $.trim(text) == '') {
			f.preventDefault();
			$('#chat-input').focus();
			return false;
	} else {
			$("#chat-input").blur();
			setUserResponse(text);
			send(text);
			f.preventDefault();
			$('#chat-input').focus();
			return false;
	}
});


	//------------------------------------------- Send request to API.AI ---------------------------------------
	function send(text) {
		$.ajax({
			type: "GET",
			url: baseUrl+"query="+text+"&lang=en-us&sessionId="+mysession,
			contentType: "application/json",
			dataType: "json",
			headers: {
				"Authorization": "Bearer " + accessToken
			},
			// data: JSON.stringify({ query: text, lang: "en", sessionId: "somerandomthing" }),
			success: function(data) {
				main(data);
				// console.log(data);
			},
			error: function(e) {
				console.log (e);
			}
		});
	}


	//------------------------------------------- Main function ------------------------------------------------
	function main(data) {
		var action = data.result.action;
		var speech = data.result.fulfillment.speech;
		// use incomplete if u use required in api.ai questions in intent
		// check if actionIncomplete = false
		var incomplete = data.result.actionIncomplete;
		if(data.result.fulfillment.messages) { // check if messages are there
			if(data.result.fulfillment.messages.length > 0) { //check if quick replies are there
				var suggestions = data.result.fulfillment.messages[1];
			}
		}
		switch(action) {
			// case 'your.action': // set in api.ai
			// Perform operation/json api call based on action
			// Also check if (incomplete = false) if there are many required parameters in an intent
			// if(suggestions) { // check if quick replies are there in api.ai
			//   addSuggestion(suggestions);
			// }
			// break;
			default:
				setBotResponse(speech);
				if(suggestions) { // check if quick replies are there in api.ai
					addSuggestion(suggestions);
				}
				break;
		}
	}


	//------------------------------------ Set bot response in result_div -------------------------------------
	function setBotResponse(val) {
		setTimeout(function(){
			if($.trim(val) == '') {
						val = 'I couldn\'t get that. Let\' try something else!'
						var BotResponse = '<p class="botResult">'+val+'</p><div class="clearfix"></div>';
						$(BotResponse).appendTo('#result_div');
			}
			else {

						if(val.includes('->')){
							valArray = val.split("->");

							val = valArray[0];

							var BotResponse = '';

							var i;
							for (i = temp+1; i < (valArray.length+temp); i++) {
								BotResponse = BotResponse + '<br class="dynamic_button"><button id="button'+(i+4)+'" class="dynamic_button mybtn btn btn-sm btn-primary" type="button">'+ valArray[i-temp] +'</button>';
							}
							temp = i;

							BotResponse = '<p class="botResult">'+val+BotResponse+'</p><div class="clearfix"></div>';
						}
						else{
							val = val.replace(new RegExp('\r?\n','g'), '<br />');
							var BotResponse = '<p class="botResult">'+val+'</p><div class="clearfix"></div>';
						}

				$(BotResponse).appendTo('#result_div');
			}
			scrollToBottomOfResults();
			hideSpinner();
		}, 500);
	}


	//------------------------------------- Set user response in result_div ------------------------------------
	function setUserResponse(val) {
		var UserResponse = '<p class="userEnteredText">'+val+'</p><div class="clearfix"></div>';
		$(UserResponse).appendTo('#result_div');
		$("#chat-input").val('');
		scrollToBottomOfResults();
		showSpinner();
		$('.suggestion').remove();
	}


	//---------------------------------- Scroll to the bottom of the results div -------------------------------
	function scrollToBottomOfResults() {
		var terminalResultsDiv = document.getElementById('result_div');
		terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
	}


	//---------------------------------------- Ascii Spinner ---------------------------------------------------
	function showSpinner() {
		$('.spinner').show();
	}
	function hideSpinner() {
		$('.spinner').hide();
	}


	//------------------------------------------- Suggestions --------------------------------------------------
	function addSuggestion(textToAdd) {
		setTimeout(function() {
			var suggestions = textToAdd.replies;
			var suggLength = textToAdd.replies.length;
			$('<p class="suggestion"></p>').appendTo('#result_div');
			$('<div class="sugg-title">Suggestions: </div>').appendTo('.suggestion');
			// Loop through suggestions
			for(i=0;i<suggLength;i++) {
				$('<span class="sugg-options">'+suggestions[i]+'</span>').appendTo('.suggestion');
			}
			scrollToBottomOfResults();
		}, 1000);
	}

	// on click of suggestions get value and send to API.AI
	$(document).on("click", ".suggestion span", function() {
		var text = this.innerText;
		setUserResponse(text);
		send(text);
		$('.suggestion').remove();
	});
	// Suggestions end -----------------------------------------------------------------------------------------
});
