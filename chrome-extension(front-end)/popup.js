//Initialize jquery for extension load
$(function(){
	//Before executing any operation, this function is called in order to
	//clear out any remnants from output.
	function clear(){
		document.getElementById("txtResponse").innerHTML = " "
		document.getElementById("txtResponse1").innerHTML = " "
		document.getElementById("txtResponse2").innerHTML = " "
		document.getElementById("txtResponse3").innerHTML = " "
		document.getElementById("txtResponse4").innerHTML = " "
		document.getElementById("txtResponse5").innerHTML = " "
		document.getElementById("txtResponse6").innerHTML = " "
		document.getElementById("txtResponse7").innerHTML = " "

		document.getElementById("txtResponse").innerText = " "
		document.getElementById("txtResponse1").innerText = " "
		document.getElementById("txtResponse2").innerText = " "
		document.getElementById("txtResponse3").innerText = " "
		document.getElementById("txtResponse4").innerText = " "
		document.getElementById("txtResponse5").innerText = " "
		document.getElementById("txtResponse6").innerText = " "
		document.getElementById("txtResponse7").innerText = " "

		document.getElementById("txtResponse").innerText = "Please wait while it loads."
	}

	//Setup event listener on button
	$("#btnTerm").click(function(e){
		//Tab url is received 
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			clear();
			//Ajax request is sent here.
    		$.ajax({
        		url: "http://localhost:5000/api/btnTerm",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
					//In the event of a successful response, outputs are shown between html tags.
					$("#txtResponse").text(" ")
					$("#txtResponse").text(response.detail).css({ 'color': "maroon"});
					$("#txtResponse1").html(response.detail2).css({ 'color': 'black'});
        		}
    		});

  		});		
	});
	$("#btnNer").click(function(e){

		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			clear();
    		$.ajax({
        		url: "http://localhost:5000/api/btnNer",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text(" ")   
					$("#txtResponse").text(response.org).css({ 'color': 'maroon'});
					$("#txtResponse1").text(response.org2).css({ 'color': 'black'});
					$("#txtResponse2").text(response.per).css({ 'color': 'maroon'});
					$("#txtResponse3").text(response.per2).css({ 'color': 'black'});
					$("#txtResponse4").text(response.loc).css({ 'color': 'maroon'});
					$("#txtResponse5").text(response.loc2).css({ 'color': 'black'});
					$("#txtResponse6").text(response.time).css({ 'color': 'maroon'});
					$("#txtResponse7").text(response.time2).css({ 'color': 'black'});
        		}
    		});
  		});		
	});

	$("#btnRegex").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			//Input is taken from the user.
			SentRegex = prompt("Please enter a regular expression. Example: (?<=Start).+?(?=End)")
			let taburl = tabs[0].url;
    		dict2 = {taburl: taburl, SentRegex: SentRegex}
			clear();
    		$.ajax({
        		url: "http://localhost:5000/api/btnRegex",
        		type: "post",
        		data: JSON.stringify(dict2),
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text(" ")   
					$("#txtResponse1").html(response.detail).css({ 'color': 'black'});
					$("#txtResponse2").text(response.detail2);
        		}
    		});
  		});		
	});

	$("#btnCon").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			clear();
    		$.ajax({
        		url: "http://localhost:5000/api/btnCon",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text(" ")   
					$("#txtResponse1").text(response.detail).css({ 'color': 'black'});
        		}
    		});
  		});		
	});
	$("#btnWord").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			clear();
    		$.ajax({
        		url: "http://localhost:5000/api/btnWord",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text(" ")
					$("#txtResponse").text(response.detail).css({ 'color': 'black'});
        		}
    		});
  		});		
	});
	$("#btnSum").click(function(e){
		SentNum = prompt("How many sentences do you want?")
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			dict2 = {taburl: taburl, SentNum: SentNum}
			clear();
    		$.ajax({
        		url: "http://localhost:5000/api/btnSum",
        		type: "post",
        		data: JSON.stringify(dict2),
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text(" ")
					$("#txtResponse1").text(response.detail).css({ 'color': 'black'});
        		}
    		});
  		});		
	});
	 
$("#btnKeyword").click(function (e) {
	//keyword is targeted in order to get keyword input.
    var keyWord = document.getElementById("keyword");
	// input searched keyword is taken
    SentNum = keyWord.value;
	// Default value is 1 since HTML shows it as selected in initial start. 
    let isChecked = 1; 
	
	//isChecked becomes 1 when the checkbox is selected, otherwise it becomes 0. 
    $("#caseSens").on("change", function () {
        this.value = this.checked ? 1 : 0;
        isChecked = this.value;
      }).change();

	 
    chrome.tabs.query({active: true, currentWindow: true}, tabs => {
      let taburl = tabs[0].url;
      document.getElementById("keyword").addEventListener("keypress", function (e) {
        var keyWord = document.getElementById("keyword");
		// input searched keyword is taken
        SentNum = keyWord.value; 
		// code for enter
        if (e.key === "Enter") {
          if (SentNum.length != 0) //If the user has not entered any input, don't send ajax request.  
		  {
            dict2 = { taburl: taburl, SentNum: SentNum, case: isChecked };
			clear();
            $.ajax({
              url: "http://localhost:5000/api/btnKeyword",
              type: "post",
              data: JSON.stringify(dict2),
              contentType: "application/json",
              success: function (response) {
				$("#txtResponse").text(" ")
                $("#txtResponse1").html(response.detail).css({ color: "black" });
              },
            });
          }
        }
      });
	  //Code for keyword button click
	  var keyWord = document.getElementById("keyword");
	  SentNum = keyWord.value; // input searched keyword is taken
		if (SentNum.length != 0) {
		  dict2 = { taburl: taburl, SentNum: SentNum, case: isChecked };
		  clear();
		  $.ajax({
			url: "http://localhost:5000/api/btnKeyword",
			type: "post",
			data: JSON.stringify(dict2),
			contentType: "application/json",
			success: function (response) {
				$("#txtResponse").text(" ")
			  	$("#txtResponse1").html(response.detail).css({ color: "black" });
			},
		  });
		}
    });
  });
	$("#btnOCR").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			clear();
    		$.ajax({
        		url: "http://localhost:5000/api/btnOCR",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text(" ")
					$("#txtResponse1").html(response.detail).css({ 'color': 'black'});
					$("#txtResponse2").text(response.detail2)
        		}
    		});
  		});		
	});
	$("#btnBertSum").click(function(e){
		SentNum = prompt("How many sentences do you want?")
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			dict2 = {taburl: taburl, SentNum: SentNum}
			clear();
    		$.ajax({
        		url: "http://localhost:5000/api/btnBertSum",
        		type: "post",
        		data: JSON.stringify(dict2),
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text(" ")
					$("#txtResponse1").text(response.detail).css({ 'color': 'black'});
        		}
    		});
  		});		
	});
});

