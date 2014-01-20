<html>
<head>
    <style type="text/css">
        ${css}
.scale {
width: 70%;
margin-left: 14%; 
}
    </style>
</head>
<body>
%for o in objects:

<div class="scale">
<b>${o.hotel.name}</b>
<p>${o.order_n}</p>
</div>

%endfor
</body>
</html>