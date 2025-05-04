var toollib = {};
toollib.getScreenCapture = function getScreenCapture(){
    let Thread = threads.start(function(){
        if(auto.service != null){  
                let Allow = textMatches(/(允许|立即开始|统一)/).findOne(10*1000);
                if(Allow){
                    Allow.click();
                }
        }
    });
    if(!requestScreenCapture()){
        log("请求截图权限失败");
        return false;
    }else{
        Thread.interrupt()
        log("已获得截图权限");
        return true;
    }
};