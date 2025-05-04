// var res = http.get("10.0.2.2:8000")
// if(res.statusCode != 200){
//     toast("请求失败: " + res.statusCode );
//     }else{
//     toast("请求成功");
//     toastLog("响应体："+res.body.string());
//     }

function LClick(point){
    if(point){
        log("点击"+point);
        press(point.x+random(0,30),point.y+random(0,30),180+random(0,50));
        return true;
    }else{
        return false;
    }
}
toastLog("AoA,启动！")
//setScreenMetrics(720, 1280);

var toollib = require("toollib.js");
toollib.getScreenCapture();
sleep(1000);

var temp = images.read("./images/00yule.png");
images.captureScreen("/sdcard/$MuMu12Shared/test2.png");
var p = images.findImage(captureScreen(),temp,{threshold: 0.9});
LClick(p);
temp.recycle();
toastLog("AoA,关闭！")
