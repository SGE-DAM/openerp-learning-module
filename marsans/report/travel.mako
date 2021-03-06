<html>
<head>
    <style type="text/css">
        ${css}
#scale {
width: 70%;
margin-left: 14%; 
border:1px solid #eee;
}

 div.header {
  	 border-bottom: 2px solid black;
           width: 100%;
  	 }
  	 
  span.header {
  	display: inline-block;
  	text-align: left;
  	font-size: 12;
  	font-weight: bold;
  	padding-left: 6px;
  	 }
  div.list {
  	page-break-inside: avoid;
           width: 100%;
  	border-bottom:1px solid gray;
  	}
  
  span.list {
  	display: inline-block;
  	text-align: left;
  	font-size: 12;
  	padding-right: 6px;
          vertical-align: middle;
  	margin-top: 7px;
  	padding-bottom: 2px;
  	page-break-inside: avoid;
          min-height: 30px;
  	}
    </style>
</head>
<body>
%for o in objects:

<div class="scale">
<h2>Travel name: ${o.name}</h2>


<div class="list_scales">
	<div class="header">
  		<span class="header" style="width: 5%;">${_("Order")}</span>
  		<span class="header" style="width: 10%;">${_("Hotel")}</span>
  		<span class="header" style="width: 20%;">${_("Date")}</span>
  		<span class="header" style="width: 20%;">${_("End day")}</span>
  		<span class="header" style="width: 10%;">${_("Days")}</span>
		<span class="header" style="width: 10%;">${_("Price")}</span>
		<span class="header" style="width: 10%;">${_("Total")}</span>
  	</div>

%for line in o.scales:

<div class="list">
  		<span class="list" style="width: 5%;">${line.order_n}</span>
  		<span class="list" style="width: 10%;">${line.hotel.name}</span>
  		<span class="list" style="width: 20%;">${line.date_i}</span>
  		<span class="list" style="width: 20%;">${line.end}</span>
  		<span class="list" style="width: 10%;">${line.days}</span>
  		<span class="list" style="width: 10%;">${line.price}</span>
  		<span class="list" style="width: 10%;">${line.total}</span>
  	</div>

%endfor


</div>
</div>

%endfor
<p>Total: ${o.total}</p>
</body>
</html>