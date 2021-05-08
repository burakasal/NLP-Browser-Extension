var el = document.getElementById("myButton");
if (el) {
  el.addEventListener("click", myFunction);
}

function myFunction() {
  chrome.tabs.getSelected(null, function (tab) {
    chrome.tabs.detectLanguage(tab.id, function (language) {
      if (language !== null) {
        window.location.href = "nlp.html";
      }
    });
  });

}

chrome.tabs.query({
  active: true,
  currentWindow: true
}, function (tabs) {
  var tab = tabs[0];
  var title = tab.title;

  chrome.i18n.detectLanguage(title, function (result) {
    var outputLang = result.languages[0].language;
    
    var myDict = {
      "en": "English",
      "tr": "Turkish",
      "de": "German",
      "es": "Spanish",
      "fr": "French"
    }

    function get(object, key) {
      var result = object[key];
      if (typeof (result) !== "undefined") {
        return result;
      } else {
        return outputLang;
      }
    }
    var outputLang2 = get(myDict, outputLang)
    document.getElementById("language").innerHTML = outputLang2;
    if (outputLang2 !== "English" && outputLang2 !== "Turkish") {
      document.getElementById("btnNer").style.display = "none";
    }

  });
});


window.onload = function () {
  document.getElementById("btnKeyword").addEventListener("click",
    function () {
      if (!document.getElementById("keywordLabel")) {
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
      } else {
        document.getElementById("keyword").style.display = "inline";
        document.getElementById("caseSens").style.display = "inline";
        document.getElementById("checkBoxLabel").style.display = "inline";
        document.getElementById("keywordLabel").style.display = "inline";

      }
    },
  );

  var elems = document.getElementsByClassName("buttons");
  for (var i = elems.length; i--;) {
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