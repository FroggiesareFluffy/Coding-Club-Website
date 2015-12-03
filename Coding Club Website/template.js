function changeStyle(newStyle){
  newstyle = newStyle.options[newStyle.selectedIndex].value
  if (newstyle !== getCookie("style")){
    document.cookie = "style="+newstyle
    location.reload()
  }
}

function getCookie(cookieName) {
    var name = cookieName + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if ((c.indexOf(name)) == 0) {
            //alert("found");
            return c.substr(name.length);
        }

    }
    //alert("not found");
    return null;
}

function setCookie(name,value){
  document.cookie = name+"="+value
}

style = getCookie("style")

if (style == "NHS"){
  document.write('<link type="text/css" rel="stylesheet" href="nhs.css"/>')
} else if (style == "Vampire"){
  document.write('<link type="text/css" rel="stylesheet" href="vampire.css"/>')
} else if (style == "Green"){
  document.write('<link type="text/css" rel="stylesheet" href="green.css"/>')
} else if (style == "Rainbow"){
  document.write('<link type="text/css" rel="stylesheet" href="rainbow.css"/>')
} else if (style == "Unicorn"){
  document.write('<link type="text/css" rel="stylesheet" href="hannah.css">')
} else {
  document.cookie = "style=NHS";
  document.write('<link type="text/css" rel="stylesheet" href="nhs.css"/>')
}

if (navigator.javaEnabled() && navigator.appName !== "Netscape"){
	document.write('<applet archive="penguinGame.jar" code="game.Game" height="200" width="600"></applet>')
	console.log("Java enabled")
	console.log(navigator.appName)
} else {
	document.write('<h1 id="header">Northglenn HS Coding Club</h1>\n')
}

document.write('\
    <form name="styleselector">\
      <select name="newStyle" onChange="changeStyle(this.form.newStyle)">\
        <option value="NHS")')
if (style == "NHS"){
  document.write(" selected")
}
document.write('>\
        NHS Colors\
        <option value="Vampire"')
if (style == "Vampire"){
  document.write(" selected")
}
document.write('>\
        Vampire\
        <option value="Green"')
if (style == "Green"){
  document.write(" selected")
}
document.write('>\
        Green\
        <option value="Rainbow"')
if (style == "Rainbow"){
  document.write(" selected")
}
document.write('>\
        Rainbow\
        <option value="Unicorn"')
if (style == "Unicorn"){
  document.write(" selected")
}
document.write('>\
      Unicorn\
      </select>\
    </form>\
		<ul id="nav">\
			<li> <a href="index.html"> Home </a> </li>\
			<li> <a href="links.html"> Useful links </a> </li>\
			<li> <a href="blog.html"> Blog </a> </li>\
			<li> <a href="about.html"> About </a> </li>\
			<li> <a href="contact.html"> Contact </a> </li>\
		</ul>\
		<div id="body">'
)

