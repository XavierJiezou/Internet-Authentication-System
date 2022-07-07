import CryptoJS from "crypto-js";
function stringtoaesencrypt(data) {
	var temp_key = 'root%$#@!1234567';
	var temp_iv = getRandNum();
	var key = CryptoJS.enc.Latin1.parse(temp_key.substring(0, 16));
	var iv = CryptoJS.enc.Latin1.parse(temp_iv.substring(0, 16));
	var encrypted = CryptoJS.AES.encrypt(data, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.ZeroPadding });
	return encrypted + temp_iv;
}
function stringtoaesdecrypt(data) {
	var key = 'root%$#@!1234567';
	var iv = data.substring(data.length - 16, data.length);
	var subdata = data.substring(0, data.length - 16);
	var key1 = CryptoJS.enc.Latin1.parse(key);
	var iv1 = CryptoJS.enc.Latin1.parse(iv);
	var decrypted = CryptoJS.AES.decrypt(subdata, key1, {
		iv: iv1,
		mode: CryptoJS.mode.CBC,
		padding: CryptoJS.pad.ZeroPadding
	});
	return decrypted.toString(CryptoJS.enc.Utf8);
}
function getRandNum() {
	var chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
	var nums = "";
	for (var i = 0; i < 16; i++) {
		var id = parseInt(Math.random() * 61);
		nums += chars[id];
	}
	return nums;
}
console.log(stringtoaesencrypt('hello'))