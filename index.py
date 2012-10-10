#!/usr/bin/env python

import os
import urllib
import cgi
import cgitb
cgitb.enable()

if "SSL_CLIENT_S_DN" in os.environ:
    dn = "&".join(
        ["%s=%s" % (attribute[0].lower(), urllib.quote(attribute[1]))
         for attribute in [attribute.strip().split("=", 2)
                           for attribute in os.environ["SSL_CLIENT_S_DN"].split("/")[1:]]])
    cn = os.environ["SSL_CLIENT_S_DN_CN"]
else:
    dn = ""
    cn = ""

print "Content-type: text/html"
print
print """<html><head>
<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">
  
    <link type="text/css" href="index_files/ui.css" rel="stylesheet">
    <link type="text/css" href="index_files/custom.css" rel="stylesheet">
    <script src="index_files/jquery-1.js" type="text/javascript"></script>
    <script src="index_files/jquery.js" type="text/javascript"></script>
    <script src="index_files/ui_002.js" type="text/javascript"></script>
    <script src="index_files/ui.js" type="text/javascript"></script>
    <script src="index_files/jquery_002.js" type="text/javascript"></script>
    <script src="index_files/jquery_003.js" type="text/javascript"></script>
    <script src="index_files/files.txt" type="text/javascript"></script>

    <script src="./data/users.json"></script>
    <script src="./data/policies.json" type="text/javascript"></script>

  <style type="text/css">/* TREE LAYOUT */ .tree ul { margin:0 0 0 5px; padding:0 0 0 0; list-style-type:none; } .tree li { display:block; min-height:18px; line-height:18px; padding:0 0 0 15px; margin:0 0 0 0; /* Background fix */ clear:both; } .tree li ul { display:none; } .tree li a, .tree li span { display:inline-block;line-height:16px;height:16px;color:black;white-space:nowrap;text-decoration:none;padding:1px 4px 1px 4px;margin:0; } .tree li a:focus { outline: none; } .tree li a input, .tree li span input { margin:0;padding:0 0;display:inline-block;height:12px !important;border:1px solid white;background:white;font-size:10px;font-family:Verdana; } .tree li a input:not([class="xxx"]), .tree li span input:not([class="xxx"]) { padding:1px 0; } /* FOR DOTS */ .tree .ltr li.last { float:left; } .tree > ul li.last { overflow:visible; } /* OPEN OR CLOSE */ .tree li.open ul { display:block; } .tree li.closed ul { display:none !important; } /* FOR DRAGGING */ #jstree-dragged { position:absolute; top:-10px; left:-10px; margin:0; padding:0; } #jstree-dragged ul ul ul { display:none; } #jstree-marker { padding:0; margin:0; line-height:5px; font-size:1px; overflow:hidden; height:5px; position:absolute; left:-45px; top:-30px; z-index:1000; background-color:transparent; background-repeat:no-repeat; display:none; } #jstree-marker.marker { width:45px; background-position:-32px top; } #jstree-marker.marker_plus { width:5px; background-position:right top; } /* BACKGROUND DOTS */ .tree li li { overflow:hidden; } .tree > .ltr > li { display:table; } /* ICONS */ .tree ul ins { display:inline-block; text-decoration:none; width:16px; height:16px; } .tree .ltr ins { margin:0 4px 0 0px; } </style><link
 href="index_files/style.css" media="all" type="text/css" 
rel="stylesheet"><style type="text/css">#filetree li[rel=group] > a ins {  background-image:url(img/network-workgroup.png); } #filetree li[rel=folder] > a ins {  background-image:url(img/folder.png); } #filetree li[rel=file] > a ins {  background-image:url(img/x-office-document.png); } </style></head><body>
  <img style="float: left; width: 25em;" 
src="./img/idm_header_logo.png">
    <div id="main" style="width: 40em; padding: 2px; margin-left: auto; 
margin-right: auto;">
      <div id="sender" style="height: 8em; border: 1px solid; margin: 
2px; padding: 0.5em;">
      	<p>The sender's URL:</p>
        <a target="_blank" href="http://dice.csail.mit.edu/idm/idm_query.cgi?""" + dn + """#me">""" + cn + """</a>
        <img style="float: right; margin-left: 0.5em; margin-right: 
auto; height: 5em; width: 5em;" id="senderimg" 
src="index_files/image-x-generic.png">
      </div>
      <div id="file" style="height: 17em; border: 1px solid; margin: 
2px; overflow: auto;">
        <p style="float: left; margin: 2px; padding: 0.5em;">Please 
enter the data's URL, or select from the files below:</p>
        <input id="filebox" name="filebox" style="width: 30em; margin: 
0.5em;">
        <div class="tree tree-classic" id="filetree" 
style="margin-bottom: 2em; direction: ltr;"><ul class="ltr"><li 
rel="group" class="closed last"><a href="" style="" class=""><ins>&nbsp;</ins>Fusion</a><ul><li
 class="closed" rel="folder"><a href="" style="" class=""><ins>&nbsp;</ins>Analysa</a><ul><li
 class="last closed" rel="folder"><a href="" style="" class=""><ins>&nbsp;</ins>RFI</a><ul><li
 class="leaf" rel="file"><a 
href="./MA/documents/Fake_MA_Request.pdf"
 style="" class=""><ins>&nbsp;</ins>RBGuy</a></li><li class="leaf" 
rel="file"><a 
href="./MA/documents/Fake_MA_Request_core10.pdf"
 style="" class=""><ins>&nbsp;</ins>RBGuyCore</a></li><li class="leaf" 
rel="file"><a 
href="http://dig.csail.mit.edu/2009/DHS-fusion/documents/BBunny.pdf" 
style="" class=""><ins>&nbsp;</ins>BBunny</a></li><li class="last leaf" 
rel="file"><a 
href="http://dig.csail.mit.edu/2009/DHS-fusion/documents/ACapone.pdf" 
style="" class=""><ins>&nbsp;</ins>ACapone</a></li></ul></li></ul></li><li
 class="last closed" rel="folder"><a href="" style="" class=""><ins>&nbsp;</ins>Received</a><ul><li
 class="last closed" rel="folder"><a href="" style="" class=""><ins>&nbsp;</ins>FBI</a><ul><li
 class="leaf" rel="file"><a 
href="http://dig.csail.mit.edu/2009/DHS-fusion/documents/ACapone.pdf" 
style="" class=""><ins>&nbsp;</ins>ACapone</a></li><li class="leaf" 
rel="file"><a 
href="http://dig.csail.mit.edu/2009/DHS-fusion/documents/DBerkowitz.pdf"
 style="" class=""><ins>&nbsp;</ins>DBerkowitz</a></li><li class="last 
leaf" rel="file"><a 
href="http://dig.csail.mit.edu/2009/DHS-fusion/documents/CManson.pdf" 
style="" class=""><ins>&nbsp;</ins>CManson</a></li></ul></li></ul></li></ul></li></ul></div>
      </div>
      <div id="recipient" style="height: 8em; border: 1px solid; margin:
 2px; padding: 0.5em;">
      	<p>Please enter the recipient's URL:</p>
        <input class="ui-autocomplete-input" autocomplete="off" 
id="recipientbox" name="recipientbox" style="margin-top: 1em; float: 
left; width: 30em;">
        <img style="float: right; height: 5em; width: 5em;" 
id="recipientimg" src="index_files/image-x-generic.png">
      </div>
      <div id="policy" style="height: 6.3em; border: 1px solid; margin: 
2px; padding: 0.5em;">
      	<p>Please enter a policy's URL:</p>
        <input class="ui-autocomplete-input" autocomplete="off" 
id="policybox" name="policybox" style="width: 30em;" value="Massachusetts MGL 6-172">
      </div>
      <div id="should_tb" style="border: 1px solid; margin: 2px; 
padding: 0.5em;">
        <table><tbody><tr>
        <td><input id="use_tabulator" name="use_tabulator" value="true" 
type="checkbox"></td>
        <td><p style="font-size: 80%;">Display results using the <a 
href="http://www.w3.org/2005/ajar/tab">Tabulator</a> Firefox browser 
extension. <br>This is the recommended way to display results, but can 
be disabled if you are not able to install Tabulator.</p></td>
        </tr></tbody></table>
      </div>
      <div id="summary" style="height: 10em; border: 1px solid; margin: 
2px; padding: 0.5em;">
        <p style="margin: 2px;">From: <span id="summary_sender"><a target="_blank" href="http://dice.csail.mit.edu/idm/idm_query.cgi?""" + dn + """#me">""" + cn + """</a></span></p>
        <p style="margin: 2px;">To: <span id="summary_recipient"></span></p>
        <p style="margin: 2px;">File: <span id="summary_file"></span></p>
        <p style="margin: 2px;">Policy: <span id="summary_policy"><a target='_blank' href='http://dice.csail.mit.edu/idm/MA/rules/MGL_6-172.n3'>Massachusetts MGL 6-172</a></span></p>
        <input style="float: right; margin-right: 1em;" value="Submit" 
id="summary_submit" type="button">
      </div>
    </div>
  <script type="text/javascript">
  function isValidURL(url){
    var RegExp = /^(([\w]+:)?\/\/)?(([\d\w]|%[a-fA-f\d]{2,2})+(:([\d\w]|%[a-fA-f\d]{2,2})+)?@)?([\d\w][-\d\w]{0,253}[\d\w]\.)+[\w]{2,4}(:[\d]+)?(\/([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)*(\?(&?([-+_~.\d\w]|%[a-fA-f\d]{2,2})=?)*)?(#([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)?$/; 
    if(RegExp.test(url)){
        return true;
    }else{
        return false;
    }
  }
  
    $(document).ready(function(){
      $('#filebox').attr("value", "");
/*
      $('#senderbox').autocomplete({
          data: users,
          matchContains:true,
          formatItem:function(item) {
              return "<strong>"+item.name+"</strong>"; // "+item.email+" <br/><span style='font-size:smaller' >&lt;"+item.uri+"&gt;</span>"; 
          },
          formatMatch:function(item) {
              return item.name; //item.uri +" "+item.email+" "+item.name; 
          },
          formatResult:function(item) {
              return item.name; //item.name+" <"+item.email+">"; 
          }
          }).autocomplete("result",function(e,item) {
//              $('#summary_sender').html("<a target='_blank' href='"+item.uri+"'>"+item.name+ "</a> &lt;"+item.email+"&gt;");
              item.uri = "http://dice.csail.mit.edu/idm/idm_query.cgi?""" + dn + """#me";
              $('#summary_sender').html("<a target='_blank' href='"+item.uri+"'>"+item.name+"</a>");
              senderbox.autocomplete = true;
              var docpart = item.uri.slice(0,item.uri.indexOf('#'));
              var converturi = "http://mr-burns.w3.org/?data-uri[]="+escape(docpart)+"&input=&output=jsonp";
              $.ajax({
                      url: converturi, 
                      success: function( data ) {
                          var dbtemp = $.rdf.databank();
                          dbtemp.load( data );
                          var r = $.rdf({databank:dbtemp}).prefix('foaf', 'http://xmlns.com/foaf/0.1/').about("<"+item.uri+">").where( "?s foaf:depiction ?o" )
                          if(r.get(0)) {
                              $('#senderimg').attr('src',r.get(0).o.value);
                          } else {
                              r = $.rdf({databank:dbtemp}).prefix('foaf', 'http://xmlns.com/foaf/0.1/').about("<"+item.uri+">").where( "?s foaf:img ?o" )
                              if( r.get(0) ) {
                                  $('#senderimg').attr('src',r.get(0).o.value);
                              } else {
                                  $('#senderimg').attr('src','img/image-x-generic.png');
                              }
                          }
                      },
                      dataType: "jsonp"
              });
          });*/
          
      $('#recipientbox').autocomplete({
          data: users,
          matchContains:true,
          formatItem:function(item) {
              return "<strong>"+item.name+"</strong>"; // "+item.email+" <br/><span style='font-size:smaller' >&lt;"+item.uri+"&gt;</span>"; 
          },
          formatMatch:function(item) {
              return item.name; //item.uri +" "+item.email+" "+item.name; 
          },
          formatResult:function(item) {
              return item.name; //item.name+" <"+item.email+">"; 
          }
          }).autocomplete("result",function(e,item) {
//              $('#summary_recipient').html("<a target='_blank' href='"+item.uri+"'>"+item.name+ "</a> &lt;"+item.email+"&gt;");
              var dn = ""
              Object.getOwnPropertyNames(item.dn).forEach(function(key) { dn += encodeURIComponent(key) + "=" + encodeURIComponent(item.dn[key]) + "&"; });
              item.uri = "http://dice.csail.mit.edu/idm/idm_query.cgi?" + dn.substr(0, dn.length - 1) + "#me";
              $('#summary_recipient').html("<a target='_blank' href='"+item.uri+"'>"+item.name+"</a>");
              var docpart = item.uri.slice(0,item.uri.indexOf('#'));
              var converturi = "http://mr-burns.w3.org/?data-uri[]="+escape(docpart)+"&input=&output=jsonp";
              $.ajax({
                      url: converturi, 
                      success: function( data ) {
                          var dbtemp = $.rdf.databank();
                          dbtemp.load( data );
                          var r = $.rdf({databank:dbtemp}).prefix('foaf', 'http://xmlns.com/foaf/0.1/').about("<"+item.uri+">").where("?s foaf:depiction ?o" );
                          if(r.get(0)) {
                              $('#recipientimg').attr('src',r.get(0).o.value);
                          } else {
                              r = $.rdf({databank:dbtemp}).prefix('foaf', 'http://xmlns.com/foaf/0.1/').about("<"+item.uri+">").where( "?s foaf:img ?o" );
                              if( r.get(0) ) {
                                  $('#recipientimg').attr('src',r.get(0).o.value);
                              } else {
                                  $('#recipientimg').attr('src','img/image-x-generic.png');
                              }
                          }
                      },
                      dataType: "jsonp"
              });
          });

    $('#filetree').tree({
  callback: {
    onselect: function( node, tree ) {
      var uri = $(node).children("a:eq(0)").attr("href");
      var name = $(node).children("a:eq(0)").text().substring(1);
      filebox.value = uri;
      $('#summary_file').html("<a href='"+uri+"' target='_blank'>"+name+"</a>");
/*      var parsed = "http://mr-burns.w3.org/?data-uri[]="+escape("http://dice.csail.mit.edu/idm/xmpparser.py?uri="+escape(uri))+"&input=rdf-xml&output=jsonp";
      $.ajax({
                      url: parsed, 
                      success: function( data ) {
                          var dbtemp = $.rdf.databank();
                          dbtemp.load( data );
                          //TODO: this only works if there is a single policy file... is that what we want?
                          var r = $.rdf({databank:dbtemp}).prefix('air','http://dig.csail.mit.edu/2009/AIR/air#').about("<"+uri+">").where("?s air:policy ?o");
                          if(r.get(0)) {
		              var polyuri = r.get(0).o.value.toString();
                              $('#summary_policy').html("<a target='_blank' href='"+polyuri+"'>"+polyuri+"</a>");
		              policybox.value = polyuri;
                          } else {
                              $('#summary_policy').html("");
                          }
                      },
                      dataType: "jsonp"
              });*/
    }
  },
  data:files,
  ui: {
    theme_name: "classic"
  },
  types: {
    "group" : {
      clickable : false,
      renameable: false,
      deletable : false,
      creatable : false,
      draggable : false,
      icon : { image : "img/network-workgroup.png" }
    },
    "folder" : {
      clickable : false,
      renameable: false,
      deletable : false,
      creatable : false,
      draggable : false,
      icon : { image : "img/folder.png" }
    },
    "file" : {
      renameable: false,
      deletable : false,
      creatable : false,
      draggable : false,
      icon : { image : "img/x-office-document.png" }
    }
  }
});

  $('#policybox').autocomplete({
          data: policies,
          matchContains:true,
          formatItem:function(item) {
              return "<strong>"+item.name+"</strong> <br/><span style='font-size:smaller' >&lt;"+item.uri+"&gt;</span>"; 
          },
          formatMatch:function(item) {
              return item.uri +" "+item.name; 
          },
          formatResult:function(item) {
              return item.name; 
          }
          }).autocomplete("result",function(e,item) {
              $('#summary_policy').html("<a target='_blank' href='"+item.uri+"'>"+item.name+ "</a>");
              var policy = item.uri;
          });

    function callToTabulator(sender, recipient, document, policy, senderLabel, recipientLabel){
    	  if (!isValidURL(sender) && !isValidURL(recipient) && !isValidURL(document)){        
		  $('#summary_recipient').html("");
		  //$('#summary_sender').html("");
		  $('#summary_file').html("");
		  alert("The inputed URLs are invalid. Please insert a valid URLs for the desired sender, recipient and document file and try submitting again.");
	  }else if (!isValidURL(sender) && !isValidURL(document)){
		  //$('#summary_sender').html("");
		  $('#summary_file').html("");
		  alert("The inputed URLs are invalid. Please insert a valid URLs for the desired sender and document file and try submitting agian.");
	  }else if(!isValidURL(recipient) && !isValidURL(document)){
		  $('#summary_file').html("");
		  $('#summary_recipient').html("");
		  alert("The inputed URLs are invalid. Please insert a valid URLs for the desired recipient and document file and try submitting again.");
	  }else if (!isValidURL(sender) && !isValidURL(recipient)){        
		  $('#summary_recipient').html("");
		  //$('#summary_sender').html("");
		  alert("The inputed URLs are invalid. Please insert a valid URLs for the desired sender and recipient and try submitting again.");
	  }else if (!isValidURL(sender)){
		  //$('#summary_sender').html("");
		  alert("The inputed URL is invalid. Please insert a valid URL for the desired sender and try submitting agian.");
	  }else if(!isValidURL(recipient)){
		  $('#summary_recipient').html("");
		  alert("The inputed URL is invalid. Please insert a valid URL for the desired recipient and try submitting again.");
	  }else if(!isValidURL(document)){
		  $('#summary_file').html("");
		  alert("The inputed URL is invalid. Please insert a valid URL for the desired document file and try submitting again.");
	  }else{
  
	  	  //If there is an inputed pollicy and it is a valid uri, then use it.
	  	  if(isValidURL(policybox.value)){
	  	  	  policy = policybox.value
	  	  	  $('#summary_policy').html("<a target='_blank' href='"+policy+"'>"+policy+ "</a>");
	  	  }
      var should_tabulator = $('#use_tabulator').attr('checked')
	  	  
 		  var log = "use_tabulator="+should_tabulator+"&by="+escape(sender)+"&to="+escape(recipient)+"&data="+escape(document)+"&rulesFile="+escape(policy);
		  if (senderLabel) { log += "&by_label="+escape(senderLabel); }
		  if (recipientLabel) { log += "&to_label="+escape(recipientLabel); }
		  /* var policyrunner = "http://samuelsw.scripts.mit.edu/dhs_air.py"; */
		  /* var policyrunner = "http://mr-burns.w3.org/cgi-bin/dhs_air.py"; */
		  var policyrunner = "http://dice.csail.mit.edu/dhs_air.py";
      
		  policyrunner = policyrunner + "?" + log;
		  window.open( policyrunner );
	  }
    }
    
$('#summary_submit').click( function( e ) { 
  var sender;
  var sender_label = undefined;
/*
  if($('#summary_sender').children('a:eq(0)').attr('href') == undefined){
  	  sender = senderbox.value;
          $('#summary_sender').html("<a target='_blank' href='"+sender+"'>"+sender+"</a>");
  }else{
*/
  	  sender = $('#summary_sender').children('a:eq(0)').attr('href');
  	  sender_label = $('#summary_sender').children('a:eq(0)').html();
//  }
  
  var recipient;
  var recipient_label = undefined;
  if($('#summary_recipient').children('a:eq(0)').attr('href') == undefined){
  	  recipient = recipientbox.value;
  	  $('#summary_recipient').html("<a target='_blank' href='"+recipient+"'>"+recipient+"</a>");
  }else{
  	  recipient  = $('#summary_recipient').children('a:eq(0)').attr('href');
  	  recipient_label = $('#summary_recipient').children('a:eq(0)').html();
  }
  var document;
  var policy;
  if($('#summary_file').children('a:eq(0)').attr('href') == undefined){
  	  document = filebox.value;
  	  $('#summary_file').html("<a href='"+document+"' target='_blank'>"+document+"</a>");
/*  	  var parsed = "http://mr-burns.w3.org/?data-uri[]="+escape("http://dice.csail.mit.edu/idm/xmpparser.py?uri="+escape(document))+"&input=rdf-xml&output=jsonp";
  	  $.ajax({
                   url: parsed,
                   success: function( data ) {
                   var dbtemp = $.rdf.databank();
                   dbtemp.load( data );
//TODO: this only works if there is a single policy file... is that what we want?
                   var r = $.rdf({databank:dbtemp}).prefix('air','http://dig.csail.mit.edu/2009/AIR/air#').about("<"+document+">").where("?s air:policy ?o");
                   if(r.get(0)) {
                         $('#summary_policy').html("<a target='_blank' href='"+r.get(0).o.value.toString()+"'>"+r.get(0).o.value.toString()+"</a>");
                         policy = r.get(0).o.value.toString();
                   } else {
                          $('#summary_policy').html("");
                   }callToTabulator(sender, recipient, document, policy);
            },
            dataType: "jsonp"
          });*/
   }else{
       	  document = $('#summary_file').children('a:eq(0)').attr('href');
       	  policy = $('#summary_policy').children('a:eq(0)').attr('href');
       	  callToTabulator(sender, recipient, document, policy, sender_label, recipient_label);
  }
});
    });

  </script>
<div style="display: none;" id="jstree-marker"></div></body></html>
"""
