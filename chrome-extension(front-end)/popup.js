//Initialize jquery for extension load
$(function(){
	//Setup event listener on button
	$("#btnTerm").click(function(e){

		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			
    		$.ajax({
        		url: "http://localhost:5000/api/fetch",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
           			console.log(response);
					$("#txtResponse").text(response.detail).css({ 'color': "maroon"});
					$("#txtResponse1").html(response.detail2).css({ 'color': 'black'});
					$("#txtResponse2").text(" ")
					$("#txtResponse3").text(" ")
					$("#txtResponse4").text(" ")
					$("#txtResponse5").text(" ")
					$("#txtResponse6").text(" ")
					$("#txtResponse7").text(" ")
        		}
    		});

  		});		
	});
	$("#btnNer").click(function(e){

		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			
    		$.ajax({
        		url: "http://localhost:5000/api/fetch2",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
           			console.log(response);
					$("#txtResponse").text(response.org).css({ 'color': 'maroon'});
					$("#txtResponse1").text(response.org2).css({ 'color': 'black'});
					$("#txtResponse2").text(response.per).css({ 'color': 'maroon'});
					$("#txtResponse3").text(response.per2).css({ 'color': 'black'});
					$("#txtResponse4").text(response.loc).css({ 'color': 'maroon'});
					$("#txtResponse5").text(response.loc2).css({ 'color': 'black'});
        		}
    		});
  		});		
	});

	$("#btnRegex").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			SentRegex = prompt("Please enter a regular expression. Example: (?<=Start).+?(?=End)")
			let taburl = tabs[0].url;
    		dict2 = {taburl: taburl, SentRegex: SentRegex}
    		$.ajax({
        		url: "http://localhost:5000/api/fetch3",
        		type: "post",
        		data: JSON.stringify(dict2),
        		contentType: "application/json",
        		success: function (response) {
           			console.log(response);
					$("#txtResponse").text("");
					$("#txtResponse1").html(response.detail).css({ 'color': 'black'});
					$("#txtResponse2").text(response.detail2);
					$("#txtResponse3").text(" ");
					$("#txtResponse4").text(" ");
					$("#txtResponse5").text(" ");
        		}
    		});
  		});		
	});

	$("#btnCon").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			
    		$.ajax({
        		url: "http://localhost:5000/api/fetch4",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
           			console.log(response);
					$("#txtResponse").text(" ")
					$("#txtResponse1").text(response.detail).css({ 'color': 'black'});
					$("#txtResponse2").text(" ")
					$("#txtResponse3").text(" ")
					$("#txtResponse4").text(" ")
					$("#txtResponse5").text(" ")
					$("#txtResponse6").text(" ")
					$("#txtResponse7").text(" ")
        		}
    		});
  		});		
	});
	$("#btnWord").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			
    		$.ajax({
        		url: "http://localhost:5000/api/fetch5",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
           			console.log(response);
					$("#txtResponse").text(response.detail).css({ 'color': 'black'});
        		}
    		});
  		});		
	});
	$("#btnSum").click(function(e){
		SentNum = prompt("How many sentences do you want? (Please wait while it loads)")
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
			dict2 = {taburl: taburl, SentNum: SentNum}
    		$.ajax({
        		url: "http://localhost:5000/api/fetch6",
        		type: "post",
        		data: JSON.stringify(dict2),
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text(" ");
					$("#txtResponse1").text(response.detail).css({ 'color': 'black'});
					$("#txtResponse2").text(" ");
					$("#txtResponse3").text(" ");
					$("#txtResponse4").text(" ");
					$("#txtResponse5").text(" ");
        		}
    		});
  		});		
	});
	$("#btnTurkNer").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
    		$.ajax({
        		url: "http://localhost:5000/api/fetch7",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
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
	 
$("#btnKeyword").click(function (e) {
    var keyWord = document.getElementById("keyword");
    //console.log(keyWord.value);
    SentNum = keyWord.value; // input searched keyword is taken
    //console.log(SentNum.length);

    let isChecked = 1; // Default value is 1 since HTML shows it as selected in initial start.

    $("#caseSens")
      .on("change", function () {
        this.value = this.checked ? 1 : 0;
        isChecked = this.value;
      })
      .change();

    chrome.tabs.query({active: true, currentWindow: true}, tabs => {
      let taburl = tabs[0].url;
      document
      .getElementById("keyword")
      .addEventListener("keypress", function (e) {
        var keyWord = document.getElementById("keyword");
        //console.log(keyWord.value);
        SentNum = keyWord.value; // input searched keyword is taken
        if (e.key === "Enter") {
          // code for enter
          if (SentNum.length != 0) {
            console.log(taburl);
            dict2 = { taburl: taburl, SentNum: SentNum, case: isChecked };
            $.ajax({
              url: "http://localhost:5000/api/fetch8",
              type: "post",
              data: JSON.stringify(dict2),
              contentType: "application/json",
              success: function (response) {
                $("#txtResponse").text(" ");
                $("#txtResponse1").html(response.detail).css({ color: "black" });
                $("#txtResponse2").text(" ");
                $("#txtResponse3").text(" ");
                $("#txtResponse4").text(" ");
                $("#txtResponse5").text(" ");
              },
            });
          }
        }
      });
    });
  });
	$("#btnOCR").click(function(e){
		chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
			let taburl = tabs[0].url;
    		$.ajax({
        		url: "http://localhost:5000/api/fetch9",
        		type: "post",
        		data: taburl,
        		contentType: "application/json",
        		success: function (response) {
					$("#txtResponse").text("")
					$("#txtResponse1").html(response.detail).css({ 'color': 'black'});
					$("#txtResponse2").text(response.detail2)
					$("#txtResponse3").text(" ")
					$("#txtResponse4").text(" ")
					$("#txtResponse5").text(" ")
        		}
    		});
  		});		
	});
});

