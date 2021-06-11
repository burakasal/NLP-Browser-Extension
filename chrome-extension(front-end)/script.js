var el = document.getElementById("myButton");
if (el) {
  el.addEventListener("click", myFunction);
}
//When the Detect Language button is clicked, routing to nlp.html is done.
function myFunction() {
    window.location.href = "nlp.html"; 
}
//Tab url is received
chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
  let taburl = tabs[0].url;
  //Ajax request is sent to detect language. 
    $.ajax({
        url: "http://localhost:5000/api/btnlangDetect",
        type: "post",
        data: taburl,
        contentType: "application/json",
        success: function (response) {
          //Page language is displayed in html.
          document.getElementById("language").innerHTML = response.language

          //If the language is neither English or Turkish, NER button is hidden.
          if (response.language2 !== "en" && response.language2 !== "tr") {
            document.getElementById("btnNer").style.display = "none";
          }
          //If the language is not English, hide the Summarizer button.
          if(response.language2 !== "en"){
            document.getElementById("btnBertSum").style.display = "none";
          }
        }
    });
  })


window.onload = function () {
  document.getElementById("btnKeyword").addEventListener("click", function () {
    //If the keyword button has not been clicked before.
    if (!document.getElementById("keywordLabel")) {
      //Text box and checkbox are created and displayed in UI.
      var labelKeyword = document.createElement("label"); 
      labelKeyword.setAttribute("for", "keyword");
      labelKeyword.innerText = "Keyword:";
      labelKeyword.setAttribute("id", "keywordLabel");
      labelKeyword.setAttribute("style", "font-weight: bold;");
      document.getElementById("caseSensID").appendChild(labelKeyword);

      var inputKeyword = document.createElement("input");
      inputKeyword.setAttribute("type", "text");
      inputKeyword.setAttribute("id", "keyword");
      inputKeyword.setAttribute("name", "keyword");
      document.getElementById("caseSensID").appendChild(inputKeyword);

      var inputCheckbox = document.createElement("input");
      inputCheckbox.setAttribute("type", "checkbox");
      inputCheckbox.setAttribute("name", "caseSens");
      inputCheckbox.setAttribute("value", "1");
      inputCheckbox.setAttribute("id", "caseSens");
      inputCheckbox.setAttribute("checked", "checked");
      document.getElementById("caseSensID").appendChild(inputCheckbox);

      var labelCheckbox = document.createElement("label");
      labelCheckbox.setAttribute("for", "caseSens");
      labelCheckbox.setAttribute("style", "color: blue;");
      labelCheckbox.setAttribute("id", "checkBoxLabel");
      labelCheckbox.innerHTML = "Case Sensitive";
      document.getElementById("caseSensID").appendChild(labelCheckbox);
    } 
    //If the keyword button has been clicked before, display text box and checkbox again.
    else {
      document.getElementById("keyword").style.display = "inline";
      document.getElementById("caseSens").style.display = "inline";
      document.getElementById("checkBoxLabel").style.display = "inline";
      document.getElementById("keywordLabel").style.display = "inline";
    }
  });

  //All buttons are targeted.
  var elems = document.getElementsByClassName("buttons");
  for (var i = elems.length; i--; ) {
    //All butons are attached an event listener.
    elems[i].addEventListener("click", fn, false);
  }

  function fn() {
    //If any other button than Keyword is clicked, text box and checkbox are hidden.
    if (this.innerText !== "Keyword") {
      document.getElementById("keyword").style.display = "none";
      document.getElementById("caseSens").style.display = "none";
      document.getElementById("checkBoxLabel").style.display = "none";
      document.getElementById("keywordLabel").style.display = "none";
    }
  }
};
