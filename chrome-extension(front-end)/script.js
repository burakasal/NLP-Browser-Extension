var el = document.getElementById("myButton");
if (el) {
  el.addEventListener("click", myFunction);
}

function myFunction() {
  chrome.tabs.getSelected(null, function (tab) {
    chrome.tabs.detectLanguage(tab.id, function (language) {
      if (language !== null) {
        window.location.href = "en.html";
      }
      //     else if(language == "tr"){
      //           window.location.href="tr.html";
      //     }
    });
  });
  
}


var address;

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var tab = tabs[0];
    var title = tab.title;

    console.log("Title: " + title);

    chrome.i18n.detectLanguage(title, function (result) {
          var outputLang = "";
          for (i = 0; i < result.languages.length; i++) {
            outputLang += result.languages[i].language + " ";
          }
          console.log(result);
          document.getElementById("language").innerHTML = outputLang;
        });
});


window.onload = function () {

  document.getElementById("btnKeyword").addEventListener(
    "click",
    function () {
      var labelKeyword = document.createElement("label");
      labelKeyword.setAttribute("for", "keyword");
      labelKeyword.innerText = "Keyword:";
      labelKeyword.setAttribute("id", "keywordLabel");
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
    },
    { once: true }
  );

  var elems = document.getElementsByClassName("buttons");
  for (var i = elems.length; i--; ) {
    elems[i].addEventListener("click", fn, false);
  }

  function fn() {
    if (this.innerText !== "Keyword") {
      document.getElementById("keyword").style.display = "none";
      document.getElementById("caseSens").style.display = "none";
      document.getElementById("checkBoxLabel").style.display = "none";
      document.getElementById("keywordLabel").style.display = "none";
    }
  }
};
