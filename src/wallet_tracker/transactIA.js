
const WebSocket = require('ws');

var btcs = new WebSocket("wss://ws.blockchain.info/inv");

btcs.onopen = function(){
    btcs.send(JSON.stringify({"op":"addr_sub", "addr":"UNPrfWgJfkANmd1jt88A141PjhiarT8d9U"}));
};

btcs.onmessage = function(onmsg){
    var response = JSON.parse(onmsg.data);
    var getOuts = response.x.out;
    var countOuts = getOuts.length;

    for(i=0; i<countOuts; i++) {
	var outAdd = response.x.out[i].addr;
	var address = "UNPrfWgJfkANmd1jt88A141PjhiarT8d9U";
	if (outAdd == address) {
	    var amount = response.x.out[i].value;
	    var calAmount = amout / 100000000;
	    //document.getElementById("websocket").innetHTML = "Amount recieved" + calAmount + "BTC";
		console.log(calAmount);	    
	};
    };
};